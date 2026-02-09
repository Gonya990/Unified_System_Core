# 📊 System Status Report & Restoration Plan

> **Date:** 2026-02-05
> **Time:** 22:35 (Local)
> **Status:** 🔴 CRITICAL MAINTENANCE REQUIRED

## 🚨 Critical Findings (The "As-Is")

### 1. 🤖 AI Telegram Bot

* **Status:** STOPPED (Scaled to 0).
* **Root Cause of "Access Denied":** The bot code checks `is_approved` in the
  database. I manually updated the DB, but the bot instance was likely caching
  user state or connected to a different DB (SQLite vs Firestore). Confirmed
  usage of `/app/user_context.db` in K8s, which is **ephemeral** (lost on restart)
  unless persisted.
  * *Correction:* There is a PVC `telegram-bot-pvc` mounted to `/data`, but the
    code uses `/app/user_context.db` by default if not configured to use `/data`.
* **Root Cause of "Conflict":** Multiple instances were running. We found
  **zombie processes** on the host machine (`python -m src.ai_telegram_bot_v2`)
  interacting with the same Token as the K8s pod.
* **Auth Error:** "client_secret.json missing". The bot expects
  `config/gmail_credentials.json`. We mounted it via K8s, but the application
  likely failed to read it due to path mismatch or permission issues (`root` vs
  `app user`).

### 2. 🏭 Content Factory

* **Status:** RUNNING (in Docker), but output is flawed.
* **Video Quality:** User reported "1 second video".
  * *Diagnosis:* This typically happens when `ffmpeg` fails to concatenate valid
    video segments, resulting in an empty video stream, and the `-shortest` flag
    cuts the output to the shortest stream (which is near zero).
  * *Cause:* `orchestrator_v3_no_face.py` likely failed to find valid B-Roll
    clips or generated "empty" clips due to codec issues.
* **API Usage:** User doubts usage of keys (Banana, Gemini 3.0).
  * *Verification:* Logs show `Gemini 2.0 Flash` being used. Code references
    `Banana.dev`, but fallback logic might be skipping it if the key is missing
    or invalid.

### 3. 📉 Crypto Bot (Hummingbot)

* **Status:** RUNNING but **Degraded**.
* **Issue:** MQTT Connection failures in logs. The bot cannot communicate with
  the dashboard/broker.
* **Impact:** Trading might work (headless), but monitoring is broken.

### 4. 🧹 System Hygiene

* **Host Clutter:** Duplicate `mail_processor.py` sequences found running natively
  on the host (`PID 1167871`, `1716518`).
* **Scheduler Conflict:** `factory_scheduler.py` is running on the HOST
  (`PID 1982458`). It should ONLY run inside the `content-factory` container.
  This causes double-scheduling and race conditions.

## 🛠 Restoration Plan (For Tomorrow)

### Phase 1: Deep Cleaning (The Purge)

1. **Kill ALL Host Python Processes:** Stop `mail_processor`, `factory_scheduler`,
   and any `telegram_bot` stragglers on `unified-home-core-cloud`.
2. **Verify K8s Volumes:** Adjust the deployment to mount the database to
   `/data/user_context.db` (Persistent Volume) so approvals survive restarts.
3. **Fix Permissions:** Ensure the mounted Google Credentials file is readable by
   the container user.

### Phase 2: Bot Resurrection

1. **Database Persistence:** Configure the bot to use the PVC.
2. **Auth Fix:** Direct mount verify. I will run `ls -la /app/config` inside
   the pod before starting the app.
3. **Single Truth:** Ensure ONLY the K8s pod runs the bot.

### Phase 3: Content Factory High-Fidelity Fix

1. **Debug Video Generation:** Run a *manual* generation command with verbose
   `ffmpeg` logging to catch the "1 second" glitch.
2. **Key Validation:** Create a script `validate_keys.py` that explicitly tests:
    * OpenRouter (Anthropic)
    * Google Gemini (GenAI / 3.0)
    * Banana.dev
    * YouTube API
    * *Output:* A clear "Pass/Fail" table for the user.

### Phase 4: Crypto Connectivity

1. **MQTT Fix:** Investigate the `mqtt-broker` container. If it's down or
   blocked, the bot can't report status. Restart the message broker.

---

## ✅ Progress Update — 2026-02-09 08:20

- **Host clutter purged:** Killed stray `mail_processor.py` on `unified-home-core-cloud`; only the K8s pod instance of `ai_telegram_bot_v2` remains.
- **Bot database pinned to PVC:** `.env` now uses `SQLITE_DB_PATH=/data/user_context.db`; `docker-compose.yml` mounts `bot-data` at `/data` so approvals survive restarts.
- **Gmail creds wired:** `docker-compose.yml` mounts `config/gmail_credentials.json` into the bot container (`/app/config/gmail_credentials.json`).
- **K8s bot healthy:** Pod `trading/ai-telegram-bot-54697db754-gwdcr` is Running with `DB_PATH=/app/data/user_context.db` and hostPath `/home/gonya/bot_data` (`user_context.db` present, 32 KB).
- **Content Factory status:** No K8s/Docker factory pods running yet—kept offline to avoid double-scheduling; start when ready to debug the 1‑second video issue.
- **Crypto bot note:** Hummingbot logs still complain about missing API keys and `.password_verification`; needs keys + password file to turn green.

### Next 3 actions to make the board fully green
1) **Verify bot DB persistence:** Tail `user_context.db` timestamps while approving a test user to confirm writes land on `/home/gonya/bot_data`.  
2) **Restart mail processor inside container only:** If needed, run via `docker-compose` or K8s Job; keep host clean.  
3) **Content Factory bring-up:** Deploy `infra/k8s/content-factory-deployment.yaml` (namespace `telegram-bot`) or start the docker-compose service, then run a manual render with verbose ffmpeg to reproduce the 1s issue.
