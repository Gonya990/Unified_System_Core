# Workflow Design Decisions

> **Document:** Architecture Decision Record (ADR)  
> **Session:** workflow_design_c651  
> **Date:** 2025-12-24  
> **Author:** Antigravity (mac-agent) with User

---

## Context

The Unified System operates with **multiple AI agents working concurrently** in the same workspace. This creates unique challenges:

1. **Shared filesystem** — agents can overwrite each other's work
2. **Shared git repository** — commits can conflict
3. **Shared processes** — one agent might kill another's server
4. **Token efficiency** — context windows are limited
5. **Session continuity** — work must persist across agent sessions

---

## Constraints

| Constraint | Impact |
|------------|--------|
| Multiple agents, same directory | Need file-level coordination |
| Agents can't communicate directly | Must use git + filesystem as coordination layer |
| Local-only state is invisible | Other agents can't see stash, local branches, uncommitted work |
| Context window limits | Can't inline everything, need skills/workflows |
| Agents may crash mid-task | Work must be committed frequently |

---

## Design Decisions

### Decision 1: WIP Commits over Git Stash

**Problem:** `git stash` is local-only. If Agent A stashes work, Agent B cannot see or recover it.

**Options Considered:**

| Option | Pros | Cons |
|--------|------|------|
| `git stash` | Quick, easy | Local-only, invisible to others |
| Named branches | Visible on remote | Adds complexity, merge overhead |
| **WIP commits** | Visible, simple, recoverable | Pollutes history (minor) |

**Decision:** Use `WIP: <agent-id> - <description>` commits.

**Rationale:**

- Pushed to remote immediately → visible to all agents
- Can be squashed later if history cleanup needed
- Simple workflow, no branch management
- Allows mid-work recovery if agent crashes

---

### Decision 2: Workflow Locks

**Problem:** Multi-step workflows (like commit-push) shouldn't run concurrently.

**Options Considered:**

| Option | Pros | Cons |
|--------|------|------|
| No locking | Simple | Race conditions, conflicts |
| File-based lock | Simple, visible | No timeout, stale locks possible |
| **File-based with timestamp** | Visible, has timeout | Needs manual check for staleness |

**Decision:** Use `.agent/.workflow-lock` with timestamp.

**Format:**

```
2024-12-24T14:00:00+02:00 commit-push in progress
```

**Rationale:**

- Lock file is visible in git status (can be gitignored if needed)
- Timestamp allows agents to detect stale locks (> 5 min = stale)
- Simple to implement, no external dependencies

---

### Decision 3: Append-Only for Shared Files

**Problem:** Multiple agents editing `CONTEXT_HANDOFF.md` or `AGENTS.md` will conflict.

**Options Considered:**

| Option | Pros | Cons |
|--------|------|------|
| Lock shared files | Prevents conflicts | Blocks other agents |
| Per-agent sections | Parallel editing | Complex structure |
| **Append-only edits** | Minimal conflicts | May need periodic cleanup |

**Decision:** Shared files use append-only edits. Add rows to tables, add sections, never delete.

**Rationale:**

- Git can usually auto-merge appends at different positions
- Even if conflict occurs, resolution is straightforward
- Preserves all agents' contributions

---

### Decision 4: Session Isolation with UUIDs

**Problem:** Multiple agents storing artifacts in same location cause overwrites.

**Options Considered:**

| Option | Pros | Cons |
|--------|------|------|
| Shared folders | Simple | Conflicts, overwrites |
| Agent-named folders | Clear ownership | Agent names might collide |
| **UUID folders** | Guaranteed unique | Less readable |
| Timestamp folders | Unique, sortable | Can collide in same second |

**Decision:** Use `Sessions/<uuid>/` or `Sessions/<descriptive-name>/` for each conversation.

**Rationale:**

- UUIDs are guaranteed unique
- Descriptive names (like `nodriver_implementation`) are acceptable when clearly scoped
- Each agent works in their own folder, no conflicts

---

### Decision 5: Targeted Edits over Full File Writes

**Problem:** `write_to_file` with Overwrite=true destroys other agents' recent changes.

**Options Considered:**

| Option | Pros | Cons |
|--------|------|------|
| Full file writes | Simple | Destroys parallel changes |
| **Targeted edits** | Preserves other work | More complex |
| Patch files | Very precise | Overkill for most cases |

**Decision:** Always use `replace_file_content` or `multi_replace_file_content` for existing files.

**Rationale:**

- Only modifies specific lines, not entire file
- Other agents' changes (in different lines) are preserved
- Git merge is easier with smaller diffs

---

### Decision 6: Workflow Recommendations at Trigger Points

**Problem:** Agents forget to commit, update docs, or run appropriate workflows.

**Options Considered:**

| Option | Pros | Cons |
|--------|------|------|
| Manual tracking | Flexible | Easy to forget |
| Automatic execution | Consistent | May be unwanted |
| **Proactive suggestions** | Helpful, non-blocking | Requires discipline to follow |

**Decision:** Agents should proactively suggest workflows at defined trigger points.

**Trigger Points:**

- After implementation → `/commit-push`
- After creating plan → `/update-progress`
- Before ending session → `/update-progress`
- After multiple file changes → `/update-progress`

**Rationale:**

- Keeps user in control
- Reduces forgotten commits
- Creates consistent documentation habits

---

### Decision 7: Subagent Delegation for Context Savings

**Problem:** Main agent context fills up with repetitive browser actions, long outputs.

**Options Considered:**

| Option | Pros | Cons |
|--------|------|------|
| Inline everything | Simple | Fills context fast |
| **Subagent delegation** | Separate context | Requires clear handoff |
| External scripts | Reusable | Less flexible |

**Decision:** Delegate to subagents when task:

- Is browser automation
- Has long-running output
- Can be described in <100 words
- Doesn't need full session history

**Rationale:**

- Subagents have fresh context → more token room
- Main agent stays focused on high-level coordination
- Browser tasks especially benefit from dedicated context

---

## Rejected Alternatives

### Git Branches per Agent

- **Rejected because:** Adds merge complexity, agents would need to coordinate branch merges
- **Kept instead:** Single `main` branch with frequent small commits

### Database Lock System

- **Rejected because:** Adds infrastructure dependency, overkill for file-based coordination
- **Kept instead:** Simple file locks with timestamps

### Mandatory Code Review

- **Rejected because:** Blocks automation, agents can't review each other
- **Kept instead:** Trust agents, use WIP commits for visibility

---

## Summary

| Decision | Choice | Key Benefit |
|----------|--------|-------------|
| Git strategy | WIP commits, no stash | Remote visibility |
| Concurrency | File-based workflow locks | Simple, no dependencies |
| Shared files | Append-only edits | Conflict reduction |
| Artifact isolation | UUID session folders | No overwrites |
| File editing | Targeted replacements | Preserve parallel work |
| Workflow prompts | Proactive suggestions | Consistency |
| Context management | Subagent delegation | Token efficiency |

---

*These decisions optimize for multi-agent concurrency while maintaining simplicity and using git as the single source of truth.*
