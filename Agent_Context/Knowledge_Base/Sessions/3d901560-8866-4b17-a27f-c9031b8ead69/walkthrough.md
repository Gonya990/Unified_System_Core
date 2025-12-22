# Deployment Report / Отчет о развертывании

## 1. System Consolidation / Консолидация

- **Cleaned**: Removed old `Home_Assistant_Config` to `_Archive`.
- **Structured**: Reorganized `Windows_AI_Core` into `src`, `scripts`, `docs`.
- **Verified**: Network connectivity between Mac, Windows, and Proxmox is active (Tailscale Mesh).

## 2. Windows AI Core (Node: `igor-gaming`)

- **Status**: ✅ Deployed & Installed.
- **Python Environment**: Configured with `uv`.
- **Libraries**: PyTorch, Transformers installed.
- **Access**:

  ```bash
  ssh gonya@100.127.194.111
  cd Desktop/Windows_AI_Core
  ```

## 3. Proxmox Virtual Environment (Node: `pve`)

- **Status**: ✅ Active.
- **New VM**: `unified-home-core` (ID 106).
- **OS**: Ubuntu 22.04 LTS (Cloud Image).
- **Configuration**:
  - 2 Cores, 4GB RAM.
  - SSH Key Authentication (auto-injected).
  - User: `gonya`.

### How to Connect (Active)

1. **VM IP**: `192.168.190.180`
2. Connect:

   ```bash
   ssh -i /Users/macbook/Documents/Unified_System/Sandbox/id_rsa_proxmox gonya@192.168.190.180
   ```

## Next Steps / Что дальше?

- **Home Assistant**: Install Docker on VM 106 and deploy HA container.
- **N8N**: Can be deployed on VM 106 or used on Windows Machine.
- **Monitoring**: Check `admin_check.sh` periodically.
