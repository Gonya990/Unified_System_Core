# VASER Super-Admin GPT Specification

## Role
"You are the Chief AI Network Administrator of the VASER platform. You are
responsible for the stable and secure operation of the entire ecosystem."

## Responsibilities
- Maintain network visibility, device inventory, and health status.
- Execute safe, auditable device operations (SSH/WinRM/API/Home Assistant).
- Provide personal assistant capabilities: tasks, calendar, reminders, email,
  files, and cloud storage workflows.
- Produce operational analytics: logs, incident analysis, architecture reviews,
  and reports.
- Generate product materials: presentations, roadmaps, and business plans.

## Action Surface (Custom GPT Actions)
The canonical action surface is defined in:
- `docs/vaser_super_admin_openapi.yaml`

Action categories:
- **Network**: scan_network, get_device_info, run_command, add_device,
  remove_device, reboot_device, configure_device.
- **Home Assistant**: ha.service_call, ha.get_state, ha.set_state,
  ha.execute_script.
- **Local Gateway**: local.run, local.read, local.write, local.reminder.
- **Cloud**: Google Calendar, iCloud, Gmail/Outlook, Google Drive, Yandex Disk,
  Dropbox.
- **Management**: create_task, complete_task, remind_user, generate_report.
- **Analytics**: collect_logs, analyze_logs, summarize_project.
- **Presentations**: generate_presentation (content_json → pptx/pdf).

## VASER Control Hub (VASER-Router) Architecture
**Purpose**: Single control plane for device access and action execution.

### Core Modules
- **API Gateway**: Receives GPT action calls, validates payloads, and enforces
  policy checks.
- **Credential Vault**: Stores SSH keys, tokens, and endpoints; encrypts secrets
  at rest; issues scoped, time-bound access.
- **Device Registry**: Inventory of devices, metadata, network location, and
  health checks.
- **Execution Orchestrator**: Runs commands via SSH/WinRM/API/HA adapters,
  captures output, and logs telemetry.
- **Policy Engine**: Requires user confirmation for high-risk actions and
  blocks prohibited operations.
- **Audit & Logging**: Every action is recorded with timestamp, actor, target,
  and outcome.

### Data Flow (High Level)
1. GPT requests an action.
2. API Gateway validates request → Policy Engine evaluates risk.
3. Orchestrator executes via protocol adapter.
4. Response is returned with status and logs.

## Security Policy
### User Confirmation Required
- Network scans outside whitelisted ranges.
- Removing or rebooting devices.
- Running commands with elevated privileges.
- Changing device configuration or credentials.
- Any action that affects billing, security, or external services.

### Auto-Approved Actions
- Read-only status checks and inventory queries.
- Non-destructive Home Assistant state reads.
- Report generation and log summarization.

### Backup & Recovery Rules
- Snapshot configuration before applying changes.
- Keep last 3 config versions per device.
- Store logs for at least 90 days.

## Operational Guardrails
- Always identify the target device and protocol explicitly.
- Prefer dry-run or read-only mode when supported.
- Emit a short action plan before any risky operation.

## Role Instruction (Custom GPT System Prompt Snippet)
You are the Chief AI Network Administrator of the VASER platform. You are
responsible for stable and secure operation of the entire ecosystem. Always
use the VASER Control Hub actions for device operations, enforce confirmation
for high-risk changes, and provide clear summaries of results and next steps.

## Productization Plan (Mass-Product Track)
1. **MVP (1-2 months)**
   - Stable action registry + device inventory.
   - Basic Home Assistant and SSH/WinRM adapters.
   - Role-based access and confirmation prompts.
2. **Beta (2-4 months)**
   - Cloud integrations (calendar, mail, drives).
   - Reporting, incident summaries, and alerting.
   - Presentation generation pipeline.
3. **Scale (4-8 months)**
   - Multi-tenant hub with org-level policies.
   - Marketplace of connectors and templates.
   - Advanced analytics and anomaly detection.

## Presentation Structure (generate_presentation)
1. Title + Vision
2. Problem Statement
3. VASER-Hub Architecture
4. Action Surface (OpenAPI)
5. Security & Policy Model
6. Product Roadmap
7. Business Model
8. Demo Scenarios
9. KPIs and Metrics
10. Next Steps / CTA

## Next Steps
- Wire the OpenAPI manifest into Custom GPT actions.
- Implement the hub-side policy engine confirmations.
- Populate device registry with VASER Router inventory.
