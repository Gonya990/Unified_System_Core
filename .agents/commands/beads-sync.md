# Beads Sync

Synchronize beads issues with git remote.

## Usage

```
/beads-sync [--flush-only] [--import-only]
```

## Sync Workflow (CORRECT ORDER)

```bash
# 1. Export local DB → JSONL
bd sync --flush-only

# 2. Commit beads before pull (CRITICAL - avoids conflicts)
git add .beads/ && git commit -m "chore(beads): sync"

# 3. Pull remote changes
git pull --rebase

# 4. Import merged JSONL
bd sync --import-only

# 5. Final reconcile & push
bd sync
```

## Conflict Resolution

If merge conflict in `.beads/issues.jsonl`:

```bash
git checkout --theirs .beads/issues.jsonl  # Accept remote
bd sync --import-only                       # Re-import
bd sync                                     # Reconcile
```

## Key Rule

> ⚠️ Always commit `.beads/` changes BEFORE `git pull`.
> Conflicts happen when you pull with uncommitted beads changes.

## Quick Commands

| Command | Description |
|---------|-------------|
| `bd sync` | Full sync (flush + git + import) |
| `bd sync --flush-only` | Export DB → JSONL only |
| `bd sync --import-only` | Import JSONL → DB only |
| `bd sync --status` | Check sync status |
| `bd sync --rename-on-import` | Handle prefix mismatches |

## Session Protocol

1. `bd ready` — Find unblocked work
2. `bd show <id>` — Get full context
3. `bd update <id> --status in_progress` — Start work
4. `bd close <id> --reason "..."` — Complete task
5. **`bd sync`** — Run at session end (ALWAYS)

## Blocker Protocol

> ⚠️ **NEVER skip verification silently.** If infra/env blocks task completion, create a bead.

When a task cannot be fully completed due to blockers:

```bash
# 1. Create a bead for the blocker
bd create --title "[INFRA] <description of blocker>" --type bug --priority 2

# 2. Add context
bd update <new-id> --description "## Problem\n<what failed>\n\n## Impact\n<what was skipped>"

# 3. Do NOT close the original task without verification evidence
```

**Examples of blockers that need beads:**
- Test environment broken (missing deps, build failures)
- External service unavailable
- Missing credentials/access
- Hardware/network issues

**Rule:** If you can't prove it works, don't close it. Create a blocker bead instead.

## bd vs TodoWrite

| bd (persistent) | TodoWrite (ephemeral) |
|-----------------|----------------------|
| Multi-session work | Single-session tasks |
| Survives compaction | Conversation-scoped |
| Git-backed, team sync | Local to session |

**Decision**: "Will I need this context in 2 weeks?" → YES = bd
