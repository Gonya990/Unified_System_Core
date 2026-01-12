# Central Hub Integration Guide

## Overview

The Unified System now features a **Centralized Communication Hub** running on `igor-gaming-1`, enabling seamless agent-to-agent coordination and task management using the MCP Agent Mail protocol.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   igor-gaming-1                          │
│            (Centralized Coordination Hub)                │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  MCP Agent Mail Server (Port 8765)                │  │
│  │  - Project: /main                                 │  │
│  │  - Database: SQLite                               │  │
│  │  - Auth: Bearer Token                             │  │
│  └───────────────────────────────────────────────────┘  │
│                          │                               │
└──────────────────────────┼───────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐    ┌────▼─────┐    ┌────▼──────┐
    │ MacBook   │    │ Windows  │    │ Other     │
    │ (Local)   │    │ AI Host  │    │ Agents    │
    │           │    │          │    │           │
    │ Scripts:  │    │          │    │           │
    │ - agent_  │    │          │    │           │
    │   comm.sh │    │          │    │           │
    │ - mission_│    │          │    │           │
    │   sync.sh │    │          │    │           │
    └───────────┘    └──────────┘    └───────────┘
```

## Components

### 1. Central Hub (igor-gaming-1)

**Location:** `100.88.65.71:8765`  
**Protocol:** MCP JSON-RPC over HTTP  
**Authentication:** Bearer token (`antigravity_secret`)

#### Services

- **MCP Agent Mail Server** - Message routing and delivery
- **SQLite Database** - Message and agent data persistence  
- **Docker Compose** - Container orchestration

### 2. Local Scripts

#### `agent_comm.sh` - Direct Communication

Basic agent-to-agent messaging wrapper.

**Commands:**

```bash
# Check agent identity
./Scripts/External/agent_comm.sh whoami

# Send a message
./Scripts/External/agent_comm.sh send <recipient> "Your message"

# Check inbox
./Scripts/External/agent_comm.sh inbox
```

**Features:**

- ✅ Dynamic agent registration (auto-generated names)
- ✅ Cached agent identity
- ✅ HTTP/1.1 compatibility for MacBook
- ✅ JSON-RPC protocol

#### `mission_sync.sh` - Task Coordination

Enhanced task management and coordination.

**Commands:**

```bash
# Show mission status
./Scripts/External/mission_sync.sh status

# List available tasks
./Scripts/External/mission_sync.sh list

# Claim a task
./Scripts/External/mission_sync.sh claim <task_id>

# Mark task as complete
./Scripts/External/mission_sync.sh complete <task_id>
```

**Features:**

- ✅ Task assignment tracking
- ✅ Inbox monitoring
- ✅ Acknowledgement alerts
- ✅ Color-coded output

## Agent Registration

### Automatic (Recommended)

The scripts automatically register agents on first use with randomly generated names that follow the MCP naming convention (Adjective+Noun format).

Example agent names:

- `GreenPond`
- `BlueBear`
- `OrangeLake`

### Manual Registration

```bash
curl -sS --http1.1 -X POST "http://100.88.65.71:8765/mcp" \
  -H "Authorization: Bearer antigravity_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":"1",
    "method":"tools/call",
    "params": {
      "name":"register_agent",
      "arguments": {
        "project_key":"/main",
        "program":"my-agent",
        "model":"my-model-v1"
      }
    }
  }'
```

## Message Flow

### 1. Sending a Message

```bash
./Scripts/External/agent_comm.sh send PurpleBear "Hello from automation!"
```

**Flow:**

1. Script retrieves cached agent name (e.g., `GreenPond`)
2. Calls `send_message` MCP tool
3. Hub validates sender and recipient
4. Message delivered to recipient's inbox
5. Contact request automatically sent if first contact

### 2. Task Coordination

```bash
# Task Coordinator sends task
OrangeLake → [TASK] Deploy Documentation → GreenPond

# Agent claims task
./Scripts/External/mission_sync.sh claim task-001
→ Send [CLAIM] message

# Agent completes task
./Scripts/External/mission_sync.sh complete task-001
→ Send [COMPLETE] message with ACK required
```

## API Reference

### Available MCP Tools

- `ensure_project` - Create or verify project exists
- `register_agent` - Register new agent identity
- `send_message` - Send message to recipients
- `fetch_inbox` - Retrieve messages
- `acknowledge_message` - Acknowledge received message
- `reply_message` - Reply in thread
- `search_messages` - Search message history
- `whois` - Get agent information
- `request_contact` - Request contact with agent
- `respond_contact` - Accept/reject contact request

### Message Structure

```json
{
  "project_key": "/main",
  "sender_name": "GreenPond",
  "to": ["PurpleBear"],
  "subject": "Task Update",
  "body_md": "Markdown formatted message",
  "importance": "normal|high|urgent",
  "ack_required": false,
  "cc": [],
  "bcc": []
}
```

## Configuration

### Environment Variables

```bash
# Hub connection
HUB_URL="http://100.88.65.71:8765/mcp"
AUTH_TOKEN="antigravity_secret"
PROJECT_KEY="/main"

# Local cache
AGENT_STATE_FILE="$HOME/.cache/agent_comm_state"
```

### Deployment Configuration

Located in: `infra/setup_central_hub.sh`

**Key settings:**

- Python: 3.12
- Database: SQLite (`/opt/mcp-agent-mail/data/agent_mail.db`)
- Rate limiting: Disabled
- RBAC: Disabled

## Security

### Network Security

- ✅ All communication over Tailscale VPN
- ✅ Bearer token authentication required
- ✅ No public internet exposure

### Authentication

Each request must include:

```
Authorization: Bearer antigravity_secret
```

### Agent Identity

- Agent names cached locally in `~/.cache/agent_comm_state`
- Names follow MCP convention: `<Adjective><Noun>`
- Names are unique per project

## Troubleshooting

### Common Issues

#### 1. Agent Not Registered

**Error:** `Agent not registered. Run 'agent_comm.sh whoami' first.`

**Solution:**

```bash
./Scripts/External/agent_comm.sh whoami
```

This will register and cache your agent name.

#### 2. Connection Refused

**Error:** `Connection reset by peer`

**Check:**

```bash
# Verify hub is running
ssh igor-gaming-1 "docker ps | grep acfs-hub"

# Check hub logs
ssh igor-gaming-1 "docker logs acfs-hub-server-1"
```

#### 3. Recipient Not Found

**Error:** `Agent 'SomeAgent' not found`

**Solution:** Ensure recipient is registered:

```bash
# From recipient machine
./Scripts/External/agent_comm.sh whoami
```

### Debugging

#### View Hub Logs

```bash
ssh igor-gaming-1 "docker logs acfs-hub-server-1 | tail -n 50"
```

#### List All Agents

```bash
ssh igor-gaming-1 "docker exec acfs-hub-server-1 python -m mcp_agent_mail.cli list-projects"
```

#### Manual API Test

```bash
curl -v --http1.1 \
  -H "Authorization: Bearer antigravity_secret" \
  http://100.88.65.71:8765/health/liveness
```

## Usage Examples

### Example 1: Send Update to Team

```bash
./Scripts/External/agent_comm.sh send PurpleBear \
  "Deployment complete! Central Hub is operational at 100.88.65.71:8765"
```

### Example 2: Check Task Status

```bash
# View all active tasks
./Scripts/External/mission_sync.sh list

# Check inbox and pending items
./Scripts/External/mission_sync.sh status
```

### Example 3: Complete Task Workflow

```bash
# 1. List available tasks
./Scripts/External/mission_sync.sh list

# 2. Claim a task
./Scripts/External/mission_sync.sh claim deployment-123

# 3. Do the work...

# 4. Mark complete
./Scripts/External/mission_sync.sh complete deployment-123
```

## Performance & Limits

### Message Limits

- Inbox fetch: 20 messages per query (configurable)
- No hard limit on message size
- Attachments supported via file reservations

### Database

- SQLite for simplicity and portability
- Automatic WAL mode for concurrent access
- Regular backups recommended

## Future Enhancements

🔄 Planned:

- [ ] beads integration for task tracking
- [ ] Web UI for message browsing  
- [ ] File reservation system integration
- [ ] Multi-project support
- [ ] Message threading UI

## Mail Processor (Systemd)

The `Mail Processor` (`Scripts/Orchestration/mail_processor.py`) is the background service that polls the billboard inbox and performs automation (mark-read, auto-ack for `ack_required`, Telegram alerts for high-priority messages when configured).

### Non-blocking preflight (no systemd changes)

Run a single poll cycle to validate `.env` rehydration and server connectivity:

```bash
devenv shell -- bash -c 'python3 Scripts/Orchestration/mail_processor.py --once'
```

Expected:
- `Mail server not available` should not appear
- If inbox is empty, it exits cleanly

### User service (no sudo)

Use this when you cannot (or do not want to) use `sudo`.

1. Install the unit:

```bash
mkdir -p ~/.config/systemd/user
cp infra/mail-processor.user.service ~/.config/systemd/user/mail-processor.service
# NixOS note: the unit uses /run/current-system/sw/bin/bash + /run/current-system/sw/bin/devenv
systemctl --user daemon-reload
```

2. Start/enable:

```bash
systemctl --user enable --now mail-processor.service
```

3. Verify:

```bash
systemctl --user status mail-processor.service
journalctl --user -u mail-processor.service -n 200 --no-pager
```

### System service (requires sudo)

Use this when deploying centrally on a server.

1. Install the unit:

```bash
sudo cp infra/mail-processor.service /etc/systemd/system/mail-processor.service
# NixOS note: the unit uses /run/current-system/sw/bin/bash + /run/current-system/sw/bin/devenv
sudo systemctl daemon-reload
```

2. Start/enable:

```bash
sudo systemctl enable --now mail-processor.service
```

3. Verify:

```bash
sudo systemctl status mail-processor.service
sudo journalctl -u mail-processor.service -n 200 --no-pager
```

### Notes

- The processor reads `.env` from the repo root; ensure `AGENT_MAIL_SERVER`, `AGENT_MAIL_PROJECT`, and `AGENT_MAIL_NAME` match the billboard.
- Telegram alerts require `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ADMIN_CHAT_ID`.

## Support & Maintenance

### Restart Hub

```bash
ssh igor-gaming-1 "cd acfs-hub && docker compose restart server"
```

### Update Hub

```bash
ssh igor-gaming-1 "cd Unified_System_Core && git pull && bash infra/setup_central_hub.sh 'antigravity_secret'"
```

### View Status

```bash
ssh igor-gaming-1 "docker exec acfs-hub-server-1 python -m mcp_agent_mail.cli list-projects"
```

---

**Last Updated:** 2025-12-25  
**Status:** ✅ Production Ready  
**Version:** 1.0.0
