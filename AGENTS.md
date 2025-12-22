# 🤖 Agent Operating Rules

> Guidelines for AI agents working within the Unified System.

---

## 1. Git Workflow

### Always Commit Your Work

```bash
# After completing any task:
git add -A
git commit -m "<type>: <description>"
git push origin main
```

### Commit Types

| Type | Use for |
|------|---------|
| `feat` | New features or capabilities |
| `fix` | Bug fixes |
| `docs` | Documentation changes |
| `refactor` | Code restructuring |
| `context` | AI context/session additions |
| `cleanup` | Removing unused files |
| `scripts` | New automation scripts |

### Before Committing

- Pull latest: `git pull --rebase origin main`
- Scan for secrets: `grep -rE "(token|password|api_key).*=" .`
- Group related changes into logical commits

---

## 2. Planning & Task Management

### Use Implementation Plans

For complex tasks (>5 tool calls):

1. Create `implementation_plan.md` with:
   - Goal description
   - Proposed changes (grouped by component)
   - Verification plan
2. Request user approval via `notify_user`
3. Execute only after approval

### Track Progress with task.md

```markdown
# Task: [Task Name]

- [ ] Pending item
- [/] In progress
- [x] Completed
```

Update `task.md` as you work. Mark items `[/]` when starting, `[x]` when done.

### Create Walkthroughs

After completing work, create `walkthrough.md` documenting:

- What was changed
- What was tested
- Screenshots/recordings if UI work

---

## 3. Subagent Delegation

### When to Use Subagents

- Browser automation tasks
- Long-running processes that need monitoring
- Parallel independent operations

### Delegation Format

```
Task: <Clear description of what to do>
Return: <What information to report back>
Stop when: <Clear termination condition>
```

### Never Delegate

- Security-sensitive operations
- Destructive actions without user approval
- Tasks requiring context not in the prompt

---

## 4. Skill Creation

### When to Create a Skill

Create reusable scripts/workflows when:

- A task is repeated 3+ times
- A manual process can be automated
- A complex command sequence is needed

### Skill Locations

| Type | Location |
|------|----------|
| Shell scripts | `Scripts/` |
| Python utilities | `Agent_Context/Knowledge_Base/Scripts/` |
| Workflows | `.agent/workflows/` |

### Skill Format (Workflows)

```yaml
---
description: Short description of what this does
---
1. Step one instructions
2. Step two instructions
// turbo  <- Auto-run annotation
3. Safe step to auto-run
```

---

## 5. Context Management

### Where to Store Context

| Content | Location |
|---------|----------|
| Session artifacts | `Agent_Context/Knowledge_Base/Sessions/<uuid>/` |
| System docs | `Agent_Context/Knowledge_Base/Docs/` |
| Architecture | `Agent_Context/Knowledge_Base/Architecture/` |
| Machine info | `Agent_Context/machines/<hostname>/` |

### Read Before Acting

Before starting work, check:

1. `CONTEXT_HANDOFF.md` — Current system state
2. `task.md` — Pending items from previous sessions
3. Machine-specific `MACHINE_INFO.md` if relevant

---

## 6. Communication

### With Users

- Be concise — no walls of text
- Use tables and lists for structured data
- Include file links: `[filename](file:///path/to/file)`
- Ask clarifying questions before big decisions

### Between Sessions

- Update handoff docs with current state
- Mark in-progress items clearly
- Leave TODO comments in code if needed

---

## 7. Safety Rules

### Never Auto-Run

- `rm -rf` or destructive commands
- Commands with passwords/tokens inline
- Network requests to unknown URLs
- File operations outside workspace

### Always Confirm With User

- Major refactoring (>20 files)
- Deleting data
- Changing configurations
- External service integrations

---

*These rules ensure consistency across all agents operating in the Unified System.*
