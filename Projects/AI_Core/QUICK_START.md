# Quick Start: Multi-Admin Bot Setup (US-5ik)

## What's New

You now have **two separate Telegram bot instances** running in parallel:
- **Igor's Bot** (FrostyMeadow agent)
- **Kostya's Bot** (OrangeStone agent)

Both share the same codebase but maintain separate:
- User databases (`user_context_igor.db`, `user_context_kostya.db`)
- Configuration (`.env.igor`, `.env.kostya`)
- Health/Dashboard ports (8095-8096 for Igor, 8097-8098 for Kostya)

## 1. Install PM2 (One-time)

```bash
npm install -g pm2
```

Or with Homebrew on macOS:
```bash
brew install pm2
```

## 2. Start Both Bots

### Using the Management Script (Easiest)

```bash
cd /Users/macbook/Documents/Unified_System/Projects/AI_Core
./scripts/manage-bots.sh start
```

### Or Manually with PM2

```bash
cd /Users/macbook/Documents/Unified_System/Projects/AI_Core
pm2 start ecosystem.config.js
```

## 3. Verify Both Are Running

```bash
./scripts/manage-bots.sh status
```

Or manually:
```bash
pm2 status
```

Expected output:
```
│ app name       │ id │ mode │ ↺ │ status  │ cpu │ memory      │
│ ai-bot-igor    │ 0  │ fork │ 0 │ online  │ 0%  │ 120M        │
│ ai-bot-kostya  │ 1  │ fork │ 0 │ online  │ 0%  │ 115M        │
```

## 4. Check Health

```bash
./scripts/manage-bots.sh health
```

Or manually:
```bash
curl http://localhost:8095/health  # Igor
curl http://localhost:8097/health  # Kostya
```

## 5. View Logs

```bash
./scripts/manage-bots.sh logs-igor   # Igor's logs
./scripts/manage-bots.sh logs-kostya # Kostya's logs
./scripts/manage-bots.sh monit       # Live dashboard
```

## File Structure

```
Projects/AI_Core/
├── .env.igor                    # Igor's config (ADMIN: 708531393)
├── .env.kostya                  # Kostya's config (ADMIN: 578363419)
├── ecosystem.config.js          # PM2 configuration
├── MULTI_ADMIN_SETUP.md         # Detailed setup guide
├── QUICK_START.md              # This file
├── user_context_igor.db        # Igor's user database
├── user_context_kostya.db      # Kostya's user database
├── logs/
│   ├── igor-out.log
│   ├── igor-error.log
│   ├── kostya-out.log
│   └── kostya-error.log
└── src/
    └── ai_telegram_bot_v2.py   # Shared bot code
```

## Management Commands

```bash
# Start/Stop
./scripts/manage-bots.sh start           # Start both
./scripts/manage-bots.sh stop            # Stop both
./scripts/manage-bots.sh restart         # Restart both

# Status
./scripts/manage-bots.sh status          # Show status
./scripts/manage-bots.sh health          # Health checks
./scripts/manage-bots.sh monit           # Live monitoring

# Logs
./scripts/manage-bots.sh logs            # Both bots (last 20 lines)
./scripts/manage-bots.sh logs-igor       # Igor only (last 50 lines)
./scripts/manage-bots.sh logs-kostya     # Kostya only (last 50 lines)

# Auto-startup
./scripts/manage-bots.sh setup-autostart # Enable auto-start on reboot
./scripts/manage-bots.sh cleanup         # Remove from PM2
```

## Access Points

### Igor's Bot
- **Telegram Bot**: Use token `YOUR_TELEGRAM_BOT_TOKEN`
- **Admin ID**: 708531393 (Igor)
- **Allowed Users**: Igor + Artur (5569219290)
- **Agent Mail**: `FrostyMeadow`
- **Health**: http://localhost:8095/health
- **Dashboard**: http://localhost:8096/dashboard
- **Database**: `user_context_igor.db`

### Kostya's Bot
- **Telegram Bot**: Use token `7998292224:AAGhXLtf-...`
- **Admin ID**: 578363419 (Kostya)
- **Allowed Users**: Kostya (+ Igor if enabled)
- **Agent Mail**: `OrangeStone`
- **Health**: http://localhost:8097/health
- **Dashboard**: http://localhost:8098/dashboard
- **Database**: `user_context_kostya.db`

## Troubleshooting

### PM2 not found
```bash
npm install -g pm2
```

### Ports already in use
Edit `.env.igor` and `.env.kostya` to use different HEALTH_PORT/DASHBOARD_PORT values.

### Bot won't start
```bash
pm2 logs ai-bot-igor --err
pm2 logs ai-bot-kostya --err
```

### Check shared resources
Both bots share:
- Agent Mail communication system
- TokenBroker (secrets management)
- Inference providers (Ollama, Gemini, OpenAI)
- Google Calendar integration

---

See [MULTI_ADMIN_SETUP.md](./MULTI_ADMIN_SETUP.md) for detailed documentation.
