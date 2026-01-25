# VASER Control Hub (VASER-Router) Architecture

## Purpose
VASER Control Hub is the unified control plane for device management and API execution. It mediates all privileged operations requested by the Super Admin GPT.

## Core Components
1. **Command Gateway**
   - Validates OpenAPI action requests.
   - Applies policy checks and user-confirmation gates.
   - Routes tasks to the correct executor (SSH/WinRM/API/HA).

2. **Credential Vault**
   - Stores SSH keys, API tokens, and service endpoints.
   - Provides short-lived access tokens scoped to the requested action.
   - Logs every credential retrieval for audit.

3. **Executor Pool**
   - SSH executor for Linux/network devices.
   - WinRM executor for Windows hosts.
   - API executor for vendor endpoints.
   - Home Assistant executor for HA services/scripts.

4. **Telemetry & Audit**
   - Captures command intent, target, and result.
   - Streams health signals and device state.
   - Exposes alerts to monitoring dashboards.

## Data Flow
1. GPT issues OpenAPI action request.
2. Control Hub validates schema + policy.
3. Credential Vault provides scoped access.
4. Executor runs command.
5. Audit logs stored; result returned to GPT.

## Security Boundaries
- GPT cannot access credentials directly.
- All privileged commands are mediated by Control Hub.
- Critical actions require explicit user confirmation.

## Integration Points
- **Network:** scan, device lifecycle, command execution.
- **Home Assistant:** service calls and scripts.
- **Local Gateway:** /local/run, /local/read, /local/write.
- **Cloud Services:** calendar, mail, storage, tasks.
