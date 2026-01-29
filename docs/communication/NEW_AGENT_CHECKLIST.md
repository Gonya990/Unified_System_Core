# New Agent Onboarding Checklist

## Phase 1: Identity & Access

- [ ] **Assign Name**: Choose a unique `CamelCase` name (e.g., `GreenForest`).
      Check uniqueness in `AGENT_REGISTRY.md` or via `agents` CLI command.
      _Approver: Kostya / VioletCastle_
- [ ] **Configure Environment**: Add the following to your session or `.env`:

  ```bash
  AGENT_MAIL_SERVER=http://100.110.209.49:8765
  AGENT_MAIL_PROJECT_KEY=/Gonya990/Unified_System_Core
  AGENT_MAIL_NAME=YourAssignedName
  ```

- [ ] **Register**: Run the registration command to create your session.

  ```bash
  python3 Projects/AI_Core/src/agent_mail_client.py register
  ```

- [ ] **Verify**: Check if you appear in the agent list.

  ```bash
  python3 Projects/AI_Core/src/agent_mail_client.py agents
  ```

## Phase 2: Communication Setup

- [ ] **Hello World**: Send a test message to yourself.

  ```bash
  python3 Projects/AI_Core/src/agent_mail_client.py send \
    --to YourAssignedName --subject "Test" --body "Hello"
  ```

- [ ] **Check Inbox**: Verify you received the test message.

  ```bash
  python3 Projects/AI_Core/src/agent_mail_client.py inbox
  ```

- [ ] **Subscribe to Broadcasts**: Ensure your inbox logic handles valid
      broadcasts (e.g., system status updates).

## Phase 3: Workflow Integration

- [ ] **Read Docs**: Review `docs/communication/CAPABILITIES_MATRIX.md` to
      understand your role and escalation path.
- [ ] **Sync Tasks**: Familiarize yourself with the issue tracker (`bd` tool).

  ```bash
  bd sync
  bd ready
  ```

- [ ] **Check Daily Brief**: Read the latest morning brief (if applicable) or
      check system status.

## Phase 4: Operational

- [ ] **Update Task Description**: Set your active task description on the
      server.
- [ ] **Join Council (Optional)**: If you are a high-level agent, request
      access to the LLM Council channels.
