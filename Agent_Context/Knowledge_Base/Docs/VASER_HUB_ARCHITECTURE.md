# VASER Control Hub Architecture

## Purpose
VASER Control Hub is the single entry point for GPT actions, enforcing access control, auditing, and safe execution across the network, Home Assistant, and cloud services.

## Core Components
1. **VASER Control Hub API**
   - OpenAPI action surface for the Custom GPT.
   - Handles authentication, rate limits, and policy enforcement.
2. **VASER Vault**
   - Encrypted secrets store for SSH keys, API tokens, and endpoint metadata.
   - References are passed to actions via `credential_ref`.
3. **Device Executors**
   - SSH/WinRM/API runners for servers, PCs, and IoT devices.
   - Supports safe command execution, reboot, and configuration workflows.
4. **Home Assistant Bridge**
   - Dedicated module for `ha.service_call`, `ha.get_state`, `ha.set_state`, and `ha.execute_script`.
5. **Python Gateway**
   - `/local/run`, `/local/read`, `/local/write`, `/local/reminder` for local machine operations.
6. **Cloud Connectors**
   - Google Calendar, iCloud, Gmail/Outlook, Google Drive, Yandex Disk, Dropbox.
7. **Observability & Logs**
   - Central logging, metrics, and alerting for every action.
   - Log bundles provided to `collect_logs` and `analyze_logs`.

## Execution Flow
1. GPT sends an action request to VASER Hub.
2. Hub validates credentials, scope, and confirmation requirements.
3. Hub dispatches to the relevant executor or connector.
4. Results and audit logs are stored and returned to GPT.

## Security Boundaries
- All secrets remain in VASER Vault. GPT receives references only.
- Critical actions are gated by confirmation policy.
- Each executor has minimal privileges for its assigned scope.

## Data Contracts
- OpenAPI schema defines all action inputs/outputs.
- Each action produces a correlation ID for traceability.

## Failure Handling
- On failure, return a structured error with remediation hints.
- For partial failures, include which targets succeeded and which failed.

## Scalability Considerations
- Horizontal scaling of executors per protocol.
- Queue-based execution for long-running tasks.
- Cache read-only state where applicable (inventory, HA state).
