# Unified System Architecture

## 1. Network Topology

- **Mesh Network**: Tailscale (100.x.x.x) connects all nodes (Mac, Windows, Proxmox).
- **Local Network**: Proxmox VMs are bridged (192.168.190.x).

## 2. Synchronization Strategy (Design Choice)

We have chosen **Git + GitHub** as the primary mechanism for file synchronization and version control.

**Why GitHub?**

1. **Source of Truth**: The remote repository acts as the central valid state of the system.
2. **Version Control**: We can rollback any breaking changes (unlike simple file copy).
3. **Automation**: Windows and Linux nodes can automatically `git pull` the latest logic.
4. **Security**: Access is controlled via SSH Keys.

**Workflow**:

1. **Development**: Code is written on MacBook (Admin).
2. **Commit**: Changes are committed and pushed to GitHub `main` branch.
3. **Deployment**: Windows/Proxmox nodes pull the changes to apply updates.

## 3. Nodes Roles

- **MacBook**: Commander / Coding Terminal.
- **Windows AI Core**: Heavy Inference (GPU), Telegram Bot Host.
- **Proxmox**: 24/7 Services (Home Assistant, Docker).
