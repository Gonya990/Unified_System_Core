# Agent Capabilities Matrix & Escalation Rules

## Capabilities Matrix

<!-- markdownlint-disable MD013 -->
| Agent Role | Example IDs | Core Capabilities | Tool Access Scope |
| :--- | :--- | :--- | :--- |
| **Lead Architect** | `VioletCastle`, `Kostya` | System Design, Task Assignment, Policy Definition | **Level 5**: Full System + Admin |
| **Senior Dev** | `PinkLake`, `BlueLake` | Complex Refactoring, Feature Implementation, Optimization | **Level 4**: Read/Write, Terminal, Git |
| **Assistant** | `Antigravity`, `Claude` | Quick Fixes, Documentation, Research | **Level 3**: Read/Write, Limited Terminal |
| **Monitor** | `FuchsiaCat` | Health Checks, Log Analysis, Alerting | **Level 2**: Read-Only (mostly), Status Checks |
| **Bot/Automaton** | `TelegramBot`, `Scheduler` | Specific Automated Tasks | **Level 1**: APIs, Specific Scripts |
<!-- markdownlint-enable MD013 -->

## Escalation Rules

### 🔴 Escalate to Lead Architect (VioletCastle)

Stop execution and request guidance via Agent Mail
(`send --to VioletCastle --importance high`) if:

1. **Architecture Deviation**: You need to change the system architecture,
    folder structure, or core technologies.
2. **Security Risk**: You detect exposed credentials, unsecured endpoints, or
    suspicious activity.
3. **Resource Conflict**: You cannot obtain a lock on a critical file needed
    for a high-priority task.
4. **Workflow Deadlock**: Circular dependencies prevent progress.

### 🟡 Escalate to User (Human)

Pause and ask for permission/input if:

1. **Destructive Actions**: Deleting non-temp files, wiping databases, or
    irreversible git operations.
2. **Ambiguity**: The task description is vague, and assumptions could lead to
    wasted effort.
3. **Auth Required**: You need 2FA codes, login credentials, or OAuth tokens.
4. **Financial Impact**: Subscribing to services or provisioning paid
    infrastructure.

### 🟢 Automated Error Handling

1. **Retry**: For network timeouts (HTTP 5xx), retry with exponential backoff
    (max 3 attempts).
2. **Log**: Record all errors to `logs/` with context.
3. **Notify**: If a background job fails permanently, send a message to the
    team or User.
4. **Fallback**: If a primary tool fails (e.g., search), try a predefined
    alternative or skip the non-critical step.
