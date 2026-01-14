# Security Audit Plan

## Goal

Ensure recently added scripts and configurations adhere to the "Strict Security Protocol" and contain no secrets, vulnerabilities, or unsafe permissions.

## Scope

- **New Scripts**: `Scripts/windows_optimizer/`, `Scripts/windows_archive_analyzer/`.
- **New Configs**: `Scripts/windows_archive_analyzer/config.json`.
- **GCP Integration**: Check `.env` usage (ensure no hardcoded keys in `daily_researcher.py`).

## Proposed Strategy

### 1. Secret Scanning

- Run `grep` patterns for common secrets (API keys, tokens, passwords) in the target directories.
- Verify `gitleaks` (if available) or use a custom regex scanner.

### 2. Permission Check

- Ensure scripts are executable (`+x`) where needed but not world-writable.
- Verify ownership.

### 3. Code Safety Analysis

- **Remote Execution**: Verify `scan_archives.ps1` and `hardware_audit.ps1` do not allow arbitrary command injection if inputs were compromised (though they are currently local/static).
- **Data Handling**: Ensure JSON outputs do not leak PII (Personal Identifiable Information) inadvertently.

## Verification

- **Secret Scan**: Must return 0 matches for sensitive patterns.
- **Permissions**: `wait_for_windows.sh` must be `755` or `700`.
