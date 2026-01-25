# VASER-Hub Architecture Overview

## Purpose
VASER-Hub is the centralized control plane for device management, secrets, and
execution. It provides a single, auditable gateway for all automated actions
initiated by the VASER Super-Admin.

## Core Responsibilities
- **Access Mediation:** Broker SSH/WinRM/API credentials without exposing raw
  secrets to the GPT layer.
- **Execution Safety:** Enforce approvals, confirmation tokens, and policy
  checks before critical actions.
- **Inventory & Metadata:** Maintain a live device inventory with tags, owners,
  and operational state.
- **Observability:** Emit structured audit logs and action traces for every
  request.

## Logical Components
1. **Gateway API**
   - Validates auth tokens and scopes.
   - Routes requests to execution backends.
2. **Credential Vault**
   - Stores encrypted SSH keys, API tokens, and cloud credentials.
   - Supports rotation policies and access logging.
3. **Execution Orchestrator**
   - Runs device commands using SSH/WinRM/HTTP adapters.
   - Applies rate limits and parallel execution controls.
4. **Policy Engine**
   - Determines if an action requires confirmation.
   - Applies environment restrictions (prod vs staging).
5. **Inventory Service**
   - Tracks device identity, status, and capability profiles.
6. **Audit & Telemetry Pipeline**
   - Captures action inputs, outputs, and error traces.
   - Feeds log analysis and incident response workflows.

## Data Flows
1. **Action Request**
   - GPT action → VASER-Hub Gateway → Policy Engine
2. **Execution**
   - Policy-approved → Orchestrator → Target device adapter
3. **Audit**
   - Audit logs → Log pipeline → Analytics and reporting

## Security Model
- Zero direct secrets in GPT prompts.
- Confirmation tokens required for privileged actions.
- Strict separation between read-only and write actions.
- Default-deny policy for unknown devices or untagged environments.

## Extension Points
- Add new adapters (e.g., Kubernetes, Proxmox, cloud IAM).
- Add custom approval workflows per environment.
- Integrate with SIEM or incident response systems.
