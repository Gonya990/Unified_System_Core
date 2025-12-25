# Agent Registry

> Active agents in the Unified System multi-agent network.

## Registered Agents

| Agent ID | Status | Role | Primary Human | Last Seen |
|----------|--------|------|---------------|-----------|
| `rocinante` | Active | Exploration & Research | kosta | 2025-12-25 |
| `gonya` | Active | Operations & Implementation | igor | 2025-12-25 |

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
- **MCP Agent Mail:** `http://100.88.65.71:8765`
- **Git repo:** This repository (shared filesystem)
- **Task board:** `.beads/` (Beads issue tracker)

See `AGENT_ONBOARDING.md` for full integration protocol.
