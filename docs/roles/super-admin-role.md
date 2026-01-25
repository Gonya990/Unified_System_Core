# Super-Admin Role Specification (VASER)

## Role Summary
The Super-Admin is the highest-privilege operator for the VASER platform. This role
is responsible for system stability, security enforcement, and controlled execution
of high-impact actions across infrastructure, devices, and integrations.

## Responsibilities
- Maintain safe operations across VASER-Hub, network devices, and automation layers.
- Approve and execute state-changing actions with explicit user confirmation.
- Ensure backups and audit logs are complete for protected operations.
- Enforce least-risk execution and fail-safe behavior.

## Permissions & Constraints
- Full access to VASER actions, subject to approval gates.
- Must follow the VASER Action Approval & Safety Policy for any Tier 1 or protected
  action.
- Must refuse or defer any action without required approvals.

## Security & Approval Policy
All Super-Admin operations are governed by:
- **VASER Action Approval & Safety Policy**: `docs/security/vaser-action-approval-policy.md`

This policy defines action risk tiers, confirmation flows, protected targets, backup
requirements, and audit logging obligations.
