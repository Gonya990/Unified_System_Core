---
description: Commit and push all changes to GitHub
---
// turbo-all

# Multi-Agent Safe Commit & Push

> ⚠️ This workflow is designed to work safely when multiple agents operate concurrently.

---

## Step 1: Check for workflow lock

```bash
if [ -f .agent/.workflow-lock ]; then cat .agent/.workflow-lock; fi
```

If lock exists and is recent (< 5 min), wait or ask user before proceeding.

---

## Step 2: Create workflow lock

```bash
echo "$(date -Iseconds) commit-push in progress" > .agent/.workflow-lock
```

---

## Step 3: Check for uncommitted changes before pulling

```bash
git status --short
```

If there are uncommitted changes:

- **DON'T use `git stash`** — it hides work from other agents
- Instead, commit as WIP first:

```bash
git add <your-files>
git commit -m "WIP: <agent-id> - <brief description>"
```

---

## Step 4: Pull latest changes (critical for multi-agent)

```bash
git pull --rebase origin main
```

If rebase conflicts occur:

- **STOP** the workflow
- Run: `git rebase --abort`
- Notify user: "Rebase conflict detected. Another agent may have pushed changes. Review needed."

---

## Step 5: Show status

```bash
git status --short
```

Review the output — only files YOU modified should be staged.

---

## Step 6: Stage changes

Option A — Stage all (if you're the only active agent):

```bash
git add -A
```

Option B — Stage specific files (safer for multi-agent):

```bash
git add <file1> <file2> ...
```

---

## Step 7: Commit with descriptive message

Commit message format:

```
<type>: <description>
```

Or with agent scope (helps identify which agent made changes):

```
<type>(mac-agent): <description>
```

---

## Step 8: Push to origin

```bash
git push origin main
```

If push is rejected (another agent pushed first):

1. `git pull --rebase origin main`
2. Resolve any conflicts (ask user if needed)
3. `git push origin main`

---

## Step 9: Release workflow lock

```bash
rm -f .agent/.workflow-lock
```

---

## Conflict Recovery

If anything fails mid-workflow:

```bash
# Check current state
git status

# If in middle of rebase
git rebase --abort

# If push was rejected
git pull --rebase origin main

# Always release lock
rm -f .agent/.workflow-lock
```
