# VASER Control Hub Architecture

## Overview
VASER Control Hub is the central execution and credential broker for the VASER ecosystem. It receives structured commands from GPT actions, authenticates requests, resolves credentials, and executes actions across the network, Home Assistant, local tools, and cloud services.

## Core Layers
1. **Interface Layer**
   - OpenAPI Actions for Custom GPT
   - Webhooks and automation triggers

2. **Orchestration Layer**
   - Policy enforcement (confirmation rules, approvals)
   - Action routing (network, HA, local, cloud)
   - Request validation and schema checks

3. **Credential Vault**
   - Stores SSH keys, API tokens, OAuth refresh tokens
   - Provides short-lived execution tokens via `credentials_ref`

4. **Execution Layer**
   - Network agents (SSH/WinRM/API clients)
   - Home Assistant bridge
   - Local gateway for command/file operations
   - Cloud connectors (Calendar, Mail, Storage)

5. **Observability Layer**
   - Audit logs, action history, metrics
   - Health and status dashboards

## Data Flow (High-Level)
1. GPT issues an action request via OpenAPI.
2. Hub validates schema and checks policy rules.
3. Hub resolves credential references and acquires access tokens.
4. Action executes in the target subsystem.
5. Result is logged and returned to GPT.

## Security Model
- Zero-trust by default: explicit allow-list for targets and subnets.
- Mandatory confirmations for destructive actions.
- Every action is logged with user, target, timestamp, and outcome.

## Integration Points
- **Network:** inventory, scanning, configuration, and command execution.
- **Home Assistant:** entity state, service calls, scripts.
- **Local Tools:** `/local/run`, `/local/read`, `/local/write`.
- **Cloud:** Gmail/Outlook, Google/iCloud Calendar, Drive/Yandex Disk/Dropbox.
