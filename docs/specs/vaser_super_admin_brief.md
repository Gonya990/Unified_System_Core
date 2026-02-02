# VASER Super Admin Role Pack

## 1) Role Instruction (System Prompt Draft)

**Role name:** VASER Super Admin

**System prompt:**

```
You are the Chief AI Network Administrator for the VASER platform.
You are responsible for the stability, security, and operability of the full ecosystem.
You can act through approved tools only (VASER-Hub, Home Assistant, local gateway, and cloud APIs).
You must follow safety confirmations for critical commands, preserve audit trails, and prioritize availability.
```

### Behavioral Guidelines
- Confirm user intent before any destructive or high-risk action.
- Prefer safe, reversible operations and staged rollouts.
- Always report what was changed, where, and how to roll back.
- Maintain an operational log summary for each session.

## 2) Custom GPT Actions (OpenAPI)

Use the manifest located at:
- `docs/specs/vaser_super_admin_openapi.yaml`

Action families included:
- Network: scan, device info, command execution, add/remove/reboot/configure.
- Home Assistant: service calls, state read/write, script execution.
- Local gateway: run/read/write.
- Cloud: Calendar (Google/iCloud), Mail (Gmail/Outlook), Storage (Drive/Yandex/Dropbox).
- Management: tasks, reminders, reports.
- Analytics: log collection, log analysis, project summaries, presentation generation.

## 3) VASER Control Hub (VASER-Hub) Architecture

### Core Components
- **API Gateway**: Receives GPT actions, performs authN/authZ, rate limiting.
- **Vault & Secrets**: Stores SSH keys, tokens, and endpoints per device.
- **Execution Orchestrator**: Dispatches actions to SSH/WinRM/API/HA/local runner.
- **Device Registry**: Inventory of network devices with tags and health metadata.
- **Audit & Telemetry**: Immutable action logs, metrics, and alerting.

### Data Flow
1. GPT issues action → VASER-Hub Gateway.
2. Gateway validates policy, requires confirmation if needed.
3. Orchestrator resolves credentials and executes via connector.
4. Results are logged (stdout/stderr, duration, exit code).
5. Telemetry published to monitoring dashboards and alerting.

### Connector Matrix
- **SSH**: Linux/macOS devices.
- **WinRM**: Windows nodes.
- **API**: Devices with REST/GraphQL/SDK interfaces.
- **Home Assistant**: Smart home entities and scripts.
- **Local Gateway**: Files and utilities via `/local/*`.

## 4) Security & Safety Policy

### Confirmation Levels
- **Level 0 (No confirmation)**: Read-only queries, status checks.
- **Level 1 (Soft confirmation)**: Non-destructive automation (restart service, rescan).
- **Level 2 (Hard confirmation)**: Reboot devices, rotate keys, firmware updates.
- **Level 3 (Locked)**: Factory reset, delete backups, mass delete, firewall changes.

### Critical Nodes
- Core router/gateway, identity provider, secrets vault, storage cluster.
- Any device tagged `critical` in the registry.

### Automation Rules
- Automate read-only and remediation tasks.
- Never automate destructive actions without explicit confirmation.
- Always request maintenance windows for firmware updates.

### Backup Policy
- Daily config backups for routers, switches, HA, and VASER-Hub.
- Keep 30-day rolling snapshots and 3 monthly archives.
- Validate restore procedures quarterly.

## 5) Presentation Action Guidance

**Action:** `generate_presentation(content_json)` → `pptx/pdf`

The content JSON should include:
- Title slide (product name, version, owner)
- Architecture diagram blocks (Hub, Connectors, Security)
- Roadmap and milestones
- Business plan (TAM/SAM/SOM, pricing, GTM)

## 6) Productization Plan (Mass Market)

### Phase 1: MVP (0–3 months)
- Core VASER-Hub with network inventory and command execution.
- Home Assistant integration and local gateway.
- Minimal audit logs and role-based access.

### Phase 2: Pro (3–6 months)
- Cloud integrations (calendar, mail, storage).
- Policy engine with confirmation levels.
- Reporting and analytics dashboards.

### Phase 3: Enterprise (6–12 months)
- Multi-tenant management, SSO, advanced compliance.
- High availability deployment, SLA monitoring.
- SDKs for third-party extensions.

## 7) Presentation Structure (Suggested)

1. Title & Vision
2. Problem Statement
3. Solution Overview (VASER Super Admin)
4. Architecture (VASER-Hub + Connectors)
5. Security & Safety Policy
6. Key Use Cases (network ops, smart home, assistants)
7. Product Roadmap
8. Business Model & Pricing
9. Go-to-Market Strategy
10. Team & Next Steps
