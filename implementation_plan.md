# 🤖 Phase 5 Implementation Plan: Advanced Automation

> **Status:** In Progress (80% Complete)
> **Last Updated:** 2026-01-11
> **Goal:** Deploy Proactive Family Assistant, integrate Content Farm 2.0, and enable MCP Mail Intelligence.

---

## Progress Summary

| Component | Status | Notes |
|-----------|--------|-------|
| TokenBroker Integration | ✅ Complete | `daily_researcher.py` uses TokenBroker |
| Bot Command `/factory` | ✅ Complete | Telegram bot can trigger video pipeline |
| Homework Sentinel | ✅ Complete | `Scripts/Family/homework_sentinel.py` |
| Morning Brief | ✅ Complete | `Scripts/Family/morning_brief.py` |
| MCP Mail Client | ✅ Complete | `Scripts/Orchestration/agent_mail_client.py` |
| Mail Processor Service | ✅ Complete | `Scripts/Orchestration/mail_processor.py` |
| Telegram Alert Integration | 🔄 Pending | Needs env vars configuration |
| Systemd Service Deployment | 🔄 Pending | Deploy mail_processor as service |

---

## 1. Family Assistant (The Sentinel) ✅

### A. Homework Sentinel (`homework_sentinel.py`)

**Status:** ✅ Implemented

**Objective:** Scan Artur's Gmail for keywords ("Homework", "School", "Classroom") and generate a daily summary.
**Mechanism:**

1. **Auth:** Use `IdentityOrchestrator` to load Artur's Gmail Token (needs to be added to `secrets/`).
2. **Scan:** Fetch unread emails from last 24h.
3. **Process:** Extract deadlines and tasks using a cheap LLM (Gemini Flash).
4. **Notify:** Send report to Telegram Bot -> Artur (or Parent).

### B. Morning Brief (`morning_brief.py`)

**Status:** ✅ Implemented

**Objective:** A personalized morning start for Artur (07:00 AM).
**Content:**

- 📅 **Calendar:** First 3 events of the day.
- 🌤️ **Weather:** Current temp + rain forecast (OpenMeteo API).
- 📚 **Homework:** Summary from Sentinel.
- 🚀 **Motivation:** One short quote.

---

## 2. Content Farm 2.0 Integration ✅

### A. Telegram Bot Command `/factory`

**Status:** ✅ Implemented

**Objective:** Allow manual trigger of the video pipeline from Telegram.
**Flow:**

1. User types `/factory topic="AI Future"`.
2. Bot calls `daily_researcher.py` with arguments.
3. Bot subscribes to progress updates (via a status file or callback).

### B. TokenBroker Integration

**Status:** ✅ Implemented

**Objective:** Stop hardcoding API keys.
**Change:** Modify `daily_researcher.py` to:

```python
from Utilities.token_broker import TokenBroker
key = TokenBroker().get_key("openai", owner="Artur")
```

---

## 3. MCP Mail Intelligence 🔄

### A. Mail Processor Service (`mail_processor.py`)

**Status:** ✅ Implemented (2026-01-11)

**Objective:** Background service that monitors MCP Mail inbox and auto-processes messages.

**Features:**

- ⏰ **Polling:** Configurable interval (default 60s)
- 🚨 **Alert Detection:** Scans for high-priority keywords (urgent, critical, emergency, etc.)
- 📋 **Council Processing:** Special handling for FuchsiaCat, VioletCastle, PinkLake, etc.
- 💬 **Telegram Alerts:** Sends high-priority messages to Admin Telegram
- ✅ **Auto-Acknowledgement:** Auto-replies to messages requiring acknowledgement
- 💾 **State Persistence:** Tracks processed message IDs

**Usage:**

```bash
# Run as daemon
python3 Scripts/Orchestration/mail_processor.py

# Run once (for cron)
python3 Scripts/Orchestration/mail_processor.py --once

# Test Telegram alert
python3 Scripts/Orchestration/mail_processor.py --test-alert

# Custom interval
python3 Scripts/Orchestration/mail_processor.py --interval 30
```

### B. Configuration Required

**Environment Variables:**

```bash
# Add to .env
TELEGRAM_ADMIN_CHAT_ID=<your_telegram_chat_id>
TELEGRAM_BOT_TOKEN=<your_bot_token>

# Already configured:
AGENT_MAIL_SERVER=http://100.110.209.49:8765
AGENT_MAIL_PROJECT=home-gonya-unified-system
AGENT_MAIL_NAME=Antigravity
```

---

## 4. Next Steps (Remaining Tasks)

### Step 1: Configure Telegram Integration

- [ ] Ensure `TELEGRAM_ADMIN_CHAT_ID` is set in `.env`
- [ ] Ensure `TELEGRAM_BOT_TOKEN` is set in `.env`
- [ ] Run `--test-alert` to verify

### Step 2: Deploy Mail Processor as Systemd Service

- [ ] Create `/etc/systemd/system/mail-processor.service`
- [ ] Enable and start service
- [ ] Verify logs in `Scripts/Orchestration/logs/`

### Step 3: Integration Testing

- [ ] Send test message via `agent_mail_client.py send --to Antigravity --subject "Test Alert" --body "urgent help needed"`
- [ ] Verify Telegram alert received
- [ ] Check council message log

---

## 5. Verification Checklist

- [x] Run `/factory` from Telegram -> Verify video generation starts
- [x] Run `homework_sentinel.py` -> Check logs for email fetching
- [x] `agent_mail_client.py health` -> Server healthy
- [x] `agent_mail_client.py inbox` -> Can retrieve messages
- [ ] `mail_processor.py --test-alert` -> Telegram alert received
- [ ] Mail processor service running 24/7

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Unified System                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Telegram   │◄──►│  AI Bot v2   │◄──►│   TokenBroker │  │
│  │     Bot      │    │              │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│          │                  │                              │
│          ▼                  ▼                              │
│  ┌──────────────┐    ┌──────────────┐                     │
│  │ Mail         │    │  Content     │                     │
│  │ Processor    │    │  Factory     │                     │
│  │ (Alerts)     │    │  Pipeline    │                     │
│  └──────────────┘    └──────────────┘                     │
│          │                                                 │
│          ▼                                                 │
│  ┌──────────────────────────────────────────────────────┐ │
│  │           MCP Agent Mail Server                       │ │
│  │           (100.110.209.49:8765)                      │ │
│  └──────────────────────────────────────────────────────┘ │
│          ▲                                                 │
│          │                                                 │
│  ┌───────┴──────────────────────────────────────────────┐ │
│  │  Council Agents: FuchsiaCat, VioletCastle, PinkLake  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
