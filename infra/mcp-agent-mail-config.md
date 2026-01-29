# MCP Agent Mail Configuration

Configuration templates for adding mcp-agent-mail to Claude Code and OpenCode.

## Server Details

- **Server URL**: `http://100.110.209.49:8765/mcp` (unified-home-core-cloud via Tailscale)
- **Auth Token**: `<AGENT_MAIL_TOKEN>`
- **Project Key**: `/home/gonya/Unified_System`

## Claude Code Configuration

Add to `~/.claude.json` under `projects.<project-path>.mcpServers` or global `mcpServers`:

```json
{
  "mcpServers": {
    "mcp-agent-mail": {
      "type": "http",
      "url": "http://100.110.209.49:8765/mcp",
      "headers": {
        "Authorization": "Bearer <AGENT_MAIL_TOKEN>"
      }
    }
  }
}
```

Or run this command to add it:

```bash
python3 << 'EOF'
import json
import os

config_path = os.path.expanduser("~/.claude.json")
with open(config_path, 'r') as f:
    config = json.load(f)

config.setdefault("mcpServers", {})["mcp-agent-mail"] = {
    "type": "http",
    "url": "http://100.110.209.49:8765/mcp",
    "headers": {
        "Authorization": "Bearer <AGENT_MAIL_TOKEN>"
    }
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
print("Done!")
EOF
```

## OpenCode Configuration

Add to `~/.config/opencode/opencode.json` under `mcp`:

```json
{
  "mcp": {
    "mcp-agent-mail": {
      "type": "remote",
      "url": "http://100.110.209.49:8765/mcp",
      "headers": {
        "Authorization": "Bearer <AGENT_MAIL_TOKEN>"
      },
      "enabled": true
    }
  }
}
```

Or use the CLI:

```bash
opencode mcp add
# Select "remote" when prompted
# URL: http://100.110.209.49:8765/mcp
# Add header: Authorization: Bearer <AGENT_MAIL_TOKEN>
```

## Agent Identity (.env)

Each machine should have a unique agent name in `.env`:

```bash
# Agent Mail Identity (host-specific)
AGENT_MAIL_NAME=YourAgentName        # Unique per machine (e.g., VioletCastle, CrimsonTower)
AGENT_MAIL_PROGRAM=claude-code       # or opencode
AGENT_MAIL_MODEL=opus-4.5            # your model
AGENT_MAIL_PROJECT=/home/gonya/Unified_System
AGENT_MAIL_SERVER=http://100.110.209.49:8765
```

## Agent Registry

| Agent Name | Host | Owner |
|------------|------|-------|
| VioletCastle | kosta-laptop | Kosta |
| CrimsonTower | code-minion | AI |
| OrangeStone | igor-macbook | Bot |
| PinkLake | igor-macbook | Bot |

## Verification

After configuration, restart Claude Code or OpenCode and verify with:

```bash
# Claude Code - check for mcp-agent-mail tools
claude --help  # tools should include mcp__mcp-agent-mail__*

# OpenCode
opencode mcp list
```

## Troubleshooting

1. **Connection refused**: Ensure unified-home-core-cloud (100.110.209.49) is reachable via Tailscale
2. **Auth error**: Verify the bearer token is correct
3. **Tools not appearing**: Restart the CLI after config changes
