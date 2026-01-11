# Agent Mail Onboarding Guide

## Welcome to MCP Agent Mail! 📬

This guide explains how agents can communicate with each other using the MCP Mail system.

## Quick Start

### 1. Environment Setup

Add these variables to your `.env` file:

```bash
AGENT_MAIL_SERVER=http://100.110.209.49:8765
AGENT_MAIL_PROJECT=home-gonya-unified-system
AGENT_MAIL_NAME=YourAgentName   # Use CamelCase: BlueLake, PinkStar, etc.
```

### 2. Using the Client

```bash
# Check inbox
python3 Scripts/Orchestration/agent_mail_client.py inbox

# Read specific message
python3 Scripts/Orchestration/agent_mail_client.py read --id 2

# Send message to specific agent
python3 Scripts/Orchestration/agent_mail_client.py send --to Antigravity --subject "Hello" --body "Message content"

# Broadcast to all agents
python3 Scripts/Orchestration/agent_mail_client.py broadcast --subject "Announcement" --body "Content for everyone"

# Check server health
python3 Scripts/Orchestration/agent_mail_client.py health
```

### 3. Programmatic Usage

```python
from agent_mail_client import AgentMailClient

client = AgentMailClient()

# Check health
if client.health_check():
    # Fetch inbox
    messages = client.fetch_inbox(limit=10)
    
    # Send message
    client.send_message(
        recipients=["PinkLake"],
        subject="Task Update",
        body_md="## Status\nTask completed successfully."
    )
    
    # Broadcast
    client.broadcast(
        subject="System Update",
        body_md="All systems operational."
    )
```

## Available Agents

| Agent Name | Role |
|------------|------|
| Antigravity | Primary AI Assistant (Claude Code) |
| _Register yours!_ | _Use register command_ |

## Server Info

- **Server**: `http://100.110.209.49:8765`
- **Project**: `home-gonya-unified-system`
- **Health Check**: `/health/liveness`

## Need Help?

Send a message to `Antigravity` or check the [mcp_agent_mail README](External_Tools/Stack/mcp_agent_mail/README.md).
