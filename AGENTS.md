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

> 💡 **Why Subagents?** Subagents run in separate context windows, saving tokens in the main conversation. Use them to offload work that doesn't need full session history.

### When to Use Subagents

- Browser automation tasks (clicking, navigating, screenshots)
- Long-running processes that need monitoring
- Parallel independent operations
- Visual verification (capture UI state)
- Tasks that can be described in <100 words

### Delegation Format

```
Task: <Clear description of what to do>
Context: <Minimal info needed - no session history>
Return: <What information to report back>
Stop when: <Clear termination condition>
```

### Never Delegate

- Security-sensitive operations
- Destructive actions without user approval
- Tasks requiring context not in the prompt
- Decision-making that needs user clarification

---

## 4. Skill Creation

> 💡 **Why Skills?** Skills reduce context by replacing inline explanations with stored procedures. A single `/workflow` command replaces 10+ tool calls.

### When to Create a Skill

Create reusable scripts/workflows when:

- A task is repeated 3+ times
- A manual process can be automated
- A complex command sequence is needed
- **You notice yourself typing similar commands repeatedly**

### Skill Priority Order

1. **Check if skill exists** — Run `/` to see available workflows
2. **Use existing skill** — Prefer `/commit-push` over manual git commands
3. **Create new skill** — If no skill exists and task will repeat

### Skill Locations

| Type | Location | Context Savings |
|------|----------|----------------|
| Workflows | `.agent/workflows/` | High (turbo auto-run) |
| Shell scripts | `Scripts/` | Medium (single command) |
| Expect scripts | `Scripts/*.exp` | High (interactive automation) |
| Python utilities | `Agent_Context/Knowledge_Base/Scripts/` | Medium |

### Skill Format (Workflows)

```yaml
---
description: Short description of what this does
---
1. Step one instructions
2. Step two instructions
// turbo  <- Auto-run annotation (agent can run without asking)
3. Safe step to auto-run
// turbo-all  <- Entire workflow auto-runs
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

## 8. Workflow Recommendations

### Available Workflows

| Workflow | Slash Command | When to Recommend |
|----------|---------------|-------------------|
| Commit & Push | `/commit-push` | After completing any implementation, fix, or documentation update |
| Update Progress | `/update-progress` | Before committing, or when switching tasks mid-session |
| System Status | `/status` | When debugging connectivity or checking system health |

### Trigger Points — When to Suggest Workflows

**After Implementation Completion:**
> 🎯 *"Implementation complete. Ready to run `/commit-push` to save changes?"*

**After Creating an Implementation Plan:**
> 📋 *"Plan created. Proceed with implementation, or update progress with `/update-progress`?"*

**When User Says "implement" or "do it":**

1. Execute the implementation
2. Then prompt: *"Done! Run `/commit-push` to commit and push these changes?"*

**Before Ending a Session:**
> 💾 *"Before we wrap up, should I run `/update-progress` to document current state?"*

**After Multiple File Changes:**
> 📦 *"Several files modified. Run `/update-progress` to stage and review before committing?"*

### Proactive Recommendations

Always suggest the relevant workflow when:

- ✅ A task is marked complete in `task.md`
- ✅ An implementation plan has been executed
- ✅ Documentation has been created or updated
- ✅ A bug fix has been verified
- ✅ User explicitly approves work

---

## 9. Context Optimization

### Use Skills to Minimize Context

**Rule:** If a task can be done by a skill/script, use it instead of inline commands.

| Instead of... | Use Skill |
|---------------|-----------|
| Manual git add/commit/push | `/commit-push` workflow |
| Inline progress updates | `/update-progress` workflow |
| Repeated SSH commands | `Scripts/*.exp` expect scripts |
| Multi-step deployments | `Scripts/deploy_*.sh` scripts |

**Benefits:**

- Reduces token consumption
- Ensures consistency
- Allows turbo auto-run

### Use Subagents to Offload Work

**Delegate to subagents when:**

| Scenario | Why Delegate |
|----------|--------------|
| Browser automation (clicking, scraping) | Subagent has specialized browser tools |
| Long-running commands (builds, downloads) | Frees main context for other work |
| Parallel verification tasks | Test multiple things simultaneously |
| Visual verification (screenshots) | Subagent can capture and report |

**Subagent Delegation Template:**

```markdown
**Task:** [Specific action to perform]
**Context:** [Minimal info needed - URLs, credentials ref, etc.]
**Return:** [Exact data/confirmation to report back]
**Stop when:** [Clear exit condition]
```

**Example - Offload Browser Login Check:**

```
Task: Navigate to http://100.88.65.71:8123 and verify Home Assistant login page loads
Context: Home Assistant on NODE-01
Return: Screenshot + confirmation of page title
Stop when: Page loaded or error after 30s
```

### When to Create New Skills

**Auto-create a skill when:**

1. You perform the same sequence 3+ times
2. A user asks "how do I do X again?"
3. A subagent task succeeds and may be reused
4. A complex multi-step process works

**Skill Locations:**

| Type | Location | When to Use |
|------|----------|-------------|
| Workflows (agent guidance) | `.agent/workflows/*.md` | Repeatable multi-step procedures |
| Shell scripts | `Scripts/*.sh` | System automation, deployments |
| Expect scripts | `Scripts/*.exp` | Interactive SSH/CLI automation |
| Python utilities | `Agent_Context/Knowledge_Base/Scripts/*.py` | Data processing, API calls |

---

## 10. Multi-Agent Coordination

> ⚠️ **Important:** Multiple agents may operate in this workspace simultaneously. Follow these rules to avoid conflicts and data loss.

### File Safety

**Before editing a file:**

1. Check if file was recently modified: `git diff <file>` or `ls -la <file>`
2. If another agent is working on the same file, coordinate or wait
3. Never overwrite entire files — use targeted edits (`replace_file_content`)

**Avoid overwriting other agents' work:**

| ❌ Dangerous | ✅ Safe Alternative |
|-------------|---------------------|
| `echo "..." > file` (overwrites) | `echo "..." >> file` (appends) |
| `write_to_file` with Overwrite=true | `replace_file_content` with targeted changes |
| `git reset --hard` | `git stash` or ask user first |
| `rm -rf` on shared folders | Only delete files you created |

### Git Coordination

**Before committing:**

```bash
# Always pull and rebase first to get other agents' changes
git pull --rebase origin main
```

**If rebase conflicts occur:**

1. Stop and notify user — don't force resolve
2. Show conflict files: `git diff --name-only --diff-filter=U`
3. Let user decide resolution strategy

**Commit scope rules:**

- Only commit files YOU modified in this session
- Use `git add <specific-files>` instead of `git add -A` if unsure
- Include agent identifier in commit if helpful: `feat(agent-mac): ...`

### Process Safety

**Never kill processes you didn't start:**

| ❌ Dangerous | ✅ Safe Alternative |
|-------------|---------------------|
| `pkill -9 node` | Only kill YOUR process by PID |
| `docker stop $(docker ps -q)` | `docker stop <specific-container>` |
| `killall python` | Track your PIDs, kill only those |
| `npm run dev` (if already running) | Check first: `lsof -i :PORT` |

**Before starting servers/services:**

```bash
# Check if port is already in use
lsof -i :3000 || npm run dev
```

### Session Artifacts

**Use unique identifiers for your work:**

- Session folders: `Sessions/<conversation-uuid>/`
- Temp files: `tmp/<agent-id>-<timestamp>.txt`
- Logs: Include timestamp in filename

**Protected shared files — edit carefully:**

| File | Risk Level | Coordination Required |
|------|------------|----------------------|
| `CONTEXT_HANDOFF.md` | 🟡 Medium | Append only, don't delete sections |
| `AGENTS.md` | 🔴 High | Discuss with user first |
| `.env` files | 🔴 High | Never overwrite, only add keys |
| `package.json` | 🟡 Medium | Targeted edits only |

### Conflict Resolution

**If you detect another agent's work:**

1. **Don't overwrite** — your changes aren't more important
2. **Read their changes** — maybe they already did what you planned
3. **Append, don't replace** — add your section/changes below theirs
4. **Notify user** — "I see recent changes from another session. Proceed or review first?"

### Workflow Lock Flags

When running multi-step workflows, create a lock indicator:

```bash
# At workflow start
echo "$(date -Iseconds) - workflow in progress" > .agent/.workflow-lock

# At workflow end
rm -f .agent/.workflow-lock
```

Before starting a workflow, check:

```bash
if [ -f .agent/.workflow-lock ]; then
  echo "Another workflow in progress, waiting..."
  # Either wait or notify user
fi
```

---

*These rules ensure consistency across all agents operating in the Unified System.*
