# Consolidating Working Zones and System Audit Plan

## Goal Description

Merge all working zones (`windows-rtx-ai-setup`, `home-assistant`) and a new `Sandbox` into a unified logical or physical structure. Ensure strict security (owner/admin `igor/gonya` only), Russian locale environment, and full resource availability (Proxmox, GPUs).

## User Review Required
>
> [!IMPORTANT]
> **Directory Structure Change**: I propose moving `windows-rtx-ai-setup` and `home-assistant` into a new parent directory `Unified_System` (or similar) within `Documents` to centralize management. Is this acceptable?
> Alternatively, I can leave them in place and just "logically" map them, but physical consolidation is cleaner for "merging".

> [!NOTE]
> **Admin User**: The system will enforce "igor/gonya" as the primary admin identity.

## Proposed Changes

### Directory Structure - /Users/macbook/Documents/Unified_System

I will create a root folder `Unified_System` (System_Core) to house all active projects.

#### [NEW] [Sandbox](file:///Users/macbook/Documents/Unified_System/Sandbox)

- A dedicated directory for testing scripts and unsafe operations.

#### [MOVE] windows-rtx-ai-setup -> /Unified_System/Windows_AI_Core

- Rename for clarity. Contains all RTX AI setup scripts.

#### [MOVE] home-assistant -> /Unified_System/Home_Assistant_Config

- Contains HA configs and keys.

### Security & Localization

- **Localization**: Ensure all new scripts and logs output in Russian.
- **Access**: Add checks in scripts to verify user is `igor` or `gonya`.

## Verification Plan

### Automated Tests

1. **Directory Check**: Verify stricture exists.
2. **Permissions Check**: Run a script to verify only owner has write access.
3. **Locale Check**: Run `locale` or check env vars to ensure Russian language support.

### Manual Verification

- User to confirm file locations.
- User to run a test script in `Sandbox` to verify "Russian environment" output.
