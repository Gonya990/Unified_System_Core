#!/usr/bin/env python3
"""
Hooks Manager for Unified System
================================
Manages system hooks - read, list, execute, and provide API endpoints.

Supports hook types:
- SessionStart: Triggered when a new agent session starts
- SessionEnd: Triggered when an agent session ends  
- SubagentStart: Triggered when a subagent task begins
- SubagentStop: Triggered when a subagent task completes
- FileChange: Triggered when specific files are modified
- ScheduledTask: Triggered at specific times/intervals
- Custom: User-defined triggers

Usage:
    python hooks_manager.py --list              # List all hooks
    python hooks_manager.py --get <hook_type>   # Get hooks by type
    python hooks_manager.py --run <hook_type>   # Execute hooks of type
    python hooks_manager.py --serve             # Start HTTP API server
"""

import json
import os
import subprocess
import argparse
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import http.server
import socketserver
import urllib.parse

# Configuration
HOOKS_DIR = Path(__file__).parent
HOOKS_CONFIG = HOOKS_DIR / "hooks.json"
SCRIPTS_DIR = HOOKS_DIR / "scripts"

@dataclass
class HookDefinition:
    """Represents a single hook definition."""
    hook_type: str
    matcher: str
    command: Optional[str] = None
    script: Optional[str] = None
    timeout: int = 30
    enabled: bool = True
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass  
class HookResult:
    """Result of hook execution."""
    hook_type: str
    command: str
    success: bool
    output: str
    error: str
    duration_ms: int
    timestamp: str


class HooksManager:
    """Manages all system hooks."""
    
    def __init__(self, config_path: Path = HOOKS_CONFIG):
        self.config_path = config_path
        self.hooks: Dict[str, List[HookDefinition]] = {}
        self._load_hooks()
    
    def _load_hooks(self) -> None:
        """Load hooks from JSON configuration file."""
        if not self.config_path.exists():
            self.hooks = {}
            return
            
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
            
            self.description = data.get("description", "")
            hooks_data = data.get("hooks", {})
            
            for hook_type, hook_list in hooks_data.items():
                self.hooks[hook_type] = []
                for entry in hook_list:
                    matcher = entry.get("matcher", "*")
                    for hook_def in entry.get("hooks", []):
                        self.hooks[hook_type].append(HookDefinition(
                            hook_type=hook_type,
                            matcher=matcher,
                            command=hook_def.get("command"),
                            script=hook_def.get("script"),
                            timeout=hook_def.get("timeout", 30),
                            enabled=hook_def.get("enabled", True),
                            description=hook_def.get("description", "")
                        ))
        except json.JSONDecodeError as e:
            print(f"Error parsing hooks.json: {e}", file=sys.stderr)
            self.hooks = {}
    
    def get_all_hooks(self) -> Dict[str, List[Dict]]:
        """Get all registered hooks."""
        return {
            hook_type: [h.to_dict() for h in hooks]
            for hook_type, hooks in self.hooks.items()
        }
    
    def get_hooks_by_type(self, hook_type: str) -> List[Dict]:
        """Get hooks of a specific type."""
        hooks = self.hooks.get(hook_type, [])
        return [h.to_dict() for h in hooks]
    
    def list_scripts(self) -> List[str]:
        """List all available hook scripts."""
        if not SCRIPTS_DIR.exists():
            return []
        return [f.name for f in SCRIPTS_DIR.iterdir() if f.is_file()]
    
    def execute_hooks(self, hook_type: str, context: Optional[Dict] = None) -> List[HookResult]:
        """Execute all hooks of a given type."""
        results = []
        hooks = self.hooks.get(hook_type, [])
        
        for hook in hooks:
            if not hook.enabled:
                continue
                
            command = hook.command
            if hook.script:
                script_path = SCRIPTS_DIR / hook.script
                if script_path.exists():
                    command = str(script_path)
            
            if not command:
                continue
            
            # Expand environment variables
            env = os.environ.copy()
            if context:
                for key, value in context.items():
                    env[f"HOOK_{key.upper()}"] = str(value)
            
            # Expand ${CLAUDE_PLUGIN_ROOT} and similar
            expanded_cmd = os.path.expandvars(command)
            
            start_time = datetime.now()
            try:
                result = subprocess.run(
                    expanded_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=hook.timeout,
                    env=env,
                    cwd=str(HOOKS_DIR.parent)
                )
                duration = (datetime.now() - start_time).total_seconds() * 1000
                
                results.append(HookResult(
                    hook_type=hook_type,
                    command=expanded_cmd,
                    success=result.returncode == 0,
                    output=result.stdout,
                    error=result.stderr,
                    duration_ms=int(duration),
                    timestamp=datetime.now().isoformat()
                ))
            except subprocess.TimeoutExpired:
                results.append(HookResult(
                    hook_type=hook_type,
                    command=expanded_cmd,
                    success=False,
                    output="",
                    error=f"Timeout after {hook.timeout}s",
                    duration_ms=hook.timeout * 1000,
                    timestamp=datetime.now().isoformat()
                ))
            except Exception as e:
                results.append(HookResult(
                    hook_type=hook_type,
                    command=expanded_cmd,
                    success=False,
                    output="",
                    error=str(e),
                    duration_ms=0,
                    timestamp=datetime.now().isoformat()
                ))
        
        return results

    def get_status(self) -> Dict[str, Any]:
        """Get hooks system status."""
        return {
            "config_path": str(self.config_path),
            "config_exists": self.config_path.exists(),
            "scripts_dir": str(SCRIPTS_DIR),
            "scripts_available": self.list_scripts(),
            "hook_types": list(self.hooks.keys()),
            "total_hooks": sum(len(h) for h in self.hooks.values()),
            "hooks_by_type": {k: len(v) for k, v in self.hooks.items()},
            "timestamp": datetime.now().isoformat()
        }


class HooksHTTPHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for hooks API."""
    
    manager: HooksManager = None  # Set by server
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def _send_json(self, data: Any, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        
        if path == "/hooks/all" or path == "/hooks":
            self._send_json({
                "status": "ok",
                "hooks": self.manager.get_all_hooks()
            })
        
        elif path == "/hooks/status":
            self._send_json({
                "status": "ok",
                **self.manager.get_status()
            })
        
        elif path == "/hooks/scripts":
            self._send_json({
                "status": "ok",
                "scripts": self.manager.list_scripts()
            })
        
        elif path.startswith("/hooks/type/"):
            hook_type = path.split("/")[-1]
            hooks = self.manager.get_hooks_by_type(hook_type)
            self._send_json({
                "status": "ok",
                "hook_type": hook_type,
                "hooks": hooks
            })
        
        elif path == "/health" or path == "/health/liveness":
            self._send_json({"status": "ok", "service": "hooks-manager"})
        
        else:
            self._send_json({
                "status": "error",
                "message": "Not found",
                "available_endpoints": [
                    "GET /hooks/all - List all hooks",
                    "GET /hooks/status - Get system status",
                    "GET /hooks/scripts - List available scripts",
                    "GET /hooks/type/<type> - Get hooks by type",
                    "POST /hooks/run/<type> - Execute hooks of type"
                ]
            }, status=404)
    
    def do_POST(self):
        """Handle POST requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path.startswith("/hooks/run/"):
            hook_type = path.split("/")[-1]
            
            # Read body for context
            content_length = int(self.headers.get('Content-Length', 0))
            context = {}
            if content_length > 0:
                body = self.rfile.read(content_length)
                try:
                    context = json.loads(body)
                except json.JSONDecodeError:
                    pass
            
            results = self.manager.execute_hooks(hook_type, context)
            self._send_json({
                "status": "ok",
                "hook_type": hook_type,
                "executed": len(results),
                "results": [asdict(r) for r in results]
            })
        
        else:
            self._send_json({
                "status": "error", 
                "message": "Method not allowed"
            }, status=405)


def serve(port: int = 8765):
    """Start HTTP API server."""
    manager = HooksManager()
    HooksHTTPHandler.manager = manager
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), HooksHTTPHandler) as httpd:
        print(f"Hooks API server running on http://0.0.0.0:{port}")
        print(f"Endpoints:")
        print(f"  GET  /hooks/all     - List all hooks")
        print(f"  GET  /hooks/status  - System status")
        print(f"  GET  /hooks/scripts - Available scripts")
        print(f"  GET  /hooks/type/<t> - Hooks by type")
        print(f"  POST /hooks/run/<t>  - Execute hooks")
        httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Hooks Manager for Unified System")
    parser.add_argument("--list", "-l", action="store_true", help="List all hooks")
    parser.add_argument("--get", "-g", type=str, help="Get hooks by type")
    parser.add_argument("--run", "-r", type=str, help="Run hooks of type")
    parser.add_argument("--status", "-s", action="store_true", help="Show status")
    parser.add_argument("--scripts", action="store_true", help="List available scripts")
    parser.add_argument("--serve", action="store_true", help="Start HTTP server")
    parser.add_argument("--port", "-p", type=int, default=8766, help="Server port (default: 8766)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    manager = HooksManager()
    
    if args.list:
        hooks = manager.get_all_hooks()
        if args.json:
            print(json.dumps(hooks, indent=2))
        else:
            for hook_type, hook_list in hooks.items():
                print(f"\n{hook_type}:")
                for h in hook_list:
                    cmd = h.get('command') or h.get('script', 'N/A')
                    status = "✓" if h.get('enabled', True) else "✗"
                    print(f"  {status} [{h['matcher']}] {cmd[:60]}...")
    
    elif args.get:
        hooks = manager.get_hooks_by_type(args.get)
        if args.json:
            print(json.dumps(hooks, indent=2))
        else:
            for h in hooks:
                print(f"  - {h.get('command') or h.get('script')}")
    
    elif args.run:
        results = manager.execute_hooks(args.run)
        if args.json:
            print(json.dumps([asdict(r) for r in results], indent=2))
        else:
            for r in results:
                status = "✓" if r.success else "✗"
                print(f"{status} {r.command} ({r.duration_ms}ms)")
                if r.output:
                    print(f"   Output: {r.output[:100]}...")
                if r.error:
                    print(f"   Error: {r.error[:100]}...")
    
    elif args.status:
        status = manager.get_status()
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print(f"Config: {status['config_path']}")
            print(f"Exists: {status['config_exists']}")
            print(f"Total hooks: {status['total_hooks']}")
            print(f"Hook types: {', '.join(status['hook_types'])}")
            print(f"Scripts: {', '.join(status['scripts_available'])}")
    
    elif args.scripts:
        scripts = manager.list_scripts()
        if args.json:
            print(json.dumps(scripts, indent=2))
        else:
            for s in scripts:
                print(f"  - {s}")
    
    elif args.serve:
        serve(args.port)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
