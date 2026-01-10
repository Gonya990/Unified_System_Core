---
description: Sync mail, fetch tasks, and update agent status
---
// turbo

# Sync Mail & Status Workflow

> Synchronizing with Centralized Agent Hub...

**EXECUTE THIS SYNC NOW** - Do not just display documentation. Perform the following actions:

## Immediate Actions

1. **Register/Update Agent Status**:
```
mcp__mcp-agent-mail__register_agent(
  project_key="/home/gonya/Unified_System",
  program="claude-code",
  model="opus-4.5",
  name="VioletCastle",
  task_description="Active session"
)
```

2. **Fetch Inbox** (check for urgent messages):
```
mcp__mcp-agent-mail__fetch_inbox(
  project_key="/home/gonya/Unified_System",
  agent_name="VioletCastle",
  include_bodies=true,
  limit=20
)
```

3. **Report Results**: Summarize any messages found, especially urgent ones.

---

## Reference Documentation

This workflow helps agents sync with each other to ensure coordination and avoid conflicts.

---

## Billboard Project (Shared by All Agents)

```
PROJECT_KEY: /home/gonya/Unified_System
SERVER: igor-macbook (MCP Agent Mail)
```

All agents on this swarm use the SAME project key regardless of local working directory.

---

## Agent Registry

| Agent Name | Program | Host | Owner |
|------------|---------|------|-------|
| **VioletCastle** | claude-code (opus-4.5) | kosta-laptop | Kosta |
| **OrangeStone** | antigravity-core (gemini) | igor-macbook | Bot |
| **PinkLake** | llm-council (gemini) | igor-macbook | Bot |
| **FuchsiaCat** | llm-council (gemini) | igor-macbook | Bot |

---

## First-Time Onboarding

### 1. Check your local `.env` file

```bash
# grep for Agent Mail config
grep "AGENT_MAIL" .env
```

### 2. If not configured, add these lines to `.env`:

```bash
# Agent Mail Identity (host-specific)
AGENT_MAIL_NAME=YourAgentName        # e.g., VioletCastle
AGENT_MAIL_PROGRAM=claude-code       # or opencode, antigravity-core
AGENT_MAIL_MODEL=opus-4.5            # your model
AGENT_MAIL_PROJECT=/home/gonya/Unified_System  # ALWAYS this billboard
```

See `.env.example` for template.

### 3. Register with the billboard

```
mcp__mcp-agent-mail__register_agent(
  project_key="/home/gonya/Unified_System",
  program="$AGENT_MAIL_PROGRAM",
  model="$AGENT_MAIL_MODEL",
  name="$AGENT_MAIL_NAME",
  task_description="<what you're working on>"
)
```

### 4. Set contact policy (optional, for privacy)

```
mcp__mcp-agent-mail__set_contact_policy(
  project_key="/home/gonya/Unified_System",
  agent_name="$AGENT_MAIL_NAME",
  policy="contacts_only"  # or "open", "auto", "block_all"
)
```

---

## Regular Sync Workflow

### Step 1: Fetch Inbox

```
mcp__mcp-agent-mail__fetch_inbox(
  project_key="/home/gonya/Unified_System",
  agent_name="$AGENT_MAIL_NAME",
  include_bodies=true,
  limit=20
)
```

**Actions**:
- **URGENT messages**: STOP and handle immediately
- **Coordination messages**: Respect file reservations
- **Ack-required messages**: Call `acknowledge_message`

### Step 2: Check File Reservations (before editing)

```
mcp__mcp-agent-mail__file_reservation_paths(
  project_key="/home/gonya/Unified_System",
  agent_name="$AGENT_MAIL_NAME",
  paths=["<files-you-plan-to-edit>"],
  exclusive=true,
  ttl_seconds=3600,
  reason="bd-123: <task description>"
)
```

If conflicts reported, coordinate with holder or wait.

### Step 3: Sync Task Board (Beads)

```bash
bd sync
bd ready --json
```

**Actions**:
- Check if your task was modified/closed by another agent
- Look for new high-priority blockers
- Claim work with `bd update <id> --status=in_progress`

### Step 4: Broadcast Status (if needed)

```
mcp__mcp-agent-mail__send_message(
  project_key="/home/gonya/Unified_System",
  sender_name="$AGENT_MAIL_NAME",
  to=["OrangeStone", "VioletCastle"],  # relevant agents
  subject="[bd-123] Starting work",
  body_md="Working on <task>. Reserved <files>.",
  thread_id="bd-123",
  ack_required=false
)
```

---

## Quick Sync (One-liner)

For fast syncs between work steps:

```
1. mcp__mcp-agent-mail__fetch_inbox(project_key="/home/gonya/Unified_System", agent_name="$AGENT_MAIL_NAME")
2. bd sync && bd ready
```

---

## Discovery Commands

### Who's online?

```
mcp__mcp-agent-mail__whois(
  project_key="/home/gonya/Unified_System",
  agent_name="OrangeStone"  # or any agent name
)
```

### Search messages

```
mcp__mcp-agent-mail__search_messages(
  project_key="/home/gonya/Unified_System",
  query="bd-123 OR deployment",
  limit=20
)
```

### My contacts

```
mcp__mcp-agent-mail__list_contacts(
  project_key="/home/gonya/Unified_System",
  agent_name="$AGENT_MAIL_NAME"
)
```

---

## Reference Documentation

For detailed MCP Agent Mail usage, see:
- `External_Tools/Stack/mcp_agent_mail/AGENTS.md` - Section: "## MCP Agent Mail"
- `External_Tools/Stack/mcp_agent_mail/project_idea_and_guide.md` - Full design docs

Key sections to grep:

```bash
# How to use effectively
grep -A 50 "How to use effectively" External_Tools/Stack/mcp_agent_mail/AGENTS.md

# Beads integration
grep -A 30 "Integrating with Beads" External_Tools/Stack/mcp_agent_mail/AGENTS.md

# File reservations
grep -A 20 "File ownership & conflict" External_Tools/Stack/mcp_agent_mail/project_idea_and_guide.md
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `from_agent not registered` | Run `register_agent` first |
| `FILE_RESERVATION_CONFLICT` | Wait for expiry or coordinate |
| `Agent not found` | Check spelling, names are adjective+noun |
| Can't reach server | Check network to igor-macbook:8765 |
