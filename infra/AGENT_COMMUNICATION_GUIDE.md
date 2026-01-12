# Agent Communication Guide

## Overview

This document defines how agents communicate within the Unified System. All agents use a centralized hub for coordination, with optional Telegram alerts for human operators.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    COMMUNICATION LAYERS                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐     MCP Mail      ┌──────────┐                │
│  │  Agent A │◄────────────────►│  Agent B │                │
│  └────┬─────┘                   └────┬─────┘                │
│       │                              │                       │
│       ▼                              ▼                       │
│  ┌─────────────────────────────────────────┐                │
│  │           MCP Mail Hub                   │                │
│  │        igor-gaming-1:8765                │                │
│  │                                          │                │
│  │  • Message storage                       │                │
│  │  • Agent registry                        │                │
│  │  • Thread management                     │                │
│  │  • File reservations                     │                │
│  └─────────────────────────────────────────┘                │
│                                                              │
│  ┌──────────┐     Telegram      ┌──────────┐                │
│  │Processor │────────────────►│  Human   │                │
│  └──────────┘    (alerts)       └──────────┘                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Agent Registry

### Active Agents

| Agent | Program | Model | Host | Owner | Role |
|-------|---------|-------|------|-------|------|
| **VioletCastle** | claude-code | opus-4.5 | kosta-laptop | Kosta | Primary dev agent |
| **OrangeStone** | antigravity-core | gemini | igor-macbook | Igor (Bot) | Factory scheduler |
| **PinkLake** | llm-council | gemini | igor-macbook | Igor (Bot) | Swarm coordinator |
| **FuchsiaCat** | llm-council | gemini | igor-macbook | Igor (Bot) | Council member |
| **AmberOwl** | mail-processor | - | server | System | Inbox monitor |

### Agent Naming Convention

Names follow `AdjectiveNoun` pattern (e.g., VioletCastle, PinkLake, OrangeStone).

## Communication Platforms

### 1. MCP Agent Mail (Agent-to-Agent)

Primary communication channel for all agent coordination.

**Access Methods:**

| Method | When to Use |
|--------|-------------|
| MCP Tools | During AI sessions (Claude, Gemini) |
| CLI (`agent_mail_client.py`) | Scripts, cron jobs, manual checks |

**CLI Commands:**

```bash
# Source environment first
set -a && source .env && set +a

# Check inbox
python3 Scripts/Orchestration/agent_mail_client.py inbox --limit 10

# Read specific message
python3 Scripts/Orchestration/agent_mail_client.py read --id <message_id>

# Send message
python3 Scripts/Orchestration/agent_mail_client.py send \
  --to PinkLake \
  --to OrangeStone \
  --subject "Status Update" \
  --body "Your message here"

# List online agents
python3 Scripts/Orchestration/agent_mail_client.py agents

# Register/refresh presence
python3 Scripts/Orchestration/agent_mail_client.py register

# Health check
python3 Scripts/Orchestration/agent_mail_client.py health
```

**Message Importance Levels:**

| Level | Use Case | Triggers Alert |
|-------|----------|----------------|
| `low` | FYI, status updates | No |
| `normal` | Standard coordination | No |
| `high` | Needs attention soon | Yes |
| `urgent` | Immediate action required | Yes |
| `critical` | System emergency | Yes |

**Alert Keywords (trigger Telegram):**
- urgent, critical, emergency, blocker, breaking
- action required, needs immediate, asap

### 2. Telegram (Human Notification)

Push notifications to human operators when agents need attention.

**How It Works:**
1. Mail Processor runs as systemd service
2. Polls agent inbox every 60 seconds
3. Detects urgent/important messages
4. Sends Telegram alert to configured chat

**Setup Requirements:**

```bash
# In .env
TELEGRAM_BOT_TOKEN=<from @BotFather>
TELEGRAM_ADMIN_CHAT_ID=<your chat ID>
```

**Getting Your Chat ID:**
1. Message @userinfobot on Telegram
2. Or send message to your bot, then:
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/getUpdates" | jq '.result[-1].message.chat.id'
   ```

**Service Management:**

```bash
# Start/stop
systemctl --user start mail-processor
systemctl --user stop mail-processor

# Check status
systemctl --user status mail-processor

# View logs
journalctl --user -u mail-processor -f

# Test alert
source .env && python3 Scripts/Orchestration/mail_processor.py --test-alert
```

## Communication Protocols

### Starting Work

1. Register agent presence
2. Check inbox for pending messages
3. Check file reservations before editing shared files
4. Broadcast intent if working on shared components

```bash
# Full startup sequence
python3 Scripts/Orchestration/agent_mail_client.py register
python3 Scripts/Orchestration/agent_mail_client.py inbox
```

### Coordinating with Other Agents

**Request Help:**
```bash
python3 Scripts/Orchestration/agent_mail_client.py send \
  --to PinkLake \
  --subject "[bd-123] Need assistance with Factory module" \
  --body "Working on task bd-123. Need help with X. Can you look into Y?"
```

**Broadcast Status:**
```bash
python3 Scripts/Orchestration/agent_mail_client.py send \
  --to PinkLake \
  --to OrangeStone \
  --subject "Status: Completed TokenBroker refactor" \
  --body "Pushed changes to main. Please pull and verify."
```

**Handoff Work:**
```bash
python3 Scripts/Orchestration/agent_mail_client.py send \
  --to OrangeStone \
  --subject "[HANDOFF] Continue Factory scheduler work" \
  --body "Completed Phase 1. Phase 2 ready for pickup. See bd-456."
```

### File Reservations (Conflict Prevention)

Before editing shared files, reserve them:

```python
# Via MCP tools
mcp__mcp-agent-mail__file_reservation_paths(
  project_key="/home/gonya/Unified_System",
  agent_name="VioletCastle",
  paths=["Scripts/Orchestration/mail_processor.py"],
  exclusive=True,
  ttl_seconds=3600,
  reason="bd-123: Refactoring mail processor"
)
```

### Escalation Path

| Situation | Action |
|-----------|--------|
| Agent unresponsive | Wait 30min, then notify human via Telegram |
| Conflicting changes | Use file reservations, coordinate via mail |
| Blocker found | Mark message as `urgent`, include `blocker` keyword |
| System emergency | Use `critical` importance, all caps subject |

## Best Practices

### DO:
- Register presence at session start
- Check inbox before starting work
- Use descriptive subjects with ticket refs `[bd-123]`
- Reserve files before extended edits
- Broadcast completion of shared component work

### DON'T:
- Send messages without registering first
- Ignore urgent messages from other agents
- Edit reserved files without coordination
- Use urgent/critical for non-urgent matters
- Assume other agents received your message (check for ACK if needed)

## Troubleshooting

| Error | Solution |
|-------|----------|
| `from_agent not registered` | Run `register` command first |
| `FILE_RESERVATION_CONFLICT` | Wait for expiry or coordinate with holder |
| `Agent not found` | Check spelling (AdjectiveNoun format) |
| No Telegram alerts | Check `TELEGRAM_*` vars in `.env`, restart service |
| Messages not appearing | Verify hub connectivity: `agent_mail_client.py health` |

## Configuration Reference

**.env variables:**

```bash
# Agent identity
AGENT_MAIL_NAME=VioletCastle
AGENT_MAIL_PROGRAM=claude-code
AGENT_MAIL_MODEL=opus-4.5
AGENT_MAIL_PROJECT=/home/gonya/Unified_System
AGENT_MAIL_SERVER=http://100.110.209.49:8765

# Telegram alerts (optional)
TELEGRAM_BOT_TOKEN=<bot token>
TELEGRAM_ADMIN_CHAT_ID=<chat id>
```

## Related Documentation

- [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) - System integration details
- [OPS_RUNBOOK.md](./OPS_RUNBOOK.md) - Operational procedures
- [CENTRAL_HUB_STATUS.md](./CENTRAL_HUB_STATUS.md) - Hub status and health
