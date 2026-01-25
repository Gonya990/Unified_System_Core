# VASER Control Hub Architecture

## Component diagram

```
+--------------------------------------------------------------+
|                       VASER Control Hub                      |
|  - command intake API                                         |
|  - policy engine + routing                                   |
+---------------------------+----------------------------------+
                            |
                            v
+---------------------------+----------------------------------+
|                      credential vault                        |
|  - SSH keys                                                   |
|  - API tokens                                                 |
|  - endpoint registry                                          |
+---------------------------+----------------------------------+
                            |
                            v
+---------------------------+----------------------------------+
|                     execution agents                         |
|  - SSH/WinRM/API/Home Assistant adapters                      |
|  - task runner + retries                                      |
+---------------------------+----------------------------------+
                            |
                            v
+---------------------------+----------------------------------+
|                         audit log                             |
|  - immutable event stream                                     |
|  - correlation IDs + metadata                                 |
+--------------------------------------------------------------+
```

## Trust boundaries and data flow

1. **Command intake (untrusted input)**
   - External commands enter the VASER Control Hub through authenticated APIs.
   - Input validation, schema checks, and request signing occur at the edge.

2. **Policy check (trusted enforcement zone)**
   - Commands are evaluated against allow/deny policies, scoped permissions, and user confirmations.
   - Sensitive actions require explicit approval before execution.

3. **Execution (controlled access zone)**
   - Approved commands are routed to execution agents via least-privilege credentials.
   - Agents execute tasks on SSH/WinRM/API/Home Assistant targets.

4. **Audit (immutable record zone)**
   - Every command, decision, and result is written to the audit log.
   - Correlation IDs link intake → policy decision → execution → outcome.

## Credential management approach

- **Storage**: All secrets live in the credential vault with envelope encryption.
- **Access**: Execution agents receive short-lived session credentials.
- **Rotation**: Automated rotation for SSH keys and tokens on fixed schedules or on compromise.
- **Scoping**: Credentials are scoped per device/service with least-privilege permissions.
- **Revocation**: Immediate revoke on suspicious activity or policy violations.

## Failure modes and rollback strategy

- **Command rejection**: Policy check denies commands; events logged in the audit log.
- **Credential failure**: Failed auth triggers re-issue from credential vault or rotation.
- **Execution failure**: Agents retry with exponential backoff, then fail fast and record outcome.
- **Partial execution**: Use compensating actions (rollback scripts) per device/service.
- **Hub outage**: Fail closed; no execution without policy enforcement and audit logging.
- **Audit backlog**: Queue locally with backpressure, then flush when storage recovers.

## Data flow summary

Command intake → policy check → execution → audit
