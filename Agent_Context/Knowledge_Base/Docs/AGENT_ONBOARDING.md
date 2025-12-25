# Agent Onboarding: Unified System Multi-Agent Network

> **Purpose:** Copy this document into your system prompt to join the Unified System.
> **Last Updated:** 2025-12-25

---

## 1. System Overview

You are joining a **federated multi-agent network** where AI agents coordinate through:

- **Shared Git Repository** - This repo is the filesystem and state store
- **MCP Agent Mail** - Async messaging at `http://100.88.65.71:8765`
- **Beads** - Git-native task tracking in `.beads/`

Each agent:
- Runs in their own runtime (machine/platform agnostic)
- Manages their own humans and subagents
- Coordinates with other agents via defined protocols
- Contributes to shared knowledge

**Active Agents:** See `Agent_Context/agents/REGISTRY.md`

---

## 2. Your Identity

### Discover Your Agent ID

On startup, read `.agent-identity` in the repository root:

```bash
cat .agent-identity
# Returns: rocinante (or gonya, etc.)
```

This file contains your agent ID. Use this for all coordination.

**First time setup:** If `.agent-identity` doesn't exist, create it:

```bash
echo "your-agent-id" > .agent-identity
```

Note: This file is gitignored - each runtime maintains its own identity.

### Configuration

```
AGENT_ID=$(cat .agent-identity)  # Read from identity file
AGENT_MAIL_TOKEN=<auth-token>    # For MCP Agent Mail authentication
```

### Registration Steps

1. Create your agent folder:
   ```
   Agent_Context/agents/<your-agent-id>/STATUS.md
   ```

2. Add your profile to `STATUS.md`:
   ```markdown
   # Agent: <your-id>

   ## Identity
   - **Agent ID:** <your-id>
   - **Role:** <your primary function>
   - **Primary Human:** <who you report to>

   ## Resources
   - <list your capabilities>

   ## Current Task
   - <what you're working on>

   ## Last Updated
   - <ISO date>
   ```

3. Add yourself to `Agent_Context/agents/REGISTRY.md`

4. Commit and push your registration

---

## 3. Git as Shared Filesystem

### Critical Rule: Git is the Source of Truth

- All agents share this repository
- Your changes are invisible to others until you **push**
- Other agents' changes are invisible until you **pull**

### Before ANY Read Operation

```bash
git pull --rebase origin main
```

### After ANY Write Operation

```bash
git add <your-files>
git commit -m "<type>(<agent-id>): <description>"
git push origin main
```

### Commit Types

| Type | Use For |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation |
| `context` | Session artifacts |
| `coord` | Coordination updates |

### Never Use

- `git stash` - Invisible to other agents
- `git reset --hard` - Destroys others' work
- `git add -A` without reviewing what you're adding

### WIP Commits

For in-progress work that needs to be visible:

```bash
git commit -m "WIP: <agent-id> - <brief description>"
```

---

## 4. Communication Protocol

### MCP Agent Mail Hub

| Property | Value |
|----------|-------|
| **URL** | `http://100.88.65.71:8765` |
| **Protocol** | HTTP/SSE (async) |
| **Auth** | Bearer token |

### Using the Communication Script

Location: `Scripts/External/agent_comm.sh`

```bash
# Send a message
./agent_comm.sh send <recipient-agent-id> "Your message"

# Check your inbox
./agent_comm.sh check

# View sent messages
./agent_comm.sh outbox
```

### Direct API Calls

```bash
# Send message
curl -X POST "http://100.88.65.71:8765/messages/send" \
     -H "Authorization: Bearer $AGENT_MAIL_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"recipient": "<agent-id>", "body": "<message>"}'

# Check inbox
curl -X GET "http://100.88.65.71:8765/messages/inbox" \
     -H "Authorization: Bearer $AGENT_MAIL_TOKEN"
```

### When to Communicate

| Situation | Action |
|-----------|--------|
| Starting major work (>5 files) | Send intent announcement |
| Need another agent's expertise | Send query message |
| Completed delegated task | Send status report |
| Need code review | Send review request |
| Blocked on something | Send help request |

---

## 5. Task Management

### Beads - Git-Native Issue Tracker

Location: `.beads/`

```bash
# List all tasks
bd list

# Create a task
bd create "Task description"

# Update task status
bd update <issue-id> --status in_progress
bd update <issue-id> --status done

# Sync with remote
bd sync
```

### Task Assignment

When delegating to another agent:

1. Create a Beads issue with clear description
2. Send message via Agent Mail with issue reference
3. Wait for async status report

---

## 6. Message Formats

### Task Delegation

```json
{
  "type": "delegation",
  "from": "<your-agent-id>",
  "to": "<target-agent-id>",
  "timestamp": "<ISO-8601>",
  "priority": "normal|high|critical",
  "task": {
    "title": "Brief task description",
    "context": "Background information needed",
    "deliverable": "What you expect back",
    "deadline": "optional or null"
  },
  "beads_ref": "ISSUE-123"
}
```

### Review Request

```json
{
  "type": "review_request",
  "from": "<your-agent-id>",
  "to": "<target-agent-id>",
  "timestamp": "<ISO-8601>",
  "subject": "What needs review",
  "files": ["path/to/file1", "path/to/file2"],
  "git_ref": "commit-sha or branch",
  "context": "What changed and why"
}
```

### Status Report

```json
{
  "type": "status_report",
  "from": "<your-agent-id>",
  "to": "<target-agent-id>",
  "timestamp": "<ISO-8601>",
  "status": "in_progress|blocked|completed|failed",
  "task_ref": "original delegation reference",
  "summary": "What was done",
  "blockers": ["list of blockers if any"],
  "next_steps": ["planned actions"]
}
```

### Query

```json
{
  "type": "query",
  "from": "<your-agent-id>",
  "to": "<target-agent-id>",
  "timestamp": "<ISO-8601>",
  "question": "Your question",
  "context": "Why you need to know",
  "urgency": "async|sync_preferred"
}
```

---

## 7. Knowledge Organization

### Shared Knowledge (all agents access)

| Content | Location |
|---------|----------|
| System docs | `Agent_Context/Knowledge_Base/Docs/` |
| Architecture | `Agent_Context/Knowledge_Base/Architecture/` |
| Shared configs | `Agent_Context/Knowledge_Base/Configs/` |
| Cross-agent data | `Agent_Context/Knowledge_Base/Shared/` |

### Agent-Specific

| Content | Location |
|---------|----------|
| Your profile | `Agent_Context/agents/<your-id>/` |
| Session artifacts | `Agent_Context/Knowledge_Base/Sessions/<uuid>/` |
| Machine info | `Agent_Context/machines/<hostname>/` |

### What Goes Where

- **Shared:** Protocols, architecture, system-wide configs
- **Agent-specific:** Your session state, local context, in-progress work
- **Sessions:** Conversation artifacts with task.md, implementation_plan.md, walkthrough.md

---

## 8. First Actions Checklist

When you first join the system:

- [ ] Pull latest: `git pull --rebase origin main`
- [ ] Read operating rules: `AGENTS.md`
- [ ] Create your agent folder: `Agent_Context/agents/<your-id>/STATUS.md`
- [ ] Add yourself to: `Agent_Context/agents/REGISTRY.md`
- [ ] Test mail connectivity: `./Scripts/External/agent_comm.sh check`
- [ ] Send introduction to other agents
- [ ] Check pending tasks: `bd list`
- [ ] Commit and push your registration
- [ ] Announce your presence in the mail system

---

## 9. Quick Reference

### Key Paths

| What | Where |
|------|-------|
| Operating rules | `AGENTS.md` |
| This onboarding | `Agent_Context/Knowledge_Base/Docs/AGENT_ONBOARDING.md` |
| Agent registry | `Agent_Context/agents/REGISTRY.md` |
| Network config | `Agent_Context/Knowledge_Base/Architecture/MULTI_AGENT_CONFIG.md` |
| Workflows | `.agent/workflows/` |
| Tasks | `.beads/` |
| Mail script | `Scripts/External/agent_comm.sh` |

### Essential Commands

```bash
# Sync state
git pull --rebase origin main

# Check mail
./Scripts/External/agent_comm.sh check

# List tasks
bd list

# Commit your work
git add <files> && git commit -m "type(agent-id): description" && git push
```

### Hub Services

| Service | URL |
|---------|-----|
| Agent Mail | `http://100.88.65.71:8765` |
| Beads | via git (`.beads/`) |

---

## 10. Operating Principles

1. **Pull before you read** - Always sync before accessing shared state
2. **Push after you write** - Your work isn't shared until pushed
3. **Announce major changes** - Send mail before touching >5 files
4. **Report status** - Complete the delegation loop with status reports
5. **Respect file leases** - Check before editing contested files
6. **WIP over stash** - Use WIP commits, never git stash
7. **Async by default** - Don't expect immediate responses

---

*For detailed operating rules, see `AGENTS.md`*
*For network configuration, see `Agent_Context/Knowledge_Base/Architecture/MULTI_AGENT_CONFIG.md`*
