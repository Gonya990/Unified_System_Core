# 🚀 Implementation Plan: Nodriver Unix Socket Daemon

> **Created:** 2025-12-24  
> **Status:** 📋 PLANNED  
> **Estimated Time:** 30-45 minutes

---

## 📋 Pre-Implementation Checklist

Before we start, I need to confirm:

- [ ] **Chrome profile location** (default: `~/Library/Application Support/Google/Chrome/Default`)
- [ ] **Chrome executable path** (default: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`)
- [ ] **Auto-start on boot?** (create LaunchAgent plist)
- [ ] **Python version** (need 3.8+)

---

## 🔧 Phase 1: Environment Setup (5 min)

### Step 1.1: Create virtual environment

```bash
python3 -m venv ~/nodriver_env
source ~/nodriver_env/bin/activate
```

### Step 1.2: Install dependencies

```bash
pip install nodriver
```

### Step 1.3: Copy Chrome profile

```bash
# Close Chrome first!
cp -r ~/Library/Application\ Support/Google/Chrome/Default ~/nodriver_profile
```

**Verification:**

- [ ] `~/nodriver_env/` exists
- [ ] `nodriver` is installed
- [ ] `~/nodriver_profile/` exists

---

## 🔧 Phase 2: Create Daemon (15 min)

### Step 2.1: Create daemon script

**File:** `~/nodriver_daemon.py`

**Features:**

- Unix socket server at `/tmp/nodriver.sock`
- Persistent browser instance using user's Chrome profile
- Support for all CLI commands
- JSON request/response protocol
- Error handling and logging
- Graceful shutdown

**Commands to implement:**

| Command | Priority | Description |
| ------- | -------- | ----------- |
| `goto` | P0 | Navigate to URL |
| `screenshot` | P0 | Capture screen |
| `click` | P0 | Click by text |
| `clicksel` | P1 | Click by selector |
| `fill` | P0 | Fill input |
| `type` | P1 | Type with delay |
| `text` | P1 | Get element text |
| `js` | P0 | Execute JavaScript |
| `html` | P2 | Get page HTML |
| `title` | P2 | Get page title |
| `url` | P2 | Get current URL |
| `tabs` | P1 | List tabs |
| `newtab` | P1 | Open new tab |
| `closetab` | P1 | Close tab |
| `scroll` | P1 | Scroll page |
| `wait` | P1 | Wait for element |
| `status` | P0 | Check daemon status |
| `stop` | P0 | Stop daemon |

---

## 🔧 Phase 3: Create CLI Client (10 min)

### Step 3.1: Create CLI script

**File:** `~/ndc` (executable)

**Features:**

- Connect to Unix socket
- Parse command-line arguments
- Send JSON request
- Print JSON response
- Handle connection errors
- Timeout handling

**Usage examples:**

```bash
~/ndc goto "https://web.telegram.org"
~/ndc screenshot
~/ndc click "Saved Messages"
~/ndc fill "div.input" "Hello"
~/ndc js "document.title"
```

---

## 🔧 Phase 4: Auto-Start Setup (5 min)

### Step 4.1: Create LaunchAgent (optional)

**File:** `~/Library/LaunchAgents/com.nodriver.daemon.plist`

**Purpose:** Start daemon automatically on login

### Step 4.2: Load LaunchAgent

```bash
launchctl load ~/Library/LaunchAgents/com.nodriver.daemon.plist
```

---

## 🔧 Phase 5: Testing (10 min)

### Step 5.1: Manual testing checklist

| Test | Command | Expected |
| ---- | ------- | -------- |
| Start daemon | `python ~/nodriver_daemon.py` | Browser opens, socket ready |
| Check status | `~/ndc status` | `{"status":"running"}` |
| Navigate | `~/ndc goto "https://example.com"` | Page loads |
| Screenshot | `~/ndc screenshot` | File at `/tmp/nodriver_screen.png` |
| Click | `~/ndc click "More information"` | Element clicked |
| Stop | `~/ndc stop` | Daemon exits cleanly |

### Step 5.2: Integration test with Antigravity

I (Antigravity) will test:

```bash
# Through run_command:
~/ndc goto "https://httpbin.org/user-agent"
~/ndc screenshot
# Then view_file /tmp/nodriver_screen.png
```

---

## 📁 Deliverables

| File | Description | Status |
| ---- | ----------- | ------ |
| `~/nodriver_daemon.py` | Main daemon service | ⏳ Pending |
| `~/ndc` | CLI client | ⏳ Pending |
| `~/nodriver_profile/` | Chrome profile copy | ⏳ Pending |
| `~/Library/LaunchAgents/com.nodriver.daemon.plist` | Auto-start | ⏳ Optional |

---

## ⚠️ Potential Issues & Mitigations

| Issue | Mitigation |
| ----- | ---------- |
| Chrome profile locked | Ensure Chrome is closed before copying profile |
| Socket permission denied | Use `/tmp/` which is world-writable |
| Browser crashes | Implement auto-restart in daemon |
| Slow element finding | Add configurable timeout |
| Multiple simultaneous requests | Use asyncio queue |

---

## 🔄 Rollback Plan

If implementation fails:

1. Delete files: `rm ~/nodriver_daemon.py ~/ndc`
2. Remove LaunchAgent: `launchctl unload ~/Library/LaunchAgents/com.nodriver.daemon.plist`
3. Delete profile copy: `rm -rf ~/nodriver_profile`
4. Fall back to built-in Playwright browser

---

## ✅ Ready to Implement?

**Before proceeding, please confirm:**

1. Is your Chrome profile at the default location?
   `~/Library/Application Support/Google/Chrome/Default`

2. Is Chrome installed at the default location?
   `/Applications/Google Chrome.app/`

3. Do you want auto-start on login? (Y/N)

4. Can I close Chrome if it's currently open? (needed to copy profile)

---

*Plan created: 2025-12-24*
