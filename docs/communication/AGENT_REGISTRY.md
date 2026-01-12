# Agent Registry & Source of Truth

## Source of Truth

The **Agent Mail Server** (`http://100.110.209.49:8765`) is the
**Single Source of Truth (SSOT)** for the list of active agents, their
statuses, and their inbox states.

- **Dynamic Registry**: Agents register themselves at runtime using the
  `agent_mail_register_agent` tool or the `register()` method in the SDK.
- **Verification**: To see the current list of valid agents, use the CLI
  command:

  ```bash
  python3 Projects/AI_Core/src/agent_mail_client.py agents
  ```

- **Static Files are Secondary**: Any lists in `AGENTS.md`,
  `docs/AGENT_MAIL_ONBOARDING.md` or other files are for documentation purposes
  only and may be out of sync. Always query the server for the live list.

## Naming Convention

- **Format**: `CamelCase` (e.g., `VioletCastle`, `PinkLake`, `FuchsiaCat`,
  `Antigravity`).
- **Assignment**: Agent names are assigned by the user or the Lead Architect
  (Kostya).
- **Uniqueness**: Names must be unique within the `Unified_System_Core` project
  scope.

## Registration Process

1. **New Agents**: Must call `register` upon startup.
2. **Session**: Registration creates an active session.
3. **Task Description**: Agents should update their `task_description` to
   reflect their current focus (e.g., "Monitoring inbox", "Building Feature X").
