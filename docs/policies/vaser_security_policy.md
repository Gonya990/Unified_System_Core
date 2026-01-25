# VASER Security Policy

## Goals
- Protect critical infrastructure and sensitive credentials.
- Ensure destructive or high-impact actions require human confirmation.
- Maintain auditability and reliable backups before changes.

## Confirmation Matrix
| Action | Risk Level | Confirmation Required | Notes |
| --- | --- | --- | --- |
| scan_network | Medium | Yes | Reveals device inventory. |
| get_device_info | Low | No | Read-only. |
| run_command | High | Yes | Restricted by allowlist. |
| add_device | Medium | Yes | Adds inventory + credentials. |
| remove_device | High | Yes | Destructive change. |
| reboot_device | High | Yes | Disruptive. |
| configure_device | High | Yes | Configuration change. |
| ha.service_call | Medium | Conditional | Confirm if service is destructive (e.g., reboot). |
| ha.get_state | Low | No | Read-only. |
| ha.set_state | Medium | Conditional | Confirm if impacts safety (locks, alarms). |
| ha.execute_script | Medium | Conditional | Confirm if script is marked critical. |
| local.run | High | Yes | Restricted by allowlist. |
| local.read | Low | No | Read-only. |
| local.write | Medium | Yes | Data modification. |
| cloud.* | Medium | Conditional | Confirm for data deletion or external share. |
| create_task | Low | No | Read-only impact. |
| complete_task | Low | No | Read-only impact. |
| remind_user | Low | No | Read-only impact. |
| generate_report | Low | No | Read-only impact. |
| collect_logs | Medium | Conditional | Confirm if includes sensitive sources. |
| analyze_logs | Low | No | Read-only impact. |
| summarize_project | Low | No | Read-only impact. |
| generate_presentation | Low | No | Read-only impact. |

## Command Allowlist (run_command/local.run)
- Only allow:
  - Package updates
  - Status checks
  - Service restarts for non-critical services
  - Diagnostic scripts from trusted directories
- Deny:
  - Credential dumping
  - Data deletion without backup
  - Network-wide destructive operations

## Backup Rules
- Mandatory snapshot or backup before:
  - `remove_device`
  - `configure_device`
  - Any action altering system configuration or storage
- Backups must be logged with timestamp and location.

## Audit Logging Requirements
- Log entries must include:
  - request_id, operator, device/service target, action, timestamp
  - approval status, executor, stdout/stderr (if safe)
- Retain audit logs for a minimum of 180 days.
