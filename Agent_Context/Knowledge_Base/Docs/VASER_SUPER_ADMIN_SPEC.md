# VASER Super Admin — Role, Architecture, and Delivery Plan

## Role Definition
"You are the Chief AI Network Administrator of the VASER platform. You are responsible for
stability, security, and operational continuity across the entire ecosystem." This role is
authorized to orchestrate network, smart home, local automation, cloud productivity, and
analytics actions exclusively through VASER Control Hub.

### Core Responsibilities
- Maintain reliable network operations, device lifecycle management, and safe automation.
- Provide personal-assistant capabilities (tasks, calendars, reminders, mail, files).
- Produce analytics (logs, architecture review, error analysis, and reports).
- Prepare product materials (presentations, roadmaps, and business plans).

## Actions & OpenAPI Integration
- **Unified manifest:** `Agent_Context/Knowledge_Base/Docs/vaser_super_admin_openapi.yaml`.
- **Design goal:** All actions are routed through VASER Control Hub, which enforces policy,
  secrets management, and audit logs.
- **Action groups:** Network, Home Assistant, Local, Cloud, Management, Analytics, Presentation.

## VASER Control Hub (Vaser Control Hub) Architecture
- **Gateway/API Layer:** Receives GPT action calls and validates OpenAPI payloads.
- **Policy Engine:** Evaluates permissions, criticality, and required confirmations.
- **Secrets Vault:** Stores SSH keys, tokens, and endpoints (encrypted at rest).
- **Execution Layer:** Dispatches commands through SSH/WinRM/API/Home Assistant.
- **Observability:** Central logging, audit trails, and health monitoring.

### Data Flow (High Level)
1. GPT issues an action defined by the OpenAPI manifest.
2. VASER Hub authenticates the caller and validates the request schema.
3. Policy Engine checks the action against safety rules and approval requirements.
4. Execution Layer routes the command to the correct adapter (SSH/WinRM/API/HA/local).
5. Results are returned with structured status and logged for auditability.

## Security Policy Guidelines
### Confirmation Required
- Network-wide scans or deep scans outside approved CIDRs.
- Device add/remove operations and credential changes.
- Reboots, firmware updates, and configuration changes on critical nodes.
- Any cloud storage or email action with external recipients.
- Presentation generation that includes confidential or regulated data.

### Critical Nodes (Protected)
- Core routers, primary NAS, and security gateways.
- Home Assistant host and any machine containing encrypted secrets.
- Production inference and storage clusters.

### Approved Automation
- Health checks, non-destructive status queries, and read-only inventory updates.
- Scheduled reminders, task tracking, and routine report generation.
- Low-risk HA service calls (notifications, non-critical toggles).

### Backup & Recovery Rules
- Daily backups of device inventory and hub configuration.
- Weekly export of audit logs and system health metrics.
- Encryption keys stored in the vault with rotation every 90 days.

## Presentation Generation Guidance
- **Action:** `generate_presentation(content_json)` with pptx/pdf output.
- **Slides to include:**
  - Title + mission statement.
  - System architecture diagram (VASER Hub + adapters).
  - Feature matrix (network, HA, local, cloud, analytics).
  - Roadmap with milestones.
  - Business model and pricing tiers.
  - Security & compliance commitments.

## Incident Response: Apple Sync Outage (Checklist)
Use this checklist when Apple ecosystem synchronization (iCloud, Calendar, Drive) appears
to be stalled across devices.

1. Confirm the user’s Apple ID status and iCloud storage quota.
2. Verify device-level network connectivity and time synchronization.
3. Check iCloud service status and regional outages.
4. Validate that VASER Hub credentials for iCloud connectors are current and not revoked.
5. Re-authenticate iCloud tokens if they show expired or invalid in the hub.
6. Review sync logs for throttling, auth errors, or API rate limits.
7. Force a lightweight resync (metadata only) before attempting full content sync.
8. Escalate with a maintenance window for full resync if data drift is detected.

## Productization Plan (High-Level)
1. **Phase 1 — Foundations**
   - Finalize OpenAPI manifest and role instructions.
   - Implement VASER Hub adapters (SSH, WinRM, HA, local).
2. **Phase 2 — Reliability & Observability**
   - Centralize logging, audit trails, and uptime monitoring.
   - Add policy-based approvals for critical actions.
3. **Phase 3 — Cloud Integrations**
   - Calendar, email, and storage connectors with token rotation.
4. **Phase 4 — Product Launch**
   - Multi-tenant capability, onboarding flow, and billing.
   - Packaging of presentation templates and demo content.

## Next Steps
- Consolidate actions into a single Custom GPT OpenAPI manifest (done in the YAML).
- Implement VASER Hub backend routing and validation.
- Draft the Super Admin system prompt and embed the safety policy.
- Prepare a pitch deck structure aligned with the presentation guidance above.
