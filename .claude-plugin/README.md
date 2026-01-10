# Agent Mail Notifier Plugin

Alerts the agent when new mail arrives via agent-mail-mcp after subagent tasks complete.

## Components

### Hooks

**SubagentStop Hook** - After any subagent task completes, checks if the Agent Mail server is reachable and reminds the agent to check for new messages.

## Configuration

Set these environment variables to customize behavior:

| Variable | Default | Description |
|----------|---------|-------------|
| `AGENT_MAIL_PROJECT` | `/home/kosta/Documents/Unified_System_Core` | The project key for agent mail |
| `AGENT_MAIL_NAME` | `VioletCastle` | Your agent name in the mail system |
| `AGENT_MAIL_SERVER` | `http://igor-macbook:8765` | Agent mail server URL |

## How It Works

1. After a Task (subagent) completes, the `SubagentStop` hook triggers
2. The hook script checks if the Agent Mail server is reachable
3. If reachable, outputs a reminder with the `fetch_inbox` command syntax
4. Agent can then decide whether to check for and handle messages

## Files

```
.claude-plugin/
├── plugin.json          # Plugin manifest
└── README.md            # This file

hooks/
├── hooks.json           # Hook configuration
└── scripts/
    └── check-mail.sh    # Mail check script
```
