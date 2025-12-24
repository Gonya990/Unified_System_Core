---
description: Update status and progress in docs, prepare for commit (no commit)
---

# Update Progress & Status Workflow

> ⚠️ **Multi-Agent Safe:** This workflow only modifies YOUR session folder. Shared files (CONTEXT_HANDOFF.md) are updated with append-only edits.

This workflow updates all relevant documentation with current session progress and prepares changes for commit.

**Your Session ID:** Use your conversation UUID to isolate your work from other agents.

---

## Step 1: Identify Current Session

Determine the active session by checking recent conversation context:

```bash
ls -lt Agent_Context/Knowledge_Base/Sessions/ | head -10
```

Note the session folder(s) you've been working in. If creating new work, generate a UUID:

```bash
uuidgen | tr '[:upper:]' '[:lower:]'
```

---

## Step 2: Update/Create task.md

Navigate to or create the session folder and update `task.md`:

**Location:** `Agent_Context/Knowledge_Base/Sessions/<session-id>/task.md`

**Format:**

```markdown
# Task: [Task/Project Name]

## Phase 1: [Phase Name] <!-- id: 100 -->

- [ ] Pending item <!-- id: 101 -->
- [/] In progress (currently active) <!-- id: 102 -->
- [x] Completed item <!-- id: 103 -->

## Phase 2: [Next Phase] <!-- id: 200 -->

- [ ] Future item <!-- id: 201 -->
```

**Rules:**

- Mark items `[/]` when starting work
- Mark items `[x]` when complete
- Add `<!-- CURRENT FOCUS -->` to active items
- Use sequential IDs for tracking

---

## Step 3: Create/Update walkthrough.md (if completing work)

If finishing a task or milestone, create a walkthrough:

**Location:** `Agent_Context/Knowledge_Base/Sessions/<session-id>/walkthrough.md`

**Format:**

```markdown
# Walkthrough: [What Was Accomplished]

> **Date:** YYYY-MM-DD
> **Session:** <session-id>

## Summary

Brief description of what was done.

## Changes Made

1. **[Component/File]**: Description of change
2. **[Component/File]**: Description of change

## Verification

- [ ] How it was tested
- [ ] Expected behavior confirmed

## Screenshots/Evidence

[Include if applicable]

## Next Steps

- Follow-up tasks
- Known issues
```

---

## Step 4: Update CONTEXT_HANDOFF.md

Update the central handoff document with current state:

**Location:** `Agent_Context/Knowledge_Base/Architecture/CONTEXT_HANDOFF.md`

> ⚠️ **Multi-Agent Warning:** This is a SHARED file. Multiple agents may edit it.
>
> - **APPEND only** — add your session to tables, don't delete others
> - **Use targeted edits** — don't overwrite the entire file
> - **Check recent changes first:** `git diff Agent_Context/Knowledge_Base/Architecture/CONTEXT_HANDOFF.md`

**Update these sections:**

1. **Active Conversation Artifacts** table — ADD a row for your session
2. **ACTIVE TODOS & TASKS** — ADD your tasks in a new subsection
3. **HANDOFF CHECKLIST** — append new items if needed

---

## Step 5: Update machine-specific docs (if infrastructure work)

If working on machine-specific configurations:

**Location:** `Agent_Context/machines/<hostname>/`

Check files like:

- `MACHINE_INFO.md`
- `services.yaml`
- Any config-specific docs

---

## Step 6: Review changed files

// turbo
Check what files have been modified:

```bash
git status --short
```

---

## Step 7: Stage changes

// turbo
Stage all documentation updates:

```bash
git add -A
```

---

## Step 8: Show staged changes for review

// turbo
Display staged changes summary:

```bash
git diff --cached --stat
```

---

## Step 9: Verify no secrets exposed

// turbo
Scan for potential secrets (review output manually):

```bash
grep -rE "(token|password|api_key|secret).*=" Agent_Context/ --include="*.md" --include="*.yaml" --include="*.json" 2>/dev/null | head -20
```

---

## ⚠️ STOP HERE — DO NOT COMMIT

Changes are now staged and ready. The user must:

1. Review `git diff --cached` output
2. Decide on commit message format:
   - `docs: update progress for <session/task>`
   - `context: session <id> - <brief summary>`
3. Run `/commit-push` workflow when ready

---

## Quick Reference: Documentation Locations

| Content Type | Location |
|--------------|----------|
| Session tasks | `Agent_Context/Knowledge_Base/Sessions/<id>/task.md` |
| Session summary | `Agent_Context/Knowledge_Base/Sessions/<id>/walkthrough.md` |
| Implementation plans | `Agent_Context/Knowledge_Base/Sessions/<id>/implementation_plan.md` |
| System handoff | `Agent_Context/Knowledge_Base/Architecture/CONTEXT_HANDOFF.md` |
| Machine info | `Agent_Context/machines/<hostname>/` |
| Architecture docs | `Agent_Context/Knowledge_Base/Architecture/` |
| General docs | `Agent_Context/Knowledge_Base/Docs/` |
