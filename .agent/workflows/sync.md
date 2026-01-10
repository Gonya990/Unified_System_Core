---
description: Safe sync of git and tasks (no destructive operations)
---

// turbo

# Safe Sync

Sync git repository and task board without destructive operations.

## Quick Sync

```bash
bash Scripts/Orchestration/sync.sh
```

This runs:
1. **Git sync** - fetch, pull/push with rebase, handle conflicts
2. **Tasks sync** - `bd sync` + show ready tasks

## Individual Syncs

```bash
# Git only
bash Scripts/Orchestration/sync.sh git

# Tasks only
bash Scripts/Orchestration/sync.sh tasks
```

## Deployment (Separate)

Deployment is intentionally separate from sync:

```bash
# Update code on remote server
bash Scripts/Orchestration/deploy/remote-update.sh

# Restart services (bot, mcp, or all)
bash Scripts/Orchestration/deploy/restart-services.sh all
```

## Safety Features

- **No auto-commit** - warns if uncommitted changes exist
- **No force push** - handles conflicts via rebase
- **No hard reset** - preserves work on remote
- **Separate deploy** - sync code ≠ restart services
