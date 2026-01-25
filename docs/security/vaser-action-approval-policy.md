# VASER Action Approval & Safety Policy

## Purpose
Define how VASER actions are classified, approved, executed, and audited to keep the
platform stable and secure while enabling automation.

## Scope
Applies to all VASER actions executed via VASER-Hub, GPT integrations, CLI/SSH/WinRM,
Home Assistant services, and any API-connected device or cloud service.

## Action Risk Tiers

### Tier 0 — Read-Only (Non-Destructive)
Actions that do **not** modify state and cannot affect availability or data integrity.
Examples:
- `scan_network`, `get_device_info`, `ha.get_state`
- Listing files, reading logs, querying status APIs

**Approval:** No explicit confirmation required unless targeting a protected node.

### Tier 1 — Destructive / State-Changing
Actions that **modify** configuration, data, or availability and could cause
service impact if misused.
Examples:
- `add_device`, `remove_device`, `configure_device`, `reboot_device`
- `run_command` that changes system state
- `ha.service_call` or `ha.set_state` that changes devices
- Cloud actions that create, delete, or overwrite data

**Approval:** Explicit user confirmation required (see Approval Flows).

## Required User Confirmation Flows

### Standard Confirmation (Tier 1)
1. **Summarize the action**: include target, intent, and expected impact.
2. **Provide the exact approval phrase** for the user to copy/paste.

**Prompt Template:**
> This action will **modify system state** on **<target>**: <action summary>.
> If you approve, reply with: **APPROVE VASER ACTION <action_id>**.

**Approval Phrase:**
- Must match exactly: `APPROVE VASER ACTION <action_id>`
- `<action_id>` is a short unique identifier generated per action.

### Elevated Confirmation (Protected Targets)
For any action on a protected node/command, require **step-up confirmation**:
- Repeat the summary with a warning banner.
- Require the phrase: `APPROVE VASER PROTECTED ACTION <action_id>`.
- Require confirmation of backup status (see Backups).

### No Silent Retries
If an action fails, **do not** automatically retry without renewed approval.

## Protected Nodes & Commands

### Protected Nodes
Actions on these nodes always require elevated confirmation:
- **VASER-Hub / Vaser Control Hub**
- Core routing, firewall, or gateway devices
- Primary storage nodes or backup repositories
- Production Home Assistant core instance

### Protected Commands (Examples)
Any command matching these patterns is protected:
- Destructive filesystem: `rm -rf`, `mkfs`, `dd`, `wipefs`, `truncate`
- Availability impact: `shutdown`, `reboot`, `systemctl stop`, `service stop`
- Network risk: `iptables -F`, `nft flush`, `ufw disable`, `ip link set down`
- Container/VM destruction: `docker system prune`, `docker rm -f`, `qm destroy`, `virsh destroy`
- Cluster changes: `kubectl delete`, `etcdctl del`

If a command resembles a protected pattern, treat it as protected even if it is
not an exact match.

## Backup Requirements (Protected Actions)
Before executing a protected action:
1. Confirm the most recent backup/snapshot time (must be < 24h old).
2. Create a fresh backup if required:
   - Configuration exports for network devices.
   - Home Assistant snapshot.
   - VM/container snapshot for compute nodes.
3. Record backup identifiers in the audit log.

## Audit Logging Requirements
Every Tier 1 or protected action must be logged with:
- Timestamp (UTC)
- Requesting user and execution agent
- Target node/service and environment
- Action name, parameters, and risk tier
- Approval phrase and action_id
- Backup confirmation status and snapshot IDs (if required)
- Execution result (success/failure) and error details

Logs must be:
- Immutable (append-only)
- Retained for at least 90 days
- Accessible for incident review and compliance

## Enforcement Summary
- **Default-deny** for unknown or ambiguous actions.
- **Tier 0** actions may run without confirmation unless protected.
- **Tier 1** actions always require explicit user approval.
- **Protected** actions require elevated approval and backup verification.
