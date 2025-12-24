#!/usr/bin/env python3
"""
Nodriver Daemon - Browser control via Unix Socket
Connects to existing Chrome instance via Remote Debugging Protocol

Usage:
    1. Start Chrome with: --remote-debugging-port=9222
    2. Run: python nodriver_daemon.py
    3. Use ~/ndc CLI to control browser
"""

import asyncio
import json
import os
import signal
import socket
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Load environment from .env file
def load_env():
    env_paths = [
        Path.home() / ".nodriver.env",
        Path(__file__).parent / ".env",
        Path.cwd() / ".env"
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())
            print(f"✓ Loaded config from {env_path}")
            break

load_env()

# Configuration from environment
CONFIG = {
    "chrome_debug_port": int(os.getenv("CHROME_DEBUG_PORT", "9222")),
    "chrome_executable": os.getenv("CHROME_EXECUTABLE", 
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    "socket_path": os.getenv("SOCKET_PATH", "/tmp/nodriver.sock"),
    "screenshot_path": os.getenv("SCREENSHOT_PATH", "/tmp/nodriver_screen.png"),
    "auto_start_chrome": os.getenv("AUTO_START_CHROME", "false").lower() == "true",
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "element_timeout": int(os.getenv("ELEMENT_TIMEOUT", "10")),
    "page_load_timeout": int(os.getenv("PAGE_LOAD_TIMEOUT", "30")),
    "socket_timeout": int(os.getenv("SOCKET_TIMEOUT", "5")),
}

# Try to import nodriver
try:
    import nodriver as uc
    NODRIVER_AVAILABLE = True
except ImportError:
    NODRIVER_AVAILABLE = False
    print("⚠ nodriver not installed. Install with: pip install nodriver")


class BrowserDaemon:
    """Unix Socket daemon for browser control"""
    
    def __init__(self):
        self.browser = None
        self.page = None
        self.tabs: list = []
        self.running = False
        self.socket_path = CONFIG["socket_path"]
        
    async def connect_to_chrome(self) -> bool:
        """Connect to existing Chrome instance via CDP"""
        if not NODRIVER_AVAILABLE:
            return False
            
        try:
            # Connect to existing Chrome with remote debugging
            self.browser = await uc.start(
                headless=False,
                browser_args=[
                    f"--remote-debugging-port={CONFIG['chrome_debug_port']}"
                ]
            )
            
            # Get first tab or create one
            self.page = await self.browser.get("about:blank")
            self.tabs = [self.page]
            
            print(f"✓ Connected to Chrome on port {CONFIG['chrome_debug_port']}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to connect to Chrome: {e}")
            print(f"  Make sure Chrome is running with:")
            print(f"  {CONFIG['chrome_executable']} --remote-debugging-port={CONFIG['chrome_debug_port']}")
            return False
    
    async def handle_command(self, cmd: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single command and return result"""
        action = cmd.get("action", "").lower()
        
        try:
            # Navigation
            if action == "goto":
                url = cmd.get("url", "about:blank")
                self.page = await self.browser.get(url)
                title = await self.page.evaluate("document.title")
                return {"ok": True, "title": title, "url": url}
            
            # Screenshot
            elif action == "screenshot":
                path = cmd.get("path", CONFIG["screenshot_path"])
                await self.page.save_screenshot(path)
                return {"ok": True, "path": path}
            
            # Click by text
            elif action == "click":
                text = cmd.get("text", "")
                element = await self.page.find(text, best_match=True)
                if element:
                    await element.click()
                    return {"ok": True, "clicked": text}
                return {"ok": False, "error": f"Element not found: {text}"}
            
            # Click by selector
            elif action == "clicksel":
                selector = cmd.get("selector", "")
                element = await self.page.select(selector)
                if element:
                    await element.click()
                    return {"ok": True, "clicked": selector}
                return {"ok": False, "error": f"Selector not found: {selector}"}
            
            # Fill input (JS-based for better compatibility)
            elif action == "fill":
                selector = cmd.get("selector", "")
                text = cmd.get("text", "")
                js_code = f"""
                (() => {{
                    const el = document.querySelector("{selector}");
                    if (!el) return {{ok: false, error: "Selector not found: {selector}"}};
                    el.focus();
                    el.value = "{text}";
                    el.dispatchEvent(new Event('input', {{bubbles: true}}));
                    el.dispatchEvent(new Event('change', {{bubbles: true}}));
                    return {{ok: true, filled: "{selector}"}};
                }})()
                """
                result = await self.page.evaluate(js_code)
                return result if isinstance(result, dict) else {"ok": True, "filled": selector}
            
            # Type with delay (human-like, JS-based)
            elif action == "type":
                selector = cmd.get("selector", "")
                text = cmd.get("text", "")
                delay = cmd.get("delay", 50)
                # Use JS to simulate typing
                js_code = f"""
                (async () => {{
                    const el = document.querySelector("{selector}");
                    if (!el) return {{ok: false, error: "Selector not found: {selector}"}};
                    el.focus();
                    for (const char of "{text}") {{
                        el.value += char;
                        el.dispatchEvent(new Event('input', {{bubbles: true}}));
                        await new Promise(r => setTimeout(r, {delay}));
                    }}
                    return {{ok: true, typed: {len(text)}}};
                }})()
                """
                result = await self.page.evaluate(js_code)
                return result if isinstance(result, dict) else {"ok": True, "typed": len(text)}
            
            # Get element text
            elif action == "text":
                selector = cmd.get("selector", "")
                js_code = f"""
                (() => {{
                    const el = document.querySelector("{selector}");
                    if (!el) return {{ok: false, error: "Selector not found: {selector}"}};
                    return {{ok: true, text: el.innerText || el.textContent || ""}};
                }})()
                """
                result = await self.page.evaluate(js_code)
                return result if isinstance(result, dict) else {"ok": False, "error": "Unknown error"}
            
            # Execute JavaScript
            elif action == "js":
                code = cmd.get("code", "")
                result = await self.page.evaluate(code)
                return {"ok": True, "result": result}
            
            # Get page HTML
            elif action == "html":
                html = await self.page.evaluate("document.documentElement.outerHTML")
                # Save to file if too large
                if len(html) > 10000:
                    path = "/tmp/nodriver_page.html"
                    with open(path, "w") as f:
                        f.write(html)
                    return {"ok": True, "path": path, "length": len(html)}
                return {"ok": True, "html": html}
            
            # Get page title
            elif action == "title":
                title = await self.page.evaluate("document.title")
                return {"ok": True, "title": title}
            
            # Get current URL
            elif action == "url":
                url = await self.page.evaluate("window.location.href")
                return {"ok": True, "url": url}
            
            # List tabs
            elif action == "tabs":
                tabs_info = []
                for i, tab in enumerate(self.tabs):
                    try:
                        title = await tab.evaluate("document.title")
                        url = await tab.evaluate("window.location.href")
                        tabs_info.append({"index": i, "title": title, "url": url})
                    except:
                        tabs_info.append({"index": i, "title": "?", "url": "?"})
                return {"ok": True, "tabs": tabs_info, "active": 0}
            
            # New tab
            elif action == "newtab":
                url = cmd.get("url", "about:blank")
                new_page = await self.browser.get(url)
                self.tabs.append(new_page)
                self.page = new_page
                return {"ok": True, "index": len(self.tabs) - 1}
            
            # Close tab
            elif action == "closetab":
                index = cmd.get("index", -1)
                if 0 <= index < len(self.tabs):
                    # Close tab (nodriver specific)
                    self.tabs.pop(index)
                    if self.tabs:
                        self.page = self.tabs[-1]
                    return {"ok": True, "closed": index}
                return {"ok": False, "error": f"Invalid tab index: {index}"}
            
            # Switch tab
            elif action == "switchtab":
                index = cmd.get("index", 0)
                if 0 <= index < len(self.tabs):
                    self.page = self.tabs[index]
                    return {"ok": True, "switched": index}
                return {"ok": False, "error": f"Invalid tab index: {index}"}
            
            # Scroll
            elif action == "scroll":
                direction = cmd.get("direction", "down")
                amount = cmd.get("amount", 500)
                if direction == "down":
                    await self.page.scroll_down(amount)
                else:
                    await self.page.scroll_up(amount)
                return {"ok": True, "scrolled": direction, "amount": amount}
            
            # Wait for element
            elif action == "wait":
                selector = cmd.get("selector", "")
                timeout = cmd.get("timeout", CONFIG["element_timeout"])
                # Use JS polling since nodriver doesn't have wait_for
                js_code = f"""
                new Promise((resolve) => {{
                    const start = Date.now();
                    const check = () => {{
                        if (document.querySelector("{selector}")) {{
                            resolve(true);
                        }} else if (Date.now() - start > {timeout * 1000}) {{
                            resolve(false);
                        }} else {{
                            setTimeout(check, 100);
                        }}
                    }};
                    check();
                }})
                """
                try:
                    found = await self.page.evaluate(js_code)
                    if found:
                        return {"ok": True, "found": selector}
                    return {"ok": False, "error": f"Timeout waiting for: {selector}"}
                except Exception as e:
                    return {"ok": False, "error": f"Wait error: {str(e)}"}
            
            # Daemon status
            elif action == "status":
                url = await self.page.evaluate("window.location.href") if self.page else "none"
                return {
                    "ok": True,
                    "status": "running",
                    "tabs": len(self.tabs),
                    "current_url": url,
                    "config": {
                        "chrome_port": CONFIG["chrome_debug_port"],
                        "socket": self.socket_path
                    }
                }
            
            # Stop daemon
            elif action == "stop":
                self.running = False
                return {"ok": True, "status": "stopping"}
            
            else:
                return {"ok": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    async def run_server(self):
        """Run Unix socket server"""
        # Remove old socket
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
        
        # Create socket
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.socket_path)
        server.listen(5)
        server.setblocking(False)
        
        # Make socket accessible
        os.chmod(self.socket_path, 0o777)
        
        print(f"✓ Socket server listening at {self.socket_path}")
        self.running = True
        
        loop = asyncio.get_event_loop()
        
        while self.running:
            try:
                # Accept connection with timeout
                try:
                    conn, _ = await asyncio.wait_for(
                        loop.sock_accept(server),
                        timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue
                
                # Read command
                data = await loop.sock_recv(conn, 65536)
                if not data:
                    conn.close()
                    continue
                
                # Parse and handle command
                try:
                    cmd = json.loads(data.decode())
                    result = await self.handle_command(cmd)
                except json.JSONDecodeError as e:
                    result = {"ok": False, "error": f"Invalid JSON: {e}"}
                
                # Send response
                response = json.dumps(result)
                await loop.sock_sendall(conn, response.encode())
                conn.close()
                
            except Exception as e:
                print(f"✗ Server error: {e}")
        
        # Cleanup
        server.close()
        os.unlink(self.socket_path)
        print("✓ Server stopped")
    
    async def start(self):
        """Start the daemon"""
        print("=" * 50)
        print("  Nodriver Daemon")
        print("=" * 50)
        print(f"  Chrome port: {CONFIG['chrome_debug_port']}")
        print(f"  Socket: {self.socket_path}")
        print("=" * 50)
        
        # Connect to Chrome
        if not await self.connect_to_chrome():
            print("\n⚠ To start Chrome with remote debugging, run:")
            print(f'  "{CONFIG["chrome_executable"]}" --remote-debugging-port={CONFIG["chrome_debug_port"]}')
            print("\nOr set AUTO_START_CHROME=true in .env")
            sys.exit(1)
        
        # Setup signal handlers
        def signal_handler(sig, frame):
            print("\n⚡ Received interrupt signal, stopping...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Run server
        await self.run_server()
        
        # Cleanup browser
        if self.browser:
            self.browser.stop()


async def main():
    daemon = BrowserDaemon()
    await daemon.start()


if __name__ == "__main__":
    asyncio.run(main())
