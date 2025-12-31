---
description: Manage tasks using the Beads Git-native issue tracker
---

# Beads Task Management

Use this workflow to track progress, create new tasks, and sync with the team.

## Step 1: List active tasks

// turbo

```bash
bd list --status in_progress,todo
```

## Step 2: Create a new task

```bash
bd create "[Task Description]"
```

## Step 3: Show task details

```bash
bd show [issue-id]
```

## Step 4: Update task status

```bash
bd update [issue-id] --status in_progress
bd update [issue-id] --status done
```

## Step 5: Sync tasks

// turbo

```bash
bd sync
```

---

## Operating Rules for Beads

1. **Create issues** for any significant new work.
2. **Update status** to `in_progress` when starting and `done` when finished.
3. **Sync often** to ensure other agents see your progress.
4. **Link commits** to issue IDs in commit messages if possible.
