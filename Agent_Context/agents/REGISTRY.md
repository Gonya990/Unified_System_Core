# Agent Registry

> Active agents in the Unified System multi-agent network.

## Registered Agents (Agent-Mail)

| Agent Name | Project | Program | Model | Role | Last Active |
|------------|---------|---------|-------|------|-------------|
| `PinkLake` | Unified_System_Core | opencode | claude-sonnet-4 | Main orchestration | 2026-01-07 |
| `Antigravity` | Unified_System_Core | antigravity | gemini-2.0-pro | Cross-machine coordination | 2026-01-11 |

## Legacy Agents (Pre Agent-Mail)

| Agent ID | Status | Role | Primary Human | Last Seen |
|----------|--------|------|---------------|-----------|
| `rocinante` | Inactive | Exploration & Research | kosta | 2025-12-25 |
| `gonya` | Inactive | Operations & Implementation | igor | 2025-12-25 |
| `Antigravity` | Pending | Cross-machine coordination | kosta | 2025-12-31 |
| `FuchsiaCat` | Pending | WSL2 automation | kosta | 2026-01-07 |

## How to Register

1. Create your agent folder: `agents/<your-agent-id>/`
2. Add `STATUS.md` with your profile (see template below)
3. Update this registry table
4. Commit and push

## Agent Profile Template

```markdown
# Agent: <agent-id>

## Identity
- **Agent ID:** <unique-identifier>
- **Role:** <primary function>
- **Primary Human:** <who you report to>

## Resources
- <list of capabilities, e.g., "GPU inference available">

## Current Task
- <what you're working on>

## Last Updated
- <ISO timestamp>
```

## Communication

All agents communicate via:

- **MCP Agent Mail:** `http://127.0.0.1:8765` (shared server - ALL agents connect here)
- **Git repo:** This repository (shared filesystem)
- **Task board:** `.beads/` (Beads issue tracker)

### Project Key (IMPORTANT)

All agents use the **same project slug** (not absolute paths):

```
PROJECT_KEY = "/Gonya990/Unified_System_Core"
```

This allows agents on different machines to coordinate via the shared hub server.

### Registering with Agent-Mail

```bash
# At session start, register yourself:
agent_mail_register_agent(
  project_key="/Gonya990/Unified_System_Core",
  program="opencode",  # or "claude-code", "codex", etc.
  model="claude-sonnet-4",
  name="YourAgentName",  # Adjective+Noun format (e.g., BlueLake)
  task_description="What you're working on"
)

# Then update this REGISTRY.md with your info
```

### Sending Messages

```bash
# Check who's available
agent_mail_whois(project_key="/Gonya990/Unified_System_Core", agent_name="PinkLake")

# Send a message
agent_mail_send_message(
  project_key="/Gonya990/Unified_System_Core",
  sender_name="YourName",
  to=["PinkLake"],
  subject="Coordination request",
  body_md="Your message here"
)
```

See `AGENT_ONBOARDING.md` for full integration protocol.
