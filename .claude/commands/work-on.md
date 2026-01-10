---
description: Start working on a Beads issue and update Agent Mail status
---
# /work-on <issue_id> <optional_note>

This command synchronizes the status of a task across **Beads** and **Agent Mail**.

## Workflow

1.  **Update Beads**: Set the issue status to `in_progress`.
2.  **Update Agent Mail**: Update the billboard with the current task description.

## Execution Pattern

When user says `/work-on <ID>`, the agent should:

1.  Run `bd update <ID> --status in_progress`.
2.  Run `mcp__mcp-agent-mail__register_agent` with:
    - `project_key`: (from .env or current dir)
    - `task_description`: "Working on [ID]: [Title] - [optional_note]"
3.  Send a coordination message if needed.

---
