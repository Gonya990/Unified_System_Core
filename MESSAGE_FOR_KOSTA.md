# 📟 Message for Kosta (FuchsiaCat)

## Task Context: Distributed Family AI Cluster (Vibranium)

I have implemented Phase 1 (Family AI Swarm) and the foundation for Phase 2 (Hardware Orchestration).

### 🚨 Critical Instructions (from User)

- **Windows Accounts & Memory**: All settings related to Windows accounts, gaming credentials, and associated memory are **your responsibility**.
- The user confirmed that **you (Kosta)** know exactly where these files and settings are located.
- **Do NOT** expect the Antigravity agent to handle the internal Windows user profiling or account-specific memory isolation for games.

### Current Implementation State

1. **API Swarm**: `swarm_manager.py` is active in `AI_Core`. It rotates Gemini keys from `config/resources.yaml`.
2. **Hardware Switching**: `proxmox_manager.py` is ready to be used by the Telegram Bot (`/play`, `/stop_play`). It uses direct SSH and `qm` commands on `100.74.137.122`.
3. **Sentinels**: `gaming_sentinel.py` is prepared for deployment on the Windows VM to monitor idle time and notify for reclaim.

### Next for You

- Verify the integration of Windows account "memory" and gaming identities.
- Ensure the Proxmox VM (Windows) is configured to handle the credentials correctly upon startup.
- Review `implementation_plan.md` and `task.md` in the brain/ artifacts.

Ping me (Antigravity) if you need specific logic for the resource broker.
