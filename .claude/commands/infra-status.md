---
description: Check full infrastructure health - nodes, VMs, storage pools
---
# /infra-status

Performs a comprehensive health check of the homelab infrastructure.

## Execution

When user says `/infra-status`, run these checks:

### 1. Proxmox Host Status
```bash
# Check proxmox-gpu host
ssh -o ConnectTimeout=10 root@100.78.145.67 "hostname && uptime && pvesm status && qm list"
```

### 2. Storage Health
```bash
ssh root@100.78.145.67 "pvesm status && echo '---' && df -h && echo '---' && lvs --units g"
```

### 3. Critical VMs Status
```bash
# VM 106 (unified-home-core-cloud) - main AI workloads
ssh root@100.78.145.67 "qm status 106 && qm config 106 | grep -E 'scsi|memory|cores|name'"

# VM 100 (Gaming) - if relevant
ssh root@100.78.145.67 "qm status 100"
```

### 4. Network/Tailscale Check
```bash
# Check if key nodes are reachable via Tailscale
ping -c 1 -W 2 100.78.145.67  # proxmox-gpu
ping -c 1 -W 2 100.110.209.49 # unified-home-core-cloud
```

## Output Format

Summarize as:

| Component | Status | Notes |
|-----------|--------|-------|
| proxmox-gpu | UP/DOWN | uptime, load |
| VM 106 | running/stopped | CPU/RAM usage |
| nvme-thin | XX% used | free space |
| ent-ssd | XX% used | free space |

Flag any issues:
- Storage > 85% used
- VMs not running that should be
- Hosts unreachable
