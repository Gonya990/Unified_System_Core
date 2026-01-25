# VASER-Hub Architecture

## Overview
VASER-Hub is the **central control plane** for device management, credential storage, and secure action execution. It receives intents from the Super Admin GPT, validates permissions, and executes operations across network devices, Home Assistant, and cloud services.

## Core Components
1. **API Gateway**
   - Receives OpenAPI action requests.
   - Handles authentication, rate limits, and audit logging.
2. **Credential Vault**
   - Stores SSH keys, API tokens, WinRM credentials, and cloud secrets.
   - Enforces scope-based access and rotation policies.
3. **Execution Orchestrator**
   - Routes tasks to appropriate adapters (SSH, WinRM, API, HA).
   - Runs pre-flight checks and safety guardrails.
4. **Device Inventory**
   - Maintains device metadata, tags, reachability, and last-seen data.
   - Supports dynamic discovery and manual registration.
5. **Policy Engine**
   - Evaluates approvals, RBAC rules, and sensitive command filters.
   - Flags high-risk operations for confirmation.
6. **Observability Stack**
   - Centralized logs, metrics, and traces.
   - Incident reports and automatic diagnostics.

## Data Flow
1. Super Admin GPT issues an action request.
2. API Gateway validates authentication and forwards to Policy Engine.
3. Policy Engine checks RBAC and approval requirements.
4. Execution Orchestrator performs pre-flight checks and calls adapters.
5. Results and logs are written to Observability and returned to the GPT.

## Integration Adapters
- **SSH Adapter**: Remote shell commands for Linux/macOS devices.
- **WinRM Adapter**: Windows remote commands and reboots.
- **API Adapter**: Vendor-specific device APIs.
- **Home Assistant Adapter**: Service calls and state management.
- **Cloud Adapter**: Calendar, mail, and storage operations.

## Safety Guardrails
- Mandatory confirmations for protected actions.
- Dry-run support for configuration changes.
- Safe timeouts and rollback suggestions.
- Secrets never returned in responses.

## Deployment Notes
- Run VASER-Hub as a hardened service on trusted infrastructure.
- Isolate adapters in separate containers or sandboxed workers.
- Enable encrypted transport (TLS) for all API calls.
