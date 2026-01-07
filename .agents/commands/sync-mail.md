---
description: Sync mail, fetch tasks, and update agent status
---
// turbo

# Sync Mail & Status Workflow

> Synchronizing with Centralized Agent Hub...

This workflow helps agents sync with each other to ensure coordination and avoid conflicts.

---

## Prerequisites

Set these environment variables in your `.env` or session:

```bash
AGENT_NAME=FuchsiaCat          # Your assigned agent name
AGENT_PROJECT_KEY=/Gonya990/Unified_System_Core
```

Your agent name is assigned once during initial registration. Use `$AGENT_NAME` throughout.

---

## Step 1: Fetch Inbox

Check for new messages from other agents or the user.

```
agent_mail_fetch_inbox(
  project_key="$AGENT_PROJECT_KEY",
  agent_name="$AGENT_NAME",
  include_bodies=true,
  limit=20
)
```

**Actions**:
- **URGENT messages**: STOP this workflow and handle immediately
- **Coordination messages** (e.g., "I'm editing file X"): Respect file reservations
- **Ack-required messages**: Acknowledge with `agent_mail_acknowledge_message`

---

## Step 2: Check File Reservations

Before editing files, check if another agent has reserved them.

```
agent_mail_file_reservation_paths(
  project_key="$AGENT_PROJECT_KEY",
  agent_name="$AGENT_NAME",
  paths=["<files-you-plan-to-edit>"],
  exclusive=true,
  reason="<what you're doing>"
)
```

If conflicts are reported, coordinate with the holder or wait.

---

## Step 3: Sync Task Board (Beads)

Ensure your task list is up to date.

```bash
bd sync
bd ready
```

**Actions**:
- Check if your current task was modified or closed by another agent
- Look for new high-priority blockers
- Claim work with `bd update <id> --status=in_progress`

---

## Step 4: Check Workflow Locks

Check if another agent is performing a critical operation.

```bash
if [ -f .agent/.workflow-lock ]; then
  echo "LOCK FOUND:"
  cat .agent/.workflow-lock
else
  echo "No active workflow locks."
fi
```

If lock exists and is recent (< 5 min), wait before starting conflicting workflows.

---

## Step 5: Broadcast Status (Optional)

If you completed significant work or are starting a major task, notify other agents:

```
agent_mail_send_message(
  project_key="$AGENT_PROJECT_KEY",
  sender_name="$AGENT_NAME",
  to=["<other-agents>"],
  subject="Status Update",
  body_md="Starting work on <task>. Will be editing <files>."
)
```

---

## Step 6: Summary Report

After syncing, report:

- **Inbox**: X new messages (Y urgent)
- **File Reservations**: Any conflicts?
- **Tasks**: Any status changes from beads?
- **Locks**: Active workflow locks?

If all clear, proceed with your work.

---

## Quick Sync (One-liner)

For fast syncs, just fetch inbox and check beads:

```
1. agent_mail_fetch_inbox(project_key="$AGENT_PROJECT_KEY", agent_name="$AGENT_NAME", include_bodies=true)
2. bd sync && bd ready
```

---

## First-Time Setup

If you're a new agent and don't have `$AGENT_NAME` yet:

1. Ask Kostya to assign you an agent name (e.g., FuchsiaCat, PurpleCastle)
2. Add to your `.env`:
   ```
   AGENT_NAME=YourAssignedName
   AGENT_PROJECT_KEY=/Gonya990/Unified_System_Core
   ```
3. Registration is done once via `agent_mail_register_agent` at session start (handled by your agent framework)
