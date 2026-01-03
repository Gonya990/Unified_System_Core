# 🌐 Browser Control Architecture Decision

> **Created:** 2025-12-24  
> **Updated:** 2026-01-03
> **Status:** 🚫 DEPRECATED / REVERTED
> **Decision:** Revert to builtin `browser_subagent` (User Request)
> **Package Manager:** UV

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
| **User profile** | Must use existing Chrome instance (no copy) |

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

## ✅ Final Implementation

### Key Decisions Made

| Decision | Value |
| -------- | ----- |
| **Profile approach** | NO copy — connect to existing Chrome via Remote Debugging |
| **Configuration** | `.env` file at `~/.nodriver.env` |
| **Auto-start** | Optional (manual by default) |
| **Package manager** | UV (fast, lockfile) |
| **Uses YOUR Chrome** | ✅ Same instance with all logins, tabs, extensions |

### Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Antigravity   │────▶│   ./ndc CLI     │────▶│ nodriver_daemon │
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

---

## 📁 Project Location

```
Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/
├── .venv/                  # UV virtual environment
├── .env.example            # Config template
├── .gitignore              # Python ignores
├── IMPLEMENTATION_PLAN.md  # Full documentation
├── INSTALL.md              # Quick setup guide
├── ndc                     # CLI client (executable)
├── nodriver_daemon.py      # Main daemon
├── pyproject.toml          # UV dependencies
├── start_daemon.sh         # Convenience starter
└── uv.lock                 # Locked dependencies
```

---

## 🔧 CLI Commands

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

## ⚡ Quick Start

```bash
# 1. Navigate to project
cd ~/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation

# 2. Dependencies are already synced (uv.lock present)
# If needed: uv sync

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

## 📊 Token Efficiency

| Action | Tokens Used |
| ------ | ----------- |
| `ndc goto url` | ~40 |
| `ndc screenshot` | ~30 |
| `ndc click text` | ~35 |
| **Total per action** | **~50-80** |

**Savings vs MCP:** 3-6x fewer tokens ✅

---

## ✅ Implementation Checklist

- [x] nodriver installed via UV
- [x] Daemon created (`nodriver_daemon.py`)
- [x] CLI client created (`ndc`)
- [x] Config template (`.env.example`)
- [x] Install guide (`INSTALL.md`)
- [x] UV project setup (`pyproject.toml`, `uv.lock`)
- [x] Start script (`start_daemon.sh`)
- [ ] Test with Antigravity agent (pending user setup)

---

*Document created: 2025-12-24 | Last updated: 2025-12-24*
