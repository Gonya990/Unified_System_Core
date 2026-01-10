# 🤖 Phase 5 Implementation Plan: Advanced Automation

> **Status:** Draft
> **Goal:** Deploy Proactive Family Assistant and integrate Content Farm 2.0.

## 1. Family Assistant (The Sentinel)

### A. Homework Sentinel (`homework_sentinel.py`)

**Objective:** Scan Artur's Gmail for keywords ("Homework", "School", "Classroom") and generate a daily summary.
**Mechanism:**

1. **Auth:** Use `IdentityOrchestrator` to load Artur's Gmail Token (needs to be added to `secrets/`).
2. **Scan:** Fetch unread emails from last 24h.
3. **Process:** Extract deadlines and tasks using a cheap LLM (Gemini Flash).
4. **Notify:** Send report to Telegram Bot -> Artur (or Parent).

### B. Morning Brief (`morning_brief.py`)

**Objective:** A personalized morning start for Artur (07:00 AM).
**Content:**

- 📅 **Calendar:** First 3 events of the day.
- 🌤️ **Weather:** Current temp + rain forecast (OpenMeteo API).
- 📚 **Homework:** Summary from Sentinel.
- 🚀 **Motivation:** One short quote.

## 2. Content Farm 2.0 Integration

### A. Telegram Bot Command `/factory`

**Objective:** Allow manual trigger of the video pipeline from Telegram.
**Flow:**

1. User types `/factory topic="AI Future"`.
2. Bot calls `daily_researcher.py` with arguments.
3. Bot subscribes to progress updates (via a status file or callback).

### B. TokenBroker Integration

**Objective:** Stop hardcoding API keys.
**Change:** Modify `daily_researcher.py` to:

```python
from Utilities.token_broker import TokenBroker
key = TokenBroker().get_key("openai", owner="Artur")
```

## 3. Implementation Steps

### Step 1: TokenBroker Adoption (Immediate)

- Modify `daily_researcher.py` to use `TokenBroker`.
- **Reason:** Prerequisite for reliable operation.

### Step 2: Bot Command `/factory`

- Add handler to `ai_telegram_bot_v2.py`.
- **Reason:** User requested "Do it!!!" for control.

### Step 3: Family Assistant

- Create `Scripts/Family/` directory.
- Implement `homework_sentinel.py` (Mock auth first if token missing).
- Implement `morning_brief.py`.

## 4. Verification

- Run `/factory` from Telegram -> Verify video generation starts.
- Run `homework_sentinel.py` -> Check logs for email fetching.
