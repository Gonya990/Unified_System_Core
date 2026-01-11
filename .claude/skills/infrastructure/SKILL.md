---
name: infrastructure
description: >
  Proxmox VM and infrastructure management for the Unified System Core homelab.
  Use for VM diagnostics, storage checks, node status, and infrastructure troubleshooting.
allowed-tools: "Read,Bash(ssh:*),Bash(qm:*),Bash(pvesm:*),Bash(lvs:*),Bash(df:*),Bash(lsblk:*)"
version: "1.0.0"
author: "Unified System Core"
---

# Infrastructure Management Skill

Manage Proxmox VMs, storage pools, and homelab infrastructure via SSH.

## Infrastructure Overview

| Node | IP (Tailscale) | Role |
|------|----------------|------|
| proxmox | 100.74.137.122 | Main Proxmox host |
| proxmox-gpu | 100.78.145.67 | GPU-enabled Proxmox host |
| unified-home-core-cloud | 100.110.209.49 | Main AI/automation VM (vmid 106) |
| smart | 100.81.133.25 | Smart home services |

## VM Reference

| VMID | Name | Host | Purpose |
|------|------|------|---------|
| 100 | Gaming VM | proxmox-gpu | Windows gaming with GPU passthrough |
| 106 | unified-home-core-cloud | proxmox-gpu | Main AI workloads, Telegram bot, automation |

## Storage Pools (proxmox-gpu)

| Pool | Type | Typical Use |
|------|------|-------------|
| nvme-thin | LVM-thin on NVMe | Fast VM disks (OS, databases) |
| ent-ssd | LVM on enterprise SSD | Secondary VM storage |
| Backup | Directory | VM backups |

## Quick Diagnostics

### Check VM Status
```bash
ssh root@100.78.145.67 "qm status <VMID>"
ssh root@100.78.145.67 "qm config <VMID>"
```

### Check Storage
```bash
ssh root@100.78.145.67 "pvesm status"
ssh root@100.78.145.67 "lvs <pool> --units g"
ssh root@100.78.145.67 "df -h"
```

### Check Inside VM
```bash
# Via Proxmox host (needs VM's local IP)
ssh root@100.78.145.67 "ssh user@<VM_LOCAL_IP> 'lsblk && df -h'"

# Direct via Tailscale (if VM has Tailscale)
ssh user@<VM_TAILSCALE_IP> "lsblk && df -h"
```

## Common Issues

### "Insufficient space" when adding disk
**Cause**: Trying to create disk on storage pool with insufficient free space.
**Fix**: 
1. Check if disk already exists: `qm config <VMID> | grep scsi`
2. Check storage free space: `pvesm status`
3. Use a different storage pool or free up space

### VM disk not visible inside guest
**Cause**: Disk attached but not formatted/mounted.
**Fix**:
1. Check if disk visible: `lsblk` inside VM
2. If visible but unmounted: format and mount
3. If not visible: check VM config and rescan SCSI bus

### VM won't start - GPU passthrough issues
**Cause**: GPU driver conflict or IOMMU issues.
**Fix**:
1. Check IOMMU groups: `dmesg | grep -i iommu`
2. Verify GPU not in use by host
3. Check VM config for correct hostpci settings

## Workflow: Diagnose VM Issue

1. **Check VM status**: `qm status <VMID>`
2. **Get VM config**: `qm config <VMID>`
3. **Check storage**: `pvesm status` and `lvs`
4. **If running, check inside VM**: SSH and run `lsblk`, `df -h`
5. **Check logs**: `journalctl -u pve* --since "1 hour ago"`

## Related Commands

- `/infra-status` - Full infrastructure health check
- `/vm-check <VMID>` - Diagnose specific VM
- `/storage-check` - Check all storage pools

## References

- Infrastructure config: `Projects/AI_Core/config/infrastructure.yaml`
- Proxmox manager: `Projects/AI_Core/src/modules/proxmox_manager.py`
