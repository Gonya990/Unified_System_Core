# VASER Security Policy

## Purpose
This policy defines the safety, authorization, and audit rules for VASER automation, including the VASER-Router (Vaser Control Hub) and its connected tools.

## Core Principles
- **Least privilege**: Actions must use the minimum scope required to complete the task.
- **Human-in-the-loop (HITL)**: Destructive or high-impact operations require explicit human approval.
- **Single control plane**: All device and service operations route through VASER-Router unless explicitly exempted.
- **Auditability**: Every action must be logged with sufficient context for forensic review.

## Protected Assets
- Network infrastructure (routers, switches, firewalls, gateways).
- Identity and secret stores (SSH keys, API tokens, vaults).
- Critical compute/storage nodes and any device tagged as **protected** or **critical**.

## Human-in-the-Loop Requirements
Explicit approval is mandatory before executing any of the following:
- Device removal, re-imaging, or factory reset.
- Network-wide scans that exceed approved CIDR ranges.
- Production system reboots or power cycles.
- Firewall, ACL, or routing changes.
- Destructive file operations (delete, purge, wipe) in shared or production locations.
- Credential rotation or secret revocation.

## Logging & Audit Requirements
- Log every action with timestamp, actor, target, action name, parameters (redacted if sensitive), and outcome.
- Store logs in the centralized audit store configured by VASER-Router.
- Retain security logs according to the platform retention policy (default 180 days).
- Escalate any failed, denied, or suspicious action attempts.

## Escalation
- **Critical incidents**: Notify the security owner immediately and halt automated actions on affected assets.
- **High risk changes**: Require additional approval from the designated system owner.
- **Repeated failures**: Trigger a security review and restrict the tool scope until resolved.
