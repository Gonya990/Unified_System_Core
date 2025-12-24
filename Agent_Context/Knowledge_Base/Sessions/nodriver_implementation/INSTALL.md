# 🚀 Nodriver Installation Guide

> **Quick Setup for Unix Socket Browser Control**  
> **Uses UV for dependency management**

---

## 📦 Files

| File | Purpose |
| ---- | ------- |
| `nodriver_daemon.py` | Main daemon service |
| `ndc` | CLI client |
| `pyproject.toml` | UV dependencies |
| `.env.example` | Configuration template |

---

## ⚡ Quick Install (UV)

```bash
# Navigate to project
cd /Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation

# Sync dependencies (creates .venv automatically)
uv sync

# Copy CLI and config to home
cp ndc ~/ndc && chmod +x ~/ndc
cp .env.example ~/.nodriver.env
```

---

## 🔧 Chrome Setup

**Start Chrome with Remote Debugging:**

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222
```

**Or create an alias:**

```bash
echo 'alias chrome-debug="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --remote-debugging-port=9222"' >> ~/.zshrc
source ~/.zshrc

# Then just run:
chrome-debug
```

---

## 🚀 Usage

### 1. Start Chrome with debugging

```bash
chrome-debug
```

### 2. Start daemon (using UV)

```bash
cd /Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation
uv run python nodriver_daemon.py
```

### 3. Control browser

```bash
~/ndc goto "https://web.telegram.org"
~/ndc screenshot
~/ndc click "Saved Messages"
~/ndc status
```

---

## 📋 All Commands

| Command | Example | Description |
| ------- | ------- | ----------- |
| **goto** | `ndc goto "url"` | Navigate |
| **screenshot** | `ndc screenshot` | → /tmp/nodriver_screen.png |
| **click** | `ndc click "text"` | Click by text |
| **clicksel** | `ndc clicksel "css"` | Click by selector |
| **fill** | `ndc fill "sel" "text"` | Fill input |
| **type** | `ndc type "sel" "text"` | Type human-like |
| **text** | `ndc text "sel"` | Get element text |
| **js** | `ndc js "code"` | Execute JavaScript |
| **html** | `ndc html` | Get page HTML |
| **title** | `ndc title` | Get page title |
| **url** | `ndc url` | Get current URL |
| **tabs** | `ndc tabs` | List tabs |
| **newtab** | `ndc newtab "url"` | Open new tab |
| **switchtab** | `ndc switchtab 0` | Switch tab |
| **closetab** | `ndc closetab 0` | Close tab |
| **scroll** | `ndc scroll down 500` | Scroll |
| **wait** | `ndc wait "sel" 10` | Wait for element |
| **status** | `ndc status` | Daemon status |
| **stop** | `ndc stop` | Stop daemon |

---

## ⚙️ Configuration

Edit `~/.nodriver.env`:

```bash
CHROME_DEBUG_PORT=9222
CHROME_EXECUTABLE=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
SOCKET_PATH=/tmp/nodriver.sock
SCREENSHOT_PATH=/tmp/nodriver_screen.png
```

---

## 🔄 Optional: Auto-Start

```bash
cat > ~/Library/LaunchAgents/com.nodriver.daemon.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nodriver.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/macbook/.local/bin/uv</string>
        <string>run</string>
        <string>--directory</string>
        <string>/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation</string>
        <string>python</string>
        <string>nodriver_daemon.py</string>
    </array>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.nodriver.daemon.plist
```

---

## 🧪 Quick Test

```bash
# Terminal 1: Start Chrome
chrome-debug

# Terminal 2: Start daemon
cd /Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation
uv run python nodriver_daemon.py

# Terminal 3: Test commands
~/ndc status
~/ndc goto "https://httpbin.org/user-agent"
~/ndc screenshot
```

---

*Created: 2025-12-24 | Package Manager: UV*
