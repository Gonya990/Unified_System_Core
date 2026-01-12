# Central Hub Deployment Status

## ✅ Deployment Complete

**Date:** 2025-01-12 (Updated)  
**Location:** unified-home-core-cloud (100.110.209.49)  
**Status:** Operational

## Configuration

### Hub Details

- **URL:** `http://100.110.209.49:8765/mcp`
- **Auth Token:** See `.env` file
- **Database:** SQLite (`/opt/mcp-agent-mail/data/agent_mail.db`)
- **Storage:** `/opt/mcp-agent-mail/data/mailbox`

### Project

- **Key:** `/main`
- **Slug:** `main`
- **Created:** 2025-12-25T15:41:01

### Technical Stack

- **Python:** 3.12 (downgraded from 3.14 for compatibility)
- **Database:** SQLite with aiosqlite driver
- **Framework:** FastAPI + SQLAlchemy
- **Deployment:** Docker Compose

## Features Enabled

✅ Agent registration with auto-generated names  
✅ Message sending and delivery  
✅ Inbox querying  
✅ Bearer token authentication  
✅ Rate limiting disabled (for agent coordination)  
✅ RBAC disabled (for agent coordination)  

## Registered Agents

| Agent | Program | Model | Registered |
|-------|---------|-------|-----------|
| BlueBear | antigravity | gemini-2.5-flash | 2025-12-25T16:02:24 |
| PurpleBear | human | human-v1 | 2025-12-25T16:02:39 |
| GreenPond | antigravity | gemini-2.5-flash | Active (local) |

## Usage

### Local Script

```bash
# Check agent identity
./Scripts/External/agent_comm.sh whoami

# Send a message
./Scripts/External/agent_comm.sh send <recipient> "message text"

# Check inbox
./Scripts/External/agent_comm.sh inbox
```

### Direct API Calls

```bash
# List projects
curl -H "Authorization: Bearer antigravity_secret" \
  http://100.88.65.71:8765/health/liveness

# Via MCP JSON-RPC
curl -H "Authorization: Bearer antigravity_secret" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}' \
  http://100.88.65.71:8765/mcp
```

## Deployment Script

Located at: `infra/setup_central_hub.sh`

### Key Changes from Initial Deployment

1. **Python Version:** Downgraded to 3.12 for asyncpg compatibility
2. **Database:** Switched from PostgreSQL to SQLite for simplicity
3. **Docker Cleanup:** Removed redundant dockerfile blocks
4. **Path Configuration:** Fixed data directory permissions
5. **Security:** Disabled rate limiting and RBAC for agent coordination

## Issues Resolved

### 1. ModuleNotFoundError

- **Issue:** `mcp_agent_mail` module not found
- **Resolution:** Fixed sed pattern to replace all Python 3.14 references

### 2. AsyncIO Loop Conflicts

- **Issue:** `RuntimeError: Task attached to a different loop`
- **Resolution:** Switched from PostgreSQL+asyncpg to SQLite+aiosqlite

### 3. Database Permission Errors

- **Issue:** `unable to open database file`
- **Resolution:** Created data directories in Dockerfile with proper ownership

### 4. Agent Name Generation

- **Issue:** Random names not matching expected format
- **Resolution:** Updated agent_comm.sh to cache auto-generated names

### 5. Rate Limiting

- **Issue:** 403 Forbidden errors on MCP calls
- **Resolution:** Disabled RBAC and rate limiting in docker-compose.yml

## Next Steps

1. ✅ Deploy hub on unified-home-core-cloud
2. ✅ Verify message delivery
3. 🔄 Update mission_sync.sh for beads integration
4. 🔄 Configure local agents to use centralized hub
5. 🔄 End-to-end multi-agent communication test

## Maintenance

### View Logs

```bash
ssh gonya@100.110.209.49 "ps aux | grep mcp_agent_mail"
```

### Restart Hub

```bash
ssh root@100.110.209.49 "systemctl restart mcp-agent-mail"
```

### Service Location

```bash
# Running at: /opt/mcp-agent-mail
# Started via: uv run python -m mcp_agent_mail.cli serve-http --host 0.0.0.0 --port 8765
```

## Security Notes

- Hub uses bearer token authentication
- All communication over Tailscale VPN
- RBAC disabled for simplified agent coordination
- Rate limiting disabled for performance

---

**Status:** ✅ Operational and tested  
**Verified:** 2025-12-25T18:05:00+02:00
