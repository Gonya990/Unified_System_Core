---
description: Diagnose a specific VM - config, disks, status, internal health
---
# /vm-check <VMID>

Deep diagnosis of a specific VM.

## Arguments

- `VMID` (required): The Proxmox VM ID (e.g., 106, 100)

## Execution

When user says `/vm-check <VMID>`:

### 1. Get VM Config and Status
```bash
ssh root@100.78.145.67 "qm status <VMID> && echo '---' && qm config <VMID>"
```

### 2. Check Disk Allocation
```bash
# Parse scsi/virtio disks from config, check their storage pools
ssh root@100.78.145.67 "qm config <VMID> | grep -E 'scsi|virtio|ide|sata'"
```

### 3. Check Storage Pool Status
```bash
# For each storage pool used by the VM
ssh root@100.78.145.67 "pvesm status"
ssh root@100.78.145.67 "lvs <pool> --units g"  # if LVM-based
```

### 4. Check Inside VM (if running)
```bash
# Get VM's IP from config or ARP table
ssh root@100.78.145.67 "ip neigh | grep <MAC_FROM_CONFIG>"

# SSH into VM and check disk usage
ssh root@100.78.145.67 "ssh user@<VM_IP> 'lsblk && echo --- && df -h'"
```

## Common VMIDs

| VMID | Name | User | Notes |
|------|------|------|-------|
| 106 | unified-home-core-cloud | gonya/kosta | Main AI VM, 300GB data disk at /mnt/data |
| 100 | Gaming | - | Windows, GPU passthrough |

## Output Format

```
VM <VMID>: <NAME>
Status: running/stopped
Host: proxmox-gpu (100.78.145.67)

Config:
- CPU: X cores
- RAM: X GB
- Disks:
  - scsi0: <storage>:<size> (OS)
  - scsi1: <storage>:<size> (Data)

Internal (if accessible):
- / : XX% used (XXG free)
- /mnt/data: XX% used (XXG free)

Issues Found:
- [list any problems]
```
