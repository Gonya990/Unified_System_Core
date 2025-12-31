<!-- markdownlint-disable MD013 -->
# Implementation Plan & User Stories

## Goal Description

Plan and implement a sophisticated Telegram Personal Assistant Bot that
integrates with Google Calendar, maintains long-term memory/context, actively
engages the user, and provides intelligent assistance for daily tasks and
business insights.

## User Review Required

> [!IMPORTANT]
> The bot requires Google Cloud Project credentials (OAuth 2.0 Client ID) for
> Calendar API access. The user must authorize the application.
>
> [!NOTE]
> Database selection for "Memory" and "Context" needs to be confirmed. SQLite
> is proposed for simplicity, or we can use a vector store if "digest insights"
> implies semantic search.

## User Stories

### 1. Onboarding & Authentication

- **ID**: US-001 (Beads: US-wkm)
- **As a** User
- **I want** to securely authenticate with the bot and link my Google Account
- **So that** the bot can access my calendar and key personal data.

### 2. Google Calendar Integration

- **ID**: US-002 (Beads: US-svk)
- **As a** User
- **I want** the bot to manage my calendar (view, add, edit events)
- **So that** I can schedule meetings and reminders directly from the chat.

### 3. Smart Event Management with Context

- **ID**: US-003 (Beads: US-o1w)
- **As a** User
- **I want** to add context to events (e.g., "Meeting with John regarding
  Project X")
- **So that** the bot remembers *why* the event exists and can brief me before
  it starts.

### 4. Proactive Assistant (Nudge & Alert)

- **ID**: US-004 (Beads: US-qrn)
- **As a** User
- **I want** the bot to check in on me if I haven't interacted for a few days
  ("Hi, let's resume working on X")
- **So that** I stay productive and don't lose track of ongoing tasks.

### 5. Insight & Memory Digestion

- **ID**: US-005 (Beads: US-yua)
- **As a** User
- **I want** the bot to remember chat history and "digest" key information
  (e.g., business facts, user preferences)
- **So that** it can answer open-ended questions like "What did we decide about
  X?" or "Draft an email based on my business context."

### 6. Quick Facts & Help

- **ID**: US-006 (Beads: US-0wl)
- **As a** User
- **I want** quick suggestions on what the assistant can help with
- **So that** I can discover its capabilities (e.g., "I know you have a
  business in [Domain], do you want to improve [Aspect]?").

### 7. Admin Service Management

- **ID**: US-007 (Beads: US-qh8)
- **As an** Admin
- **I want** to run and monitor the bot services via `docker-compose`
- **So that** deployment is consistent, isolated, and easy to restart.

### 8. Admin Key Management

- **ID**: US-008 (Beads: US-ns5)
- **As an** Admin
- **I want** to manage API keys (e.g., OpenAI, Google) directly via Telegram
  chat
- **So that** I can rotate or update credentials without SSH-ing into the
  server.

### 9. Admin User Management

- **ID**: US-009 (Beads: US-98n)
- **As an** Admin
- **I want** to authorize or ban users via Telegram commands
- **So that** I can control who accesses the bot without modifying config
  files and restarting.

### 10. Interactive UX

- **ID**: US-010 (Beads: US-t1r)
- **As a** User
- **I want** to use buttons and interactive menus instead of typing commands
- **So that** interactions are faster, error-free, and accessible on mobile.

## Use Cases

### UC-01: Connect Google Calendar (Onboarding & UX)

1. User sends `/start`.
2. Bot sends: "Welcome! Let's get started." with an **Inline Keyboard**:
   - `[ 🔗 Connect Calendar ]`
   - `[ ❓ Help ]`
3. User taps `[ Connect Calendar ]`.
4. Bot edits message to show auth link.
5. After auth, Bot sends **Persistent Reply Keyboard**:
   - `[ 📅 Today ]` `[ ➕ Add Event ]`
   - `[ 💡 Insights ]` `[ ⚙️ Settings ]`

### UC-02: Adding an Event with Context (Smart UX)

1. User: "Schedule a call with Sarah..."
2. Bot parses and replies with **Inline Confirmation Buttons**:
   - `[ ✅ Confirm: Call with Sarah @ 10AM ]`
   - `[ ✏️ Edit Context ]`
   - `[ ❌ Cancel ]`
3. User taps `[ ✅ Confirm ]`.
4. Bot creates event and edits message: "✅ Scheduled!"

### UC-05: Admin Key Management (Admin UX)

1. Admin clicks `[ 🔑 Admin Keys ]` from Admin Menu.
2. Bot displays keys with **Inline Buttons**:
   - `[ Update OPENAI_KEY ]`
   - `[ Update GOOGLE_ID ]`
3. Admin taps `[ Update OPENAI_KEY ]`.
4. Bot asks: "Send the new value for OPENAI_KEY."
5. Admin replies with key.
6. Bot confirms and deletes the key message for security.

## UX & UI Mechanisms

### 1. Choice Buttons (Inline Keyboards)

- Used for ephemeral actions (Confirm/Cancel, Select Option, Pagination).
- Trigger `CallbackQueryHandler` in the backend.
- Feedback: Buttons should show a "loading" state or update the message
  (EditMessageText) to prevent spamming.

### 2. Main Menu (Reply Keyboards)

- Persistent custom keyboard for high-frequency actions.
- Layout:
  - Row 1: `📅 Daily Brief` | `➕ New Task`
  - Row 2: `🧠 Memory/Context` | `❓ Help`
- Admin Mode: Adds `🛠 Admin Panel` row.

### 3. Responsiveness (Chat Actions)

- Bot must send `ChatAction.TYPING` while processing LLM requests.
- Bot must send `ChatAction.UPLOAD_PHOTO` when generating charts/images.

### 4. Menus

- Standard `/` command menu (set commands) for quick access to features like
  `/start`, `/clear_memory`, `/admin`.

### UC-03: Proactive Re-engagement

1. Bot's background job detects no user activity for 3 days.
2. Bot analyzes recent "Context" or open tasks.
3. Bot sends: "Hi! We haven't spoken in a while. Last time we were working on
   the Marketing Plan. Ready to resume? Or I can help you with your
   ["Business X"] optimization."

### UC-04: Daily Briefing

1. User: "What's on for today?"
2. Bot retrieves calendar events.
3. Bot enriches events with stored "Context".
4. Bot sends: "You have 3 events:
   - 10:00 AM: Call with Sarah (Context: Review budget for Q4)
   - ..."

### UC-05: Admin Key Management

1. Admin: `/admin keys`
2. Bot: "Current Keys:
   - OPENAI_API_KEY: sk-****
   - GOOGLE_CLIENT_ID: ****
   Reply with `/set_key [KEY_NAME] [VALUE]` to update."
3. Admin: `/set_key OPENAI_API_KEY sk-new-secret-key-123`
4. Bot updates `.env` or secure storage and reloads config.
5. Bot: "Key OPENAI_API_KEY updated successfully."

### UC-06: Admin User Management

1. Admin: `/admin users`
2. Bot lists users:
   - 123456789 (Approved) - @john_doe
   - 987654321 (Pending) - @unknown_user
3. Admin: `/approve 987654321` or `/ban 123456789`
4. Bot updates `user_context_db` and notifies relevant user.

## Proposed Architecture Logic

### Components

1. **Bot Frontend (Telegram)**: `ai_telegram_bot_v2.py` (enhanced).
2. **LLM Interface**: Existing Ollama integration for natural language
   understanding (parsing intent, generating summaries).
3. **Google Service**: Module to handle OAuth flow and Calendar API calls.
4. **Database (Knowledge Base)**:
    - `Users`: ID, Google Auth Token (encrypted/stored securely), Preferences.
    - `Events`: ID, CalendarEventID, ContextDescription, CreatedAt.
    - `ChatMemory`: Vector or Summarized text of past interactions.
5. **Scheduler**: Background thread/process to scan for upcoming events and
   "stale" users to nudge.

## Proposed Changes

### [Projects/AI_Core](file:///Users/macbook/Documents/Unified_System/Projects/AI_Core)

#### [MODIFY] [ai_telegram_bot_v2.py](file:///Users/macbook/Documents/Unified_System/Projects/AI_Core/src/ai_telegram_bot_v2.py)

- Refactor to support new command handlers.
- Add background scheduler for proactive messages.
- specific handlers for `/onboard`, `/calendar`.

#### [NEW] [user_context_db.py](file:///Users/macbook/Documents/Unified_System/Projects/AI_Core/src/user_context_db.py)

- SQLite or JSON-based simple database manager to store user state, auth tokens
  (safe handling), and event context.

#### [NEW] [daily_scheduler.py](file:///Users/macbook/Documents/Unified_System/Projects/AI_Core/src/daily_scheduler.py)

- Logic for "Nudge" and "Event Reminders".

## Verification Plan

### Manual Verification

1. **Onboarding**: Run bot, use `/start`, verifying Google Auth link generation.
2. **Calendar**: Ask bot to "Schedule test meeting", check real Google Calendar.
3. **Context**: Ask "What is the test meeting about?", verify bot recalls the
   context not just the title.
4. **Nudge**: Manually trigger the "check inactivity" function (or set threshold
   to 1 minute) and verify bot sends a re-engagement message.

## Project Orchestration & Lifecycle (Beads System)

This project is orchestrated using the **Beads** issue tracking system. Tasks
are organized into Epics and governed by a continuous Verification & Security
loop.

### 1. Epic Hierarchy

- **EPIC-UX (US-348)**: Onboarding, Interactive UI, and Help Systems.
- **EPIC-CORE (US-27a)**: AI Intelligence, Calendar Integration, and Scheduler.
- **EPIC-ADMIN (US-1tm)**: Service Management, Keys, and User Authorization.
- **EPIC-PROD (US-psm)**: Production Readiness, Security, and Testing.

### 2. Development & Security Loop

Every feature implementation must pass through the following loop before being
considered "Done":

1. **Drafting**: Task created in Beads.
2. **Implementation**: Code development in `Projects/AI_Core`.
3. **Security Review**: Check for credential safety (e.g., `SEC-001` / `US-psm.1`).
4. **Verification**: Automated and manual testing (e.g., `TEST-001` / `US-psm.2`).
5. **Audit**: Logged in Beads activity feed.

### 3. Orchestration Tasks

| Issue ID | Title | Description | Parent Epic |
|----------|-------|-------------|-------------|
| **US-psm.1** | Security Review: OAuth Token Encryption | Critical security check for production. | EPIC-PROD |
| **US-psm.2** | Integration Test Suite | Automated validation of the Auth/Calendar loop. | EPIC-PROD |
| **US-psm.3** | CI/CD Pipeline | Automated deployment for live prod testing. | EPIC-PROD |
| **US-27a.1** | Daily Briefing/Nudge Logic | Background orchestration of user engagement. | EPIC-CORE |
| **US-1tm.1** | Admin Dashboard in Telegram | Centralized menu for admin controls. | EPIC-ADMIN |

---

## Проектная оркестрация и жизненный цикл (система Beads)

Этот проект управляется с использованием системы отслеживания задач **Beads**.
Задачи организованы в эпики и регулируются непрерывным циклом проверки и
безопасности.

### 1. Иерархия эпиков

- **EPIC-UX (US-348)**: Онбординг, интерактивный интерфейс и справочные системы.
- **EPIC-CORE (US-27a)**: Интеллект ИИ, интеграция с Календарем и планировщик.
- **EPIC-ADMIN (US-1tm)**: Управление сервисами, ключами и авторизация
  пользователей.
- **EPIC-PROD (US-psm)**: Готовность к продакшену, безопасность и тестирование.

### 2. Цикл разработки и безопасности

Каждая реализация функции должна пройти через следующий цикл, прежде чем она
будет считаться «Готово»:

1. **Черновик**: Задача создана в Beads.
2. **Реализация**: Разработка кода в `Projects/AI_Core`.
3. **Проверка безопасности**: Проверка безопасности учетных данных (например,
   `US-psm.1`).
4. **Верификация**: Автоматическое и ручное тестирование (например, `US-psm.2`).
5. **Аудит**: Запись в ленте активности Beads.
