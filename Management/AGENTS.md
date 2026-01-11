# 🤖 Agent Operating Rules

> Guidelines for AI agents working within the Unified System.

**New agent?** Start with
[`AGENT_ONBOARDING.md`](Agent_Context/Knowledge_Base/Docs/AGENT_ONBOARDING.md)
for integration guide.

**Agent Registry:**
[`Agent_Context/agents/REGISTRY.md`](Agent_Context/agents/REGISTRY.md)

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
| --- | --- |
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

### Use Beads for Task Tracking

**Beads** is the primary task management system. Use it for:

- Multi-session work that needs persistence
- Tasks with dependencies
- Discovered work that emerges during implementation
- Anything that should survive context switches

### Beads Workflow

```bash
# Find available work
bd ready                              # Show issues ready to work (no blockers)
bd list --status=open                 # All open issues

# Create and manage issues
bd create --title="..." --type=task|bug|feature --priority=2
bd update <id> --status=in_progress   # Claim work
bd close <id>                         # Mark complete
bd close <id1> <id2> ...              # Close multiple at once

# Dependencies
bd dep add <issue> <depends-on>       # Add dependency
bd blocked                            # Show blocked issues

# Sync with remote
bd sync                               # Run at session end
```

### Priority Levels

| Priority | Use for |
| --- | --- |
| P0 | Critical - blocks everything |
| P1 | High - urgent work |
| P2 | Medium - standard tasks |
| P3 | Low - nice to have |
| P4 | Backlog - future work |

### Use Implementation Plans

For complex tasks (>5 tool calls):

1. Create a beads issue with clear scope
2. Break into sub-tasks if needed (use dependencies)
3. Request user approval before major changes
4. Execute and close issues as you complete them

### Create Walkthroughs

After completing significant work, create `walkthrough.md` documenting:

- What was changed
- What was tested
- Screenshots/recordings if UI work

---

## 3. Subagent Delegation

> 💡 **Why Subagents?** Subagents run in separate context windows, saving tokens
> in the main conversation. Use them to offload work that doesn't need full
> session history.

### When to Use Subagents

- Browser automation tasks (clicking, navigating, screenshots)
- Long-running processes that need monitoring
- Parallel independent operations
- Visual verification (capture UI state)
- Tasks that can be described in <100 words

### Delegation Format

```markdown
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

> 💡 **Why Skills?** Skills reduce context by replacing inline explanations with
> stored procedures. A single `/workflow` command replaces 10+ tool calls.

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
| --- | --- | --- |
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
| --- | --- |
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
| --- | --- | --- |
| Commit & Push | `/commit-push` | After implementation, fix, or docs update |
| Update Progress | `/update-progress` | Before committing or switching tasks |
| System Status | `/status` | Connectivity or system health checks |
| **Sync Mail** | `/sync-mail` | **At session start**, before editing shared files, or to check for messages |

### Trigger Points — When to Suggest Workflows

**At Session Start:**
> 📬 *Run `/sync-mail` to check for messages from other agents and sync tasks.*

**After Implementation Completion:**
> 🎯 *"Implementation complete. Ready to run `/commit-push` to save changes?"*

**After Creating an Implementation Plan:**
> 📋 *"Plan created. Proceed with implementation, or update progress with
> `/update-progress`?"*

**When User Says "implement" or "do it":**

1. Execute the implementation
2. Then prompt: *"Done! Run `/commit-push` to commit and push these changes?"*

**Before Ending a Session:**
> 💾 *"Before we wrap up, should I run `/update-progress` to document
> current state?"*

**After Multiple File Changes:**
> 📦 *"Several files modified. Run `/update-progress` to stage and review
> before committing?"*

**Before Editing Shared Files:**
> 🔒 *Run `/sync-mail` to check file reservations before editing core files.*

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

**Rule:** If a task can be done by a skill/script, use it instead of
inline commands.

| Instead of... | Use Skill |
| --- | --- |
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
| --- | --- |
| Browser automation | Subagent has specialized browser tools |
| Long-running commands | Frees main context for other work |
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

```text
Task: Navigate to http://100.88.65.71:8123 and verify Home Assistant login
page loads

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
| --- | --- | --- |
| Workflows | `.agent/workflows/*.md` | Repeatable multi-step procedures |

| Shell scripts | `Scripts/*.sh` | System automation, deployments |
| Expect scripts | `Scripts/*.exp` | Interactive SSH/CLI automation |
| Python Utils | `.../Scripts/*.py` | Data processing, API calls |

---

## 10. Multi-Agent Coordination

> ⚠️ **Important:** Multiple agents may operate in this workspace
> simultaneously. Follow these rules to avoid conflicts and data loss.

### Agent Mail System

All agents communicate via a **shared Agent Mail server**. Use `/sync-mail` workflow at session start.

**Project Key (CRITICAL):** All agents use the same slug, NOT absolute paths:

```
PROJECT_KEY = "home-gonya-unified-system"
```

**Core Tools:**

| Tool | Purpose |
| --- | --- |
| `agent_mail_register_agent` | Register at session start |
| `agent_mail_fetch_inbox` | Check for messages |
| `agent_mail_send_message` | Send messages to other agents |
| `agent_mail_file_reservation_paths` | Reserve files before editing |
| `agent_mail_release_file_reservations` | Release reservations when done |
| `agent_mail_acknowledge_message` | Acknowledge important messages |

**Quick Registration:**

```python
agent_mail_register_agent(
  project_key="home-gonya-unified-system",
  program="opencode",      # or "claude-code", "codex"
  model="claude-sonnet-4",
  task_description="What you're working on"
)
```

**See also:** [`Agent_Context/agents/REGISTRY.md`](Agent_Context/agents/REGISTRY.md) for active agents.

### Transparency & Synchronization Rules

To ensure all agents and humans are aware of the current state of the system, follow these MANDATORY rules:

1. **Work Session Log**: Every significant change or session must be logged in `Agent_Context/WORK_SESSION_LOG.md`.
2. **Full System Lift**: Use `./full_sync.sh` (or the equivalent slash command) at the end of every major task. This script pulls code to all nodes, restarts necessary services, and broadcasts a status update to the entire agent network.
3. **Broadcast Every Sync**: When running a synchronization, always use the `agent_mail_send_message` tool to notify `@all` about the changes. This is handled automatically by the updated `full_sync.sh`.
4. **No Hidden State**: Avoid keeping modified files uncommitted or services in a custom state that isn't reflected in the repository configuration.

5. Check if file was recently modified: `git diff <file>` or `ls -la <file>`
6. If another agent is working on the same file, coordinate or wait
7. Never overwrite entire files — use targeted edits (`replace_file_content`)

**Avoid overwriting other agents' work:**

| ❌ Dangerous | ✅ Safe Alternative |
| --- | --- |
| `echo "..." > file` (overwrites) | `echo "..." >> file` (appends) |
| `write_to_file` Overwrite=true | `replace_file_content` targeted edits |

| `git reset --hard` | Ask user first, never auto-run |
| `git stash` (hides others' work) | `WIP: commit` instead |
| `rm -rf` on shared folders | Only delete files you created |

### Git Coordination

> ⚠️ **NEVER use `git stash`** in multi-agent environments. Stash is local-only
> and can cause other agents to lose access to uncommitted work.

**Safe Git Workflow:**

```bash
# Step 1: Commit YOUR changes first (even if WIP)
git add <your-files>
git commit -m "WIP: <agent-id> - <what you're working on>"

# Step 2: Now pull others' changes
git pull --rebase origin main

# Step 3: Continue work or push
```

**Why WIP commits instead of stash:**

| Approach | Visibility | Recovery | Multi-Agent Safe |
| --- | --- | --- | --- |
| `git stash` | ❌ Local only | ❌ Only by you | ❌ NO |
| `WIP: commit` | ✅ Pushed to remote | ✅ Any agent can see | ✅ YES |

**WIP Commit Format:**

```text
WIP: <agent-id> - <brief description>
WIP: mac-agent - updating AGENTS.md multi-agent rules
WIP: windows-agent - nodriver daemon implementation
```

**If you see uncommitted changes you didn't make:**

1. **DON'T stash them** — they belong to another agent
2. Check `git log --oneline -5` for recent WIP commits
3. Ask user: "I see uncommitted changes. Commit them as WIP before I proceed?"

**If rebase conflicts occur:**

1. Stop and notify user — don't force resolve
2. Show conflict files: `git diff --name-only --diff-filter=U`
3. Let user decide resolution strategy
4. **Never:** `git rebase --skip` or `git checkout --theirs`

**Commit scope rules:**

- Only commit files YOU modified in this session
- Use `git add <specific-files>` instead of `git add -A` if unsure
- Include agent identifier in commits: `feat(agent-mac): ...`
- Use `WIP:` prefix for incomplete work that needs to be saved

### Process Safety

**Never kill processes you didn't start:**

| ❌ Dangerous | ✅ Safe Alternative |
| --- | --- |
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
| --- | --- | --- |
| `CONTEXT_HANDOFF.md` | 🟡 Medium | Append only, don't delete sections |
| `AGENTS.md` | 🔴 High | Discuss with user first |
| `.env` files | 🔴 High | Never overwrite, only add keys |
| `package.json` | 🟡 Medium | Targeted edits only |

### Conflict Resolution

**If you detect another agent's work:**

1. **Don't overwrite** — your changes aren't more important
2. **Read their changes** — maybe they already did what you planned
3. **Append, don't replace** — add your section/changes below theirs
4. **Notify user** — "I see recent changes from another session. Proceed or
   review first?"

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

## 11. Merge Preparedness

> ⚠️ **Goal:** Ensure smooth synchronization between agents and minimize merge
> conflicts through proactive coordination.

### Intent Signaling

1. **Announce Major Changes**: Before starting a task that affects >5 files or
   core architecture, send a message via `mcp_agent_mail` (or update
   `Shared/intent.log` if mail is offline) describing your scope.
2. **Check for Intentions**: Before starting your own task, check for messages
   or logs from other agents to see if they are touching the same files.

### File Reservations (Leases)

1. **Acquire Leases**: For critical files (config, core logic), use
   `mcp_agent_mail` to acquire a lease.
2. **Respect Leases**: If a file has an active lease from another agent, DO NOT
   edit it unless you coordinate via messaging or wait for the lease to expire.

### Pre-Merge Quality Gates (UBS)

1. **UBS Mandatory**: Run `ubs <changed-files>` before EVERY commit. If UBS
   fails, you are NOT prepared to merge/commit.
2. **No Syntax Errors**: Never push code that breaks the build or has obvious
   syntax errors.

### Clean Commit History

1. **Squash WIP**: When moving from "Working" to "Done", prefer squashing your
   `WIP:` commits into a single clean `feat:` or `fix:` commit.
2. **Pull Before Merge**: Always `git pull --rebase` immediately before pushing
   to ensure you are merging on top of the latest state.

3. **Preparedness Check**: Before the final push, ask yourself:
   - Have I run UBS?
   - Have I notified other agents (if task is shared)?
   - Is my commit message descriptive?

---

## 12. Centralized Coordination Hub

### Service Centralization

1. **The Hub**: The `mcp_agent_mail` server and Beads task board MUST be
   hosted on the **Service Node** (`100.110.209.49`).
2. **Unified Access**: All agents connect to this single hub via Tailscale.
   This ensures that the message "source of truth" is never split across nodes.

### New Service Deployments

**Default host for new services:** `igor-gaming-1`

When deploying new services (AI Telegram Bot, new tools, etc.), use
`igor-gaming-1` as the default target unless there's a specific reason.

### Cross-Agent Communication (ACP Compliance)

1. **Mutual Messaging**:
   - **Antigravity** and **Kostya-Agent** have permanent permission to send/
     receive messages to each other via the shared mesh.
   - All communication should aim for **ACP** (Agent Communication Protocol)
     interoperability: structured payloads, clear intent, and async delivery.
2. **Mailbox Access**: Agents MUST check the **Service Node** (`100.88.65.71`)
   mailbox regularly to ensure coordination even if workstation is offline.
3. **Task Visibility**: The Beads task board on the Service Node is the shared
   source of truth for current project status.

### Emergency Handoff

1. **State Persistence**: All critical session state (WIP commits, Beads) must
   be pushed to a shared remote or host (`Shared/`) to ensure the other agent
   can take over if one node goes dark.

---

## 13. System Health & Maintenance

### Regular Checks

Perform these checks at the start of significant sessions:

1. **Disk Space**: `df -h` (Ensure >10% free)
2. **Docker Health**: `docker ps` (Ensure critical containers are UP)
3. **Network**: `tailscale status` (Ensure mesh connectivity)

### Log Rotation

- Check `nohup.out` and other log files.
- If >100MB, rotate or truncate: `> nohup.out`

---

---

*These rules ensure consistency across all agents operating in the
Unified System.*

````markdown
## UBS Quick Reference for AI Agents

UBS stands for "Ultimate Bug Scanner": **The AI Coding Agent's Secret Weapon:
Flagging Likely Bugs for Fixing Early On**


**Install:** `curl -sSL https://raw.githubusercontent.com/Dicklesworthstone/\
ultimate_bug_scanner/main/install.sh | bash`


**Golden Rule:** `ubs <changed-files>` before every commit. Exit 0 = safe.
Exit >0 = fix & re-run.


**Commands:**
```bash
ubs file.ts file2.py                    # Specific files (< 1s) — USE THIS
ubs $(git diff --name-only --cached)    # Staged files — before commit
ubs --only=js,python src/               # Language filter (3-5x faster)
ubs --ci --fail-on-warning .            # CI mode — before PR
ubs --help                              # Full command reference
ubs sessions --entries 1                # Tail the latest install session log
ubs .                                   # Whole project (ignores .venv, etc.)

```

**Output Format:**
```
⚠️  Category (N errors)
    file.ts:42:5 – Issue description
    💡 Suggested fix
Exit code: 1
```
Parse: `file:line:col` → location | 💡 → how to fix | Exit 0/1 → pass/fail

**Fix Workflow:**
1. Read finding → category + fix suggestion
2. Navigate `file:line:col` → view context
3. Verify real issue (not false positive)
4. Fix root cause (not symptom)
5. Re-run `ubs <file>` → exit 0
6. Commit

**Speed Critical:** Scope to changed files. `ubs src/file.ts` (< 1s) vs
`ubs .` (30s). Never full scan for small edits.


**Bug Severity:**
- **Critical** (always fix): Null safety, XSS/injection, async/await,
  memory leaks

- **Important** (production): Type narrowing, division-by-zero, resource leaks
- **Contextual** (judgment): TODO/FIXME, console logs

**Anti-Patterns:**
- ❌ Ignore findings → ✅ Investigate each
- ❌ Full scan per edit → ✅ Scope to file
- ❌ Fix symptom (`if (x) { x.y }`) → ✅ Root cause (`x?.y`)
````

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT
complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs
   follow-up

2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:

   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```

5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**

- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

## OpenAI ChatGPT Conversations Knowledge Base

**Location:** `Agent_Context/Knowledge_Base/OpenAI_Conversations/`

**Description:**

- **English:** Historical ChatGPT conversations imported from OpenAI export
- **Russian:** Исторические разговоры ChatGPT, импортированные из экспорта
  OpenAI

**Last Updated:** 2025-12-30 14:42:43

**Contents:** 50 conversation files

**Purpose:** Reference material for continuity, context, and learning from
past interactions.

---
