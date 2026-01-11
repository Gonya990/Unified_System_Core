---
description: Check all storage pools and disk space on Proxmox hosts
---
# /storage-check

Check storage health across all Proxmox hosts.

## Execution

When user says `/storage-check`:

### 1. Proxmox Storage Status
```bash
ssh root@100.78.145.67 "pvesm status"
```

### 2. LVM Volume Groups
```bash
ssh root@100.78.145.67 "vgs --units g"
ssh root@100.78.145.67 "lvs --units g"
```

### 3. Filesystem Usage
```bash
ssh root@100.78.145.67 "df -h"
```

### 4. ZFS Pools (if any)
```bash
ssh root@100.78.145.67 "zpool list 2>/dev/null || echo 'No ZFS pools'"
ssh root@100.78.145.67 "zfs list 2>/dev/null || echo 'No ZFS datasets'"
```

## Storage Reference

| Pool | Type | Location | Typical Use |
|------|------|----------|-------------|
| nvme-thin | LVM-thin | NVMe SSD | Fast VM disks (OS, databases) |
| ent-ssd | LVM | Enterprise SSD | Secondary VM storage |
| Backup | Directory | HDD | VM backups |
| Natali | ZFS | - | Media storage (often full) |

## Output Format

```
STORAGE HEALTH REPORT
=====================

| Pool | Type | Total | Used | Free | % Used | Status |
|------|------|-------|------|------|--------|--------|
| nvme-thin | lvmthin | 957G | 314G | 642G | 33% | OK |
| ent-ssd | lvm | 1.8T | 1.6T | 173G | 90% | WARNING |

Alerts:
- ent-ssd at 90% - consider cleanup or expansion
- Natali ZFS pool at 98% - critical
```

## Thresholds

| % Used | Status |
|--------|--------|
| < 70% | OK |
| 70-85% | INFO |
| 85-95% | WARNING |
| > 95% | CRITICAL |
