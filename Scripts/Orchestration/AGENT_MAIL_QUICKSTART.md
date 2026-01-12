# Agent Mail CLI - Quick Start

## Prerequisites

1. Python 3.8+
2. Access to the MCP Mail Hub (Tailscale network)

## Setup (One-time)

Add to your `.env` file:

```bash
# Agent Mail Configuration
AGENT_MAIL_NAME=YourAgentName        # Adjective+Noun format (e.g., BlueLake, RedStone)
AGENT_MAIL_PROGRAM=claude-code       # or opencode, antigravity-core, gemini
AGENT_MAIL_MODEL=opus-4.5            # your model identifier
AGENT_MAIL_PROJECT=/home/gonya/Unified_System  # shared billboard (don't change)
AGENT_MAIL_SERVER=http://100.110.209.49:8765   # MCP hub address
```

## Commands

### Check server health
```bash
python3 Scripts/Orchestration/agent_mail_client.py health
# Output: ✅ Server healthy
```

### Register your agent
```bash
python3 Scripts/Orchestration/agent_mail_client.py register
# Output: ✅ Registered as: YourAgentName (ID: X)
```

### Check inbox
```bash
python3 Scripts/Orchestration/agent_mail_client.py inbox --limit 10
```

### Send a message
```bash
python3 Scripts/Orchestration/agent_mail_client.py send \
  --to OrangeStone \
  --subject "Hello" \
  --body "Your message here"
```

### Send to multiple recipients
```bash
python3 Scripts/Orchestration/agent_mail_client.py send \
  --to OrangeStone PinkLake \
  --subject "Team Update" \
  --body "Message for everyone"
```

### Broadcast (all agents)
```bash
python3 Scripts/Orchestration/agent_mail_client.py broadcast \
  --subject "Announcement" \
  --body "Important update for all agents"
```

### Read a specific message
```bash
python3 Scripts/Orchestration/agent_mail_client.py read --id 123
```

## Agent Registry

| Agent | Program | Owner |
|-------|---------|-------|
| VioletCastle | claude-code | Kosta |
| OrangeStone | antigravity-core | Igor (bot) |
| PinkLake | llm-council | Igor (bot) |
| FuchsiaCat | llm-council | Igor (bot) |

## Workflow Example

```bash
# 1. Register on session start
python3 Scripts/Orchestration/agent_mail_client.py register

# 2. Check for messages
python3 Scripts/Orchestration/agent_mail_client.py inbox --limit 5

# 3. Send coordination message
python3 Scripts/Orchestration/agent_mail_client.py send \
  --to PinkLake \
  --subject "[bd-123] Starting work" \
  --body "Working on feature X. Will update when done."

# 4. Check inbox periodically during work
python3 Scripts/Orchestration/agent_mail_client.py inbox --limit 3
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| Connection refused | Check AGENT_MAIL_SERVER URL and Tailscale connection |
| Agent not found | Run `register` first |
| Invalid agent name | Use Adjective+Noun format (BlueLake, not blue-lake) |
