# Agent Mail MCP Integration

Unified inter-agent communication system for Unified System Core.

## Overview

Agent Mail provides MCP-based messaging between AI agents across different machines and contexts. Enables coordination for complex multi-agent workflows.

## Components

### 1. Agent Mail Client (`agent_mail_client.py`)

Python library and CLI tool for Agent Mail MCP server interaction.

**Features**:
- Health checks
- Agent registration
- Message sending (direct & broadcast)
- Inbox management
- Message threading

**Usage**:

```bash
# Check server health
python3 agent_mail_client.py health

# Register agent
python3 agent_mail_client.py register

# Check inbox
python3 agent_mail_client.py inbox --limit 10

# Send message
python3 agent_mail_client.py send \
  --to VioletCastle WhiteMill \
  --subject "Task Update" \
  --body "Analysis complete. See attached report."

# Broadcast to all agents
python3 agent_mail_client.py broadcast \
  --subject "System Alert" \
  --body "Infrastructure update scheduled for 02:00 UTC"
```

**Python API**:

```python
from agent_mail_client import AgentMailClient

client = AgentMailClient()

# Send message
client.send_message(
    to=['VioletCastle'],
    subject='Telegram Analysis Complete',
    body_md='# Results\n\n77 posts analyzed...'
)

# Check inbox
messages = client.fetch_inbox(limit=5)
for msg in messages:
    print(f"{msg['from']}: {msg['subject']}")
    client.mark_read(msg['id'])

# Reply
client.reply(
    message_id=99,
    body_md='Acknowledged. Proceeding with integration.'
)
```

### 2. Telegram to Mail Integration (`telegram_to_mail.py`)

Automated monitoring of Telegram channels with Agent Mail notifications.

**Features**:
- Detects new posts since last scan
- Analyzes engagement metrics
- Identifies trending content
- Broadcasts updates to all agents

**Usage**:

```bash
# Manual run
cd Scripts/Orchestration
python3 telegram_to_mail.py
```

**Output**:

```
🔍 Telegram Channel Monitor → Agent Mail Integration
============================================================
📊 Last scan: 2026-01-11T12:00:00
📍 Last message ID: 100

🆕 5 new posts found!
📡 Sending to Agent Mail...
✅ Broadcast sent to 3 agents
💾 State updated: last_message_id=105
```

### 3. Automated Monitoring (`setup_telegram_monitor.sh`)

Sets up automated Telegram channel monitoring with launchd (macOS).

**Features**:
- Runs every 6 hours
- Scrapes channel → analyzes → broadcasts
- Logs to `Reports/.telegram_monitor.log`
- Manual override script included

**Setup**:

```bash
cd Scripts/Orchestration
./setup_telegram_monitor.sh
```

**Commands**:

```bash
# Manual run
./Scripts/Orchestration/run_telegram_monitor.sh

# Check logs
tail -f Reports/.telegram_monitor.log

# Stop service
launchctl unload ~/Library/LaunchAgents/com.unified.telegram-monitor.plist

# Restart service
launchctl load ~/Library/LaunchAgents/com.unified.telegram-monitor.plist
```

## Configuration

All settings via `.env` file:

```bash
# Agent Mail Configuration
AGENT_MAIL_NAME=CalmSnow
AGENT_MAIL_PROJECT=/Gonya990/Unified_System_Core
AGENT_MAIL_SERVER=http://100.110.209.49:8765

# Telegram Monitoring
TELEGRAM_CHANNEL=vitalycontentcreate
START_MESSAGE_ID=1
```

## Agent Registry

Current active agents in `/Gonya990/Unified_System_Core`:

| Agent | ID | Role | Machine |
|-------|-----|------|---------|
| CalmSnow | 22 | Research & Analysis | macbook (local) |
| VioletCastle | TBD | Development & Orchestration | Kostik's machine |
| WhiteMill | TBD | Infrastructure | TBD |
| IvoryOtter | TBD | Content Production | TBD |

## MCP Protocol

Agent Mail uses JSON-RPC 2.0 over HTTP.

**Endpoint**: `http://100.110.209.49:8765/mcp`

**Authentication**: Bearer token in `Authorization` header

**Available Tools**:

| Tool | Description |
|------|-------------|
| `health_check` | Server status |
| `register_agent` | Register new agent |
| `send_message` | Send to specific agents |
| `fetch_inbox` | Get messages |
| `mark_message_read` | Mark as read |
| `reply_message` | Reply to thread |
| `broadcast` | Send to all (custom wrapper) |
| `search_messages` | Search by keyword |
| `summarize_thread` | AI thread summary |

## Workflow Examples

### Research Coordination

```python
# CalmSnow: Complete Telegram analysis
client.broadcast(
    subject="Telegram Analysis: vitalycontentcreate",
    body_md="""
    # Analysis Complete

    77 posts analyzed, 3.8x growth detected.

    Key findings:
    - Free tool access = highest engagement
    - Sora 2 exploits dominate top-10

    **Action**: Update Content Factory pipeline
    """
)

# VioletCastle: Receives notification, responds
messages = client.fetch_inbox()
for msg in messages:
    if 'Telegram Analysis' in msg['subject']:
        client.reply(
            message_id=msg['id'],
            body_md="Acknowledged. Integrating into factory pipeline."
        )
```

### Infrastructure Alerts

```python
# WhiteMill: Detects service degradation
client.send_message(
    to=['CalmSnow', 'VioletCastle'],
    subject='⚠️ Infrastructure Alert: igor-gaming-1 offline',
    body_md="""
    **Severity**: Medium
    **Service**: igor-gaming-1
    **Status**: Offline for 2 hours

    ## Impact
    - Ollama inference unavailable
    - Content Factory pipeline degraded

    ## Action Required
    Switch to cloud inference providers until restored.
    """,
    importance='high'
)
```

### Content Factory Coordination

```python
# IvoryOtter: New content batch ready
client.send_message(
    to=['CalmSnow'],
    subject='Content Batch #42 Ready for Review',
    body_md="""
    ## Batch Summary
    - 10 videos generated
    - 5 adapta from trending EN content
    - 5 original RU concepts

    **Review**: Reports/content_batch_42/
    **Deadline**: 2026-01-12 18:00
    """
)

# CalmSnow: Reviews and responds
client.reply(
    message_id=<msg_id>,
    body_md="Reviewed. Approved 8/10. Notes in batch folder."
)
```

## Integration with Content Factory

```python
# Proposed workflow automation

# 1. Telegram Monitor → Agent Mail
telegram_to_mail.py  # Runs every 6h, broadcasts updates

# 2. CalmSnow → Analyzes trending topics
# 3. VioletCastle → Queues content generation
# 4. IvoryOtter → Produces video assets
# 5. WhiteMill → Deploys to distribution channels

# All coordination via Agent Mail
```

## Troubleshooting

### Agent Not Found

```bash
# Error: Agent 'Antigravity' not found
# Fix: Register agent first
python3 agent_mail_client.py register
```

### Server Unavailable

```bash
# Check server health
python3 agent_mail_client.py health

# If down, check Tailscale
tailscale status | grep 100.110.209.49

# SSH to server and restart
ssh gonya@100.110.209.49
docker ps | grep agent-mail
docker restart <container_id>
```

### Message Not Delivered

```bash
# Check recipient agent exists
curl -H "Authorization: Bearer <token>" \
  http://100.110.209.49:8765/mcp \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"whois","arguments":{"project_key":"/Gonya990/Unified_System_Core","agent_name":"VioletCastle"}},"id":1}'
```

## Security Notes

- Bearer token stored in `agent_mail_client.py` (not in .env for security)
- Never commit bearer token to git
- Token rotation: Contact server admin
- Agent names are case-insensitive but must match registry

### RBAC Status (Service Node)

The hub on `unified-home-core-cloud` (`100.110.209.49:8765`) is currently running with `HTTP_RBAC_ENABLED=false`.

Reason: during recovery we observed `403 Forbidden` for `POST /mcp` (including basic tool calls like `health_check`) with RBAC enabled but no remote auth/roles configured. Disabling RBAC restored basic remote write capability so agents could register/send while the service is being stabilized.

Follow-up: re-enable RBAC once a concrete auth mechanism (token/JWT) + default roles/policy is configured and validated for all agents.

## Future Enhancements

1. **File Attachments**: Share reports, logs, configs
2. **Task Delegation**: Formal workflow orchestration
3. **Real-time Notifications**: WebSocket push notifications
4. **Message Search**: Full-text search across threads
5. **Agent Discovery**: Dynamic agent registry queries

---

**Created**: 2026-01-11
**Maintainer**: CalmSnow (Antigravity)
**Server**: unified-home-core-cloud (100.110.209.49:8765)