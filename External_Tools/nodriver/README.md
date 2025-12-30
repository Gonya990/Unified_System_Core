# Nodriver Browser Control

> Token-efficient browser control for AI agents via Unix Socket

## Quick Start

```bash
cd ~/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation

# 1. Start Chrome with remote debugging
./start_chrome.sh

# 2. Start the daemon
./start_daemon.sh

# 3. Control browser
./ndc goto "https://example.com"
./ndc screenshot
```

## Scripts

| Script | Purpose |
| ------ | ------- |
| `start_chrome.sh` | Start Chrome with `--remote-debugging-port=9222` |
| `start_daemon.sh` | Start nodriver daemon (connects to Chrome) |
| `ndc` | CLI client for browser commands |

## CLI Reference

### Navigation

```bash
./ndc goto "https://example.com"    # Navigate to URL
./ndc url                            # Get current URL
./ndc title                          # Get page title
```

### Interaction

```bash
./ndc click "Button Text"            # Click by text
./ndc clicksel "button.submit"       # Click by CSS selector
./ndc fill "input#email" "user@x.com" # Fill input
./ndc type "input#pass" "secret"     # Type with delay
./ndc scroll down 500                # Scroll page
```

### Content

```bash
./ndc screenshot                     # Save to /tmp/nodriver_screen.png
./ndc screenshot ~/my.png            # Save to custom path
./ndc text "div.content"             # Get element text
./ndc html                           # Get page HTML
./ndc js "document.title"            # Execute JavaScript
```

### Tabs

```bash
./ndc tabs                           # List all tabs
./ndc newtab "https://google.com"    # Open new tab
./ndc switchtab 1                    # Switch to tab
./ndc closetab 0                     # Close tab
```

### Wait

```bash
./ndc wait "div.loaded" 10           # Wait for element (10s timeout)
```

### Daemon Control

```bash
./ndc status                         # Check daemon status
./ndc stop                           # Stop daemon
```

## Configuration

Edit `~/.nodriver.env`:

```bash
CHROME_DEBUG_PORT=9222
CHROME_EXECUTABLE=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
SOCKET_PATH=/tmp/nodriver.sock
SCREENSHOT_PATH=/tmp/nodriver_screen.png
```

## Manual Chrome Start

If you prefer to start Chrome manually:

```bash
# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222

# Or create an alias in ~/.zshrc:
alias chrome-debug="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --remote-debugging-port=9222"
```

## Troubleshooting

### Chrome not connecting

```bash
# Check if Chrome is running with debug port
curl http://localhost:9222/json/version
```

### Daemon not responding

```bash
# Check socket exists
ls -la /tmp/nodriver.sock

# Check daemon status
./ndc status
```

### Restart everything

```bash
./ndc stop                    # Stop daemon (if running)
pkill -f "Google Chrome"      # Kill Chrome (if needed)
./start_chrome.sh             # Start Chrome
./start_daemon.sh             # Start daemon
```
