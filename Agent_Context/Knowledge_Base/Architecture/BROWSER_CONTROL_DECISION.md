# 🌐 Browser Control Architecture Decision

> **Created:** 2025-12-24  
> **Status:** ✅ DECIDED  
> **Decision:** Unix Socket Daemon + CLI

---

## 🎯 Goal

Enable Antigravity agent to control a **local Chrome browser** with:

- User's saved logins and sessions
- User's browser extensions
- Minimal bot detection
- Token-efficient communication

---

## 🚫 Constraints

| Constraint | Description |
| ---------- | ----------- |
| **No built-in tool modification** | Cannot add new tools to Antigravity agent directly |
| **Must use existing tools** | `run_command`, `view_file`, etc. |
| **Token efficiency** | Minimize tokens per browser action |
| **Stealth** | Avoid CAPTCHA and bot detection |
| **User profile** | Must use existing Chrome profile with logins |

---

## 🔍 Options Evaluated

### Option 1: MCP Server (Rejected)

| Pros | Cons |
| ---- | ---- |
| Standard protocol | High token overhead (~300+ per action) |
| Well-documented | Complex setup |
| | Protocol overhead (JSON-RPC) |

### Option 2: HTTP API (Considered)

| Pros | Cons |
| ---- | ---- |
| Easy to debug | Moderate token overhead (~120 per action) |
| Standard HTTP | curl syntax verbose |
| Web-accessible | Network overhead |

### Option 3: run_command Scripts (Rejected)

| Pros | Cons |
| ---- | ---- |
| Simple | Very slow (new browser each time) |
| No daemon needed | High token overhead |
| | Unreliable |

### Option 4: Unix Socket Daemon + CLI ✅ CHOSEN

| Pros | Cons |
| ---- | ---- |
| **Lowest token overhead (~50 per action)** | Requires daemon running |
| Fast (persistent browser) | macOS/Linux only |
| Simple CLI commands | |
| No network exposure | |

---

## ✅ Decision: Unix Socket Daemon + CLI

### Why

1. **Token efficiency** - ~3-6x fewer tokens than MCP
2. **Performance** - Browser stays open, no startup delay
3. **Security** - Unix socket, no network exposure
4. **Simplicity** - Short CLI commands

### Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Antigravity   │────▶│   ~/ndc CLI     │────▶│ nodriver_daemon │
│     Agent       │     │ (run_command)   │     │  (persistent)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         │                      │                       ▼
         │                      │              ┌─────────────────┐
         │                      │              │  Your Chrome    │
         │                      │              │  (with logins)  │
         │                      └──────────────│                 │
         │                    Unix Socket      └─────────────────┘
         │                 /tmp/nodriver.sock
         │
         ▼
    Screenshots at
    /tmp/nodriver_screen.png
```

---

## 📋 Components to Implement

| Component | File | Purpose |
| --------- | ---- | ------- |
| **Daemon** | `~/nodriver_daemon.py` | Persistent browser controller |
| **CLI Client** | `~/ndc` | Command-line interface |
| **LaunchAgent** | `~/Library/LaunchAgents/com.nodriver.daemon.plist` | Auto-start on macOS |
| **Profile Copy** | `~/nodriver_profile/` | Copy of Chrome profile |

---

## 🔧 CLI Commands Design

| Command | Example | Description |
| ------- | ------- | ----------- |
| `goto` | `ndc goto "https://url"` | Navigate to URL |
| `screenshot` | `ndc screenshot` | Save screenshot to /tmp |
| `click` | `ndc click "Button Text"` | Click by text |
| `clicksel` | `ndc clicksel "css.selector"` | Click by CSS selector |
| `fill` | `ndc fill "selector" "text"` | Fill input field |
| `type` | `ndc type "selector" "text"` | Type with delay |
| `text` | `ndc text "selector"` | Get element text |
| `js` | `ndc js "code"` | Execute JavaScript |
| `html` | `ndc html` | Get page HTML |
| `title` | `ndc title` | Get page title |
| `url` | `ndc url` | Get current URL |
| `tabs` | `ndc tabs` | List open tabs |
| `newtab` | `ndc newtab "url"` | Open new tab |
| `closetab` | `ndc closetab 0` | Close tab by index |
| `scroll` | `ndc scroll down 500` | Scroll page |
| `wait` | `ndc wait "selector" 10` | Wait for element |
| `status` | `ndc status` | Daemon status |
| `stop` | `ndc stop` | Stop daemon |

---

## 📁 File Locations

```
~/
├── nodriver_daemon.py          # Main daemon service
├── ndc                         # CLI client (executable)
├── nodriver_profile/           # Chrome profile copy
└── Library/
    └── LaunchAgents/
        └── com.nodriver.daemon.plist  # Auto-start
```

---

## ⚠️ Open Questions

1. **Chrome profile path** - Where is your Chrome profile located?
   - Default macOS: `~/Library/Application Support/Google/Chrome/Default`
   - Need to confirm

2. **Chrome executable path** - Which Chrome to use?
   - Default: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
   - Need to confirm

3. **Auto-start on boot?** - Should daemon start automatically?
   - If yes, create LaunchAgent
   - If no, manual start

---

## 📊 Token Usage Projection

| Action | Estimated Tokens |
| ------ | ---------------- |
| `ndc goto url` | ~40 |
| `ndc screenshot` | ~30 |
| `ndc click text` | ~35 |
| Response parsing | ~20 |
| **Total per action** | **~50-80** |

**Savings vs MCP:** 3-6x fewer tokens

---

*Document created: 2025-12-24*
