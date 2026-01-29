# Vibe Kanban Skill

## Overview

Vibe Kanban is an **AI coding agent orchestration platform** that helps plan, review, and safely execute AI-assisted coding tasks. Every task runs in an isolated git worktree, preventing agents from interfering with each other or your main branch.

## When to Use This Skill

- Managing coding tasks across projects
- Orchestrating AI coding agents (Claude Code, Codex, Gemini, Cursor, OpenCode, etc.)
- Planning complex features by breaking them into tasks
- Starting isolated workspace sessions for task execution

## Available MCP Tools

| Tool | Purpose | Required Params | Optional Params |
|------|---------|-----------------|-----------------|
| `vibe_kanban_list_projects` | List all projects | - | - |
| `vibe_kanban_list_repos` | List repos in a project | `project_id` | - |
| `vibe_kanban_list_tasks` | List tasks in a project | `project_id` | `status`, `limit` |
| `vibe_kanban_create_task` | Create a new task | `project_id`, `title` | `description` |
| `vibe_kanban_get_task` | Get task details | `task_id` | - |
| `vibe_kanban_update_task` | Update a task | `task_id` | `title`, `description`, `status` |
| `vibe_kanban_delete_task` | Delete a task | `task_id` | - |
| `vibe_kanban_start_workspace_session` | Start working on a task | `task_id`, `executor`, `repos` | `variant` |

### Task Status Values
- `todo` - Not started
- `inprogress` - Currently being worked on
- `inreview` - Ready for review
- `done` - Completed
- `cancelled` - Cancelled

### Supported Executors
- `CLAUDE_CODE` - Claude Code CLI
- `CODEX` - OpenAI Codex CLI
- `GEMINI` - Google Gemini
- `CURSOR_AGENT` - Cursor Agent
- `OPENCODE` - OpenCode
- `AMP` - Amp
- `DROID` - Droid
- `COPILOT` - GitHub Copilot

## Common Workflows

### Workflow 1: List and Review Tasks

```
1. List all projects
   → vibe_kanban_list_projects()

2. List tasks in a project (optionally filter by status)
   → vibe_kanban_list_tasks(project_id="...", status="todo")

3. Get details of a specific task
   → vibe_kanban_get_task(task_id="...")
```

### Workflow 2: Create Tasks from a Plan

When planning a feature, break it into atomic tasks:

```
1. List projects to find the target project
   → vibe_kanban_list_projects()

2. Create individual tasks for each step
   → vibe_kanban_create_task(
       project_id="...",
       title="Implement user authentication",
       description="Add JWT-based auth with login/logout endpoints..."
     )

3. Repeat for each task in the plan
```

### Workflow 3: Start a Task Session

Launch an AI coding agent to work on a task:

```
1. Get the task and project details
   → vibe_kanban_get_task(task_id="...")
   → vibe_kanban_list_repos(project_id="...")

2. Start workspace session
   → vibe_kanban_start_workspace_session(
       task_id="...",
       executor="CLAUDE_CODE",
       repos=[{"repo_id": "...", "base_branch": "main"}],
       variant="DEFAULT"  # or "PLAN" for planning mode
     )
```

### Workflow 4: Update Task Status

Track progress by updating task status:

```
→ vibe_kanban_update_task(task_id="...", status="inprogress")
→ vibe_kanban_update_task(task_id="...", status="inreview")
→ vibe_kanban_update_task(task_id="...", status="done")
```

## Agent Variants

When starting a workspace session, you can specify a `variant`:

| Variant | Use Case |
|---------|----------|
| `DEFAULT` | Standard execution mode |
| `PLAN` | Planning mode - agent explores and plans without executing |
| `FLASH` | Faster model for simple tasks (Gemini) |
| `HIGH` | High reasoning effort for complex problems (Codex) |

## Best Practices

1. **Atomic Tasks**: Create small, focused tasks rather than large multi-step ones
2. **Clear Descriptions**: Include acceptance criteria and context in task descriptions
3. **Use Planning Mode**: For complex features, start with a PLAN variant to explore before implementing
4. **Review Before Merge**: Always review agent-generated code diffs before merging to base branch
5. **Status Tracking**: Keep task statuses updated to maintain project visibility

## Example: Full Feature Planning Flow

```
# 1. Find the project
projects = vibe_kanban_list_projects()
project_id = <select appropriate project>

# 2. Create a planning task
planning_task = vibe_kanban_create_task(
    project_id=project_id,
    title="Plan: User Dashboard Feature",
    description="Explore codebase and create detailed implementation plan for user dashboard"
)

# 3. Start planning session
vibe_kanban_start_workspace_session(
    task_id=planning_task.id,
    executor="CLAUDE_CODE",
    repos=[{"repo_id": "...", "base_branch": "main"}],
    variant="PLAN"
)

# 4. After planning completes, create implementation tasks
vibe_kanban_create_task(project_id, title="Add dashboard API endpoints", description="...")
vibe_kanban_create_task(project_id, title="Create dashboard UI components", description="...")
vibe_kanban_create_task(project_id, title="Add dashboard tests", description="...")

# 5. Start each task with DEFAULT variant for implementation
```

## Reference

- [GitHub Repository](https://github.com/BloopAI/vibe-kanban)
- [Official Documentation](https://docs.vibe-kanban.dev)
