# 🚀 Implementation Plan: Nodriver Unix Socket Daemon

> **Created:** 2025-12-24  
> **Status:** ✅ IMPLEMENTED  
> **Time to Install:** ~5 minutes

---

## ✅ Final Decisions

| Decision | Value |
| -------- | ----- |
| **Profile approach** | NO copy — connect to existing Chrome via Remote Debugging |
| **Configuration** | `.env` file at `~/.nodriver.env` |
| **Auto-start** | Optional (manual by default) |
| **Uses YOUR Chrome** | ✅ Same instance with all logins, tabs, extensions |

---

## 📋 Implementation Status

- [x] **UV installed**: Fast Python package manager ✅
- [x] **nodriver installed**: via `uv sync` ✅
- [x] **Daemon created**: `nodriver_daemon.py` ✅
- [x] **CLI client created**: `ndc` ✅
- [x] **Config template**: `.env.example` ✅
- [x] **Install guide**: `INSTALL.md` ✅
- [x] **Start script**: `start_daemon.sh` ✅
- [x] **Dependencies locked**: `uv.lock` ✅

---

## 🔧 Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Antigravity   │────▶│   ~/ndc CLI     │────▶│ nodriver_daemon │
│     Agent       │     │ (run_command)   │     │ (Unix Socket)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        │ CDP WebSocket
                                                        ▼
                                               ┌─────────────────┐
                                               │  YOUR Chrome    │
                                               │ --remote-debug  │
                                               │   port=9222     │
                                               └─────────────────┘
```

**Key Points:**

- Chrome runs with `--remote-debugging-port=9222`
- Daemon connects via CDP (Chrome DevTools Protocol)
- No profile copy needed — it's YOUR Chrome instance
- All logins, extensions, tabs work as-is

---

## ⚡ Quick Start (UV)

```bash
# 1. Navigate to project
cd ~/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation

# 2. Dependencies already synced (uv.lock present)
# If needed: source ~/.local/bin/env && uv sync

# 3. Start Chrome with debugging
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222

# 4. Start daemon
./start_daemon.sh

# 5. Use CLI
./ndc status
./ndc goto "https://example.com"
./ndc screenshot
```

---

## 🚀 Usage

### Step 1: Start Chrome with debugging

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222
```

### Step 2: Start daemon (in another terminal)

```bash
python3 ~/nodriver_daemon.py
```

### Step 3: Control browser

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
| **goto** | `ndc goto "url"` | Navigate to URL |
| **screenshot** | `ndc screenshot` | Save to /tmp/nodriver_screen.png |
| **click** | `ndc click "text"` | Click by text |
| **clicksel** | `ndc clicksel "css"` | Click by selector |
| **fill** | `ndc fill "sel" "text"` | Fill input |
| **type** | `ndc type "sel" "text"` | Type human-like |
| **text** | `ndc text "sel"` | Get element text |
| **js** | `ndc js "code"` | Execute JavaScript |
| **html** | `ndc html` | Get page HTML |
| **title** | `ndc title` | Get page title |
| **url** | `ndc url` | Get current URL |
| **tabs** | `ndc tabs` | List all tabs |
| **newtab** | `ndc newtab "url"` | Open new tab |
| **switchtab** | `ndc switchtab 0` | Switch to tab |
| **closetab** | `ndc closetab 0` | Close tab |
| **scroll** | `ndc scroll down 500` | Scroll page |
| **wait** | `ndc wait "sel" 10` | Wait for element |
| **status** | `ndc status` | Daemon status |
| **stop** | `ndc stop` | Stop daemon |

---

## ⚙️ Configuration

Edit `~/.nodriver.env`:

```bash
# Chrome Settings
CHROME_DEBUG_PORT=9222
CHROME_EXECUTABLE=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome

# Socket Settings  
SOCKET_PATH=/tmp/nodriver.sock
SCREENSHOT_PATH=/tmp/nodriver_screen.png

# Timeouts (seconds)
ELEMENT_TIMEOUT=10
PAGE_LOAD_TIMEOUT=30
```

---

## 🔄 Optional: Auto-Start Daemon

Create LaunchAgent for automatic startup:

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
        <string>/usr/bin/python3</string>
        <string>/Users/macbook/nodriver_daemon.py</string>
    </array>
    <key>RunAtLoad</key>
    <false/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
EOF

# Load (run once)
launchctl load ~/Library/LaunchAgents/com.nodriver.daemon.plist

# Start when needed
launchctl start com.nodriver.daemon
```

---

## 📁 Deliverables

| File | Description | Status |
| ---- | ----------- | ------ |
| `nodriver_daemon.py` | Main daemon service | ✅ Created |
| `ndc` | CLI client | ✅ Created |
| `.env.example` | Config template | ✅ Created |
| `INSTALL.md` | Setup guide | ✅ Created |
| LaunchAgent plist | Auto-start | ⏳ Optional |

---

## 🧪 Testing Checklist

| Test | Command | Expected |
| ---- | ------- | -------- |
| Start daemon | `python ~/nodriver_daemon.py` | "✓ Connected to Chrome" |
| Check status | `~/ndc status` | `{"ok":true,"status":"running"}` |
| Navigate | `~/ndc goto "https://example.com"` | `{"ok":true,"title":"..."}` |
| Screenshot | `~/ndc screenshot` | File at `/tmp/nodriver_screen.png` |
| Click | `~/ndc click "More information"` | `{"ok":true,"clicked":"..."}` |
| Stop | `~/ndc stop` | Daemon exits |

---

## 📊 Token Efficiency

| Action | Tokens Used |
| ------ | ----------- |
| `ndc goto url` | ~40 |
| `ndc screenshot` | ~30 |
| `ndc click text` | ~35 |
| **Total per action** | **~50-80** |

**vs MCP Protocol:** 3-6x fewer tokens ✅

---

*Updated: 2025-12-24*
