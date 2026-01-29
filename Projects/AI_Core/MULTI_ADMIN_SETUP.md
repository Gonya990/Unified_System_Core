# Multi-Admin Bot Architecture

This document describes how to run separate Telegram bot instances for Igor and Kostya, both using the same Unified System codebase.

## Architecture Overview

```
┌─────────────────────────────────────────┐
│   Unified System Core (One Codebase)    │
└─────────────────────────────────────────┘
              ↓ ↓
      ┌───────┴─┴────────┐
      ↓                  ↓
┌─────────────┐  ┌─────────────┐
│ Igor's Bot  │  │ Kostya's Bot│
│ (.env.igor) │  │(.env.kostya)│
└─────────────┘  └─────────────┘
   PM2 app:1       PM2 app:2
   Token: 851...   Token: 799...
   Admin: 708...   Admin: 578...
```

## Configuration Files

### Igor's Instance (.env.igor)
- **BOT_INSTANCE**: `igor`
- **TELEGRAM_BOT_TOKEN**: `8518131338:AAH_mDgVZ2UclJvUVT0RI5uypeazSORx2Wk`
- **ADMIN_ID**: `708531393` (Igor)
- **ALLOWED_USERS**: `708531393,5569219290` (Igor + Artur)
- **HEALTH_PORT**: `8095`
- **DASHBOARD_PORT**: `8096`
- **AGENT_MAIL_NAME**: `FrostyMeadow`
- **SQLITE_DB_PATH**: `user_context_igor.db`

### Kostya's Instance (.env.kostya)
- **BOT_INSTANCE**: `kostya`
- **TELEGRAM_BOT_TOKEN**: `7998292224:AAGhXLtf-LAcRdJqFK4rn1vvOoZTgWcrCJA`
- **ADMIN_ID**: `578363419` (Kostya)
- **ALLOWED_USERS**: `578363419` (Kostya + collaborators)
- **HEALTH_PORT**: `8097`
- **DASHBOARD_PORT**: `8098`
- **AGENT_MAIL_NAME**: `OrangeStone`
- **SQLITE_DB_PATH**: `user_context_kostya.db`

## Running Both Bots

### Option 1: PM2 (Recommended for Production)

#### Prerequisites
```bash
npm install -g pm2
```

#### Start Both Bots
```bash
cd /Users/macbook/Documents/Unified_System/Projects/AI_Core
pm2 start ecosystem.config.js
```

#### Check Status
```bash
pm2 status          # List all processes
pm2 logs            # View all logs
pm2 logs ai-bot-igor
pm2 logs ai-bot-kostya
```

#### Stop/Restart
```bash
pm2 stop all        # Stop all bots
pm2 restart all     # Restart all bots
pm2 delete all      # Remove from PM2
```

#### Enable Auto-restart on Boot
```bash
pm2 startup
pm2 save
```

### Option 2: Manual Command Line (Development)

#### Terminal 1 - Igor's Bot
```bash
cd /Users/macbook/Documents/Unified_System/Projects/AI_Core
python3 src/ai_telegram_bot_v2.py --env .env.igor
```

#### Terminal 2 - Kostya's Bot
```bash
cd /Users/macbook/Documents/Unified_System/Projects/AI_Core
python3 src/ai_telegram_bot_v2.py --env .env.kostya
```

## Health Checks

Each bot exposes its own health port:

- **Igor's bot**: `http://localhost:8095/health`
- **Kostya's bot**: `http://localhost:8097/health`

Or dashboard:
- **Igor's bot**: `http://localhost:8096/dashboard`
- **Kostya's bot**: `http://localhost:8098/dashboard`

## Database Isolation

Each bot maintains its own SQLite database:
- Igor: `user_context_igor.db` - User roles, context, permissions
- Kostya: `user_context_kostya.db` - User roles, context, permissions

No data is shared between instances by default (independent user contexts).

## Shared Resources

Both bots share access to:
- Agent Mail system (for A2A communication)
- TokenBroker (for secret management)
- Calendar service (Google OAuth, stored centrally)
- Inference providers (Ollama, Gemini, OpenAI, etc.)

## Troubleshooting

### Bot Won't Start with PM2
```bash
# Check PM2 logs
pm2 logs ai-bot-igor --err

# Verify Python path
python3 --version

# Check .env file exists
ls -la /Users/macbook/Documents/Unified_System/Projects/AI_Core/.env.igor
```

### Port Conflicts
If health/dashboard ports are in use:
1. Edit `.env.igor` and `.env.kostya` to use different ports
2. Update `ecosystem.config.js` accordingly
3. Restart PM2

### Token Validation Issues
Each token must be valid and correspond to active @BotFather registrations:
- Igor's token: registered with @BotFather
- Kostya's token: registered with @BotFather separately

Verify tokens:
```bash
curl -s https://api.telegram.org/bot8518131338:AAH_mDgVZ2UclJvUVT0RI5uypeazSORx2Wk/getMe | jq .
```

## Monitoring

### Real-time Logs
```bash
pm2 monit              # Live monitoring dashboard
pm2 logs -f            # Follow logs in real-time
```

### System Integration
Both instances report health to the Unified System via Agent Mail:
- Igor's bot → FrostyMeadow agent
- Kostya's bot → OrangeStone agent

Check agent mailbox:
```bash
python3 Scripts/Orchestration/agent_mail_client.py inbox --agent FrostyMeadow
python3 Scripts/Orchestration/agent_mail_client.py inbox --agent OrangeStone
```

## Migration from Single Bot

If migrating from a single bot:

1. Backup existing `user_context.db`:
   ```bash
   cp user_context.db user_context_backup.db
   ```

2. Copy existing data to Igor's instance:
   ```bash
   cp user_context_backup.db user_context_igor.db
   ```

3. Start fresh for Kostya (or restore from backup if needed):
   ```bash
   # Kostya starts with empty DB
   # Users can re-authenticate as needed
   ```

4. Test both instances independently

5. Update any external references to the bot from single to dual-bot setup
