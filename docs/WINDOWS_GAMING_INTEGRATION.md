# Windows Gaming Integration - Credential Architecture

## Overview

This document describes how Windows account memory and gaming credentials are handled in the Distributed Family AI Cluster (Vibranium) project.

## Architecture

### Credential Isolation Strategy

Gaming credentials are **intentionally isolated on the Windows VM** rather than managed by the AI Core. This design provides:

1. **Security**: Game platform credentials (Steam, Epic, GOG) never leave the Windows environment
2. **Compatibility**: Native Windows Credential Manager handles encryption
3. **Simplicity**: No cross-platform credential syncing required

### Component Responsibilities

| Component | Location | Responsibility |
|-----------|----------|----------------|
| `proxmox_manager.py` | `Projects/AI_Core/src/modules/` | VM lifecycle (start/stop gaming VM) |
| `gaming_sentinel.py` | `Scripts/External/` | Idle detection on Windows, reclaim webhook |
| Windows Credential Manager | Gaming VM (vmid 100) | Steam/Epic/GOG account storage |
| Windows User Profiles | `C:\Users\<username>` | Per-user game saves, settings |

### Credential Storage Locations

**On Windows VM (vmid 100):**
- Steam: `C:\Program Files (x86)\Steam\config\` (encrypted)
- Epic Games: Windows Credential Manager
- GOG Galaxy: `%APPDATA%\GOG.com\Galaxy\`
- Game saves: `%USERPROFILE%\Saved Games\` or per-game locations

**On AI Core (this repo):**
- Google OAuth: `identity_orchestrator.py` via TokenBroker (AES-256-GCM)
- API Keys: `config/resources.yaml` (encrypted with TokenBroker)
- Infrastructure secrets: Proxmox SSH keys in `~/.ssh/`

### Gaming Session Flow

```
User: /play
    │
    ▼
Telegram Bot (ai_telegram_bot_v2.py)
    │
    ▼
ProxmoxManager.switch_to_gaming()
    │
    ├─► Stop AI VM (vmid 106)
    └─► Start Gaming VM (vmid 100)
            │
            ▼
    Windows boots with user profile
    (credentials already stored locally)
            │
            ▼
    gaming_sentinel.py monitors for idle
            │
            ▼ (after 30min idle)
    POST /webhook/reclaim
            │
            ▼
    ProxmoxManager.switch_to_ai()
```

### Multi-User Considerations

If multiple Windows users need gaming access:

1. **Windows User Profiles**: Create separate Windows accounts on the VM
2. **Steam Family Sharing**: Share games across accounts without credential sharing
3. **VM Snapshots**: Optionally snapshot per-user configurations

## Security Notes

- **DO NOT** store Windows/gaming passwords in this repository
- **DO NOT** sync game platform credentials to cloud services
- Gaming credentials are considered "user-local" to the Windows VM
- The AI Core only controls VM power state, not internal Windows authentication

## Related Files

- `Projects/AI_Core/src/modules/proxmox_manager.py` - VM control
- `Scripts/External/gaming_sentinel.py` - Idle monitoring
- `Projects/AI_Core/config/infrastructure.yaml` - VM definitions
- `Projects/AI_Core/src/identity_orchestrator.py` - AI Core credentials (not gaming)

## Contact

For questions about this architecture, ping FuchsiaCat (Kosta) via Agent Mail.
