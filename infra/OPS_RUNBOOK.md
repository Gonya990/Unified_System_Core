# Operations Runbook

## Infrastructure Overview

| Host                    | IP (Tailscale) | Role              | Status                |
|-------------------------|----------------|-------------------|-----------------------|
| unified-home-core-cloud | 100.87.208.56  | MCP Mail, Svcs    | `ping 100.87.208.56`  |
| proxmox-gpu             | 100.74.137.122 | VM Host, GPU      | `ping 100.74.137.122` |

---

## MCP Agent Mail Service

### Quick Commands

```bash
# Status
ssh gonya@100.87.208.56 "sudo systemctl status mcp-agent-mail --no-pager"

# Restart
ssh gonya@100.87.208.56 "sudo systemctl restart mcp-agent-mail"

# Logs (live)
ssh gonya@100.87.208.56 "sudo journalctl -u mcp-agent-mail -f"

# Logs (last 100 lines)
ssh gonya@100.87.208.56 "sudo journalctl -u mcp-agent-mail -n 100"
```

### Update Deployment

```bash
# Pull latest from fork and restart
ssh gonya@100.87.208.56 \
  "cd /opt/mcp-agent-mail && sudo git pull origin main && \
   sudo uv sync && sudo systemctl restart mcp-agent-mail"
```

### Push Local Changes to Production

```bash
# 1. From local machine
cd External_Tools/Stack/mcp_agent_mail
git push fork main

# 2. Deploy on server
ssh gonya@100.87.208.56 \
  "cd /opt/mcp-agent-mail && sudo git pull origin main && \
   sudo uv sync && sudo systemctl restart mcp-agent-mail"
```

### Full Redeploy

```bash
ssh gonya@100.87.208.56 "
  sudo systemctl stop mcp-agent-mail
  sudo mv /opt/mcp-agent-mail /opt/mcp-agent-mail.bak
  sudo git clone https://github.com/KostaGorod/mcp_agent_mail.git /opt/mcp-agent-mail
  sudo cp /opt/mcp-agent-mail.bak/.env /opt/mcp-agent-mail/.env
  cd /opt/mcp-agent-mail && sudo uv sync
  sudo systemctl start mcp-agent-mail
"
```

### Verify Deployment

```bash
# Check service
ssh gonya@100.87.208.56 "sudo systemctl status mcp-agent-mail --no-pager | head -n 15"

# Check list_agents tool present
ssh gonya@100.87.208.56 "grep -c 'def list_agents' /opt/mcp-agent-mail/src/mcp_agent_mail/app.py"

# Test health (should return 401 without token, 200 with token)
curl -s -o /dev/null -w "%{http_code}" http://100.87.208.56:8765/health
```

### Configuration

| Item | Location |
| :--- | :--- |
| Service file | `/etc/systemd/system/mcp-agent-mail.service` |
| Application | `/opt/mcp-agent-mail` |
| Environment | `/opt/mcp-agent-mail/.env` |
| Database | `/opt/mcp-agent-mail/data/agent_mail.db` |
| Git remote | `https://github.com/KostaGorod/mcp_agent_mail.git` |

---

## VM 106 (unified-home-core-cloud) Maintenance

### Disk Usage Check

```bash
ssh gonya@100.87.208.56 \
  "df -h / && du -h --max-depth=2 / 2>/dev/null | sort -hr | head -n 20"
```

### Emergency Disk Cleanup

```bash
ssh gonya@100.87.208.56 "
  sudo journalctl --vacuum-time=3d
  sudo apt clean
  sudo docker system prune -af 2>/dev/null || true
  sudo rm -rf /tmp/* /var/tmp/*
"
```

### Memory Check

```bash
ssh gonya@100.87.208.56 "free -h && ps aux --sort=-%mem | head -10"
```

---

## Proxmox Host (proxmox-gpu)

### Check Status (when reachable)

```bash
ssh root@100.74.137.122 "hostname && uptime && pvesm status && qm list"
```

### Storage Health

```bash
ssh root@100.74.137.122 "pvesm status && df -h && lvs --units g"
```

### VM Management

```bash
# List VMs
ssh root@100.74.137.122 "qm list"

# Start/Stop VM
ssh root@100.74.137.122 "qm start 106"
ssh root@100.74.137.122 "qm stop 106"

# VM config
ssh root@100.74.137.122 "qm config 106"
```

---

## Beads Task Sync

### Sync Task Board

```bash
./Scripts/Orchestration/sync/tasks-sync.sh
```

### Force Reset beads-sync Branch

```bash
git push origin main:beads-sync --force
```

### List Open Tasks

```bash
bd list --status open
```

---

## Troubleshooting

### MCP Mail Server Unreachable

1. Check Tailscale: `tailscale status`
2. Ping host: `ping 100.87.208.56`
3. SSH and check service: `ssh gonya@100.87.208.56 "sudo systemctl status mcp-agent-mail"`
4. Check port: `nc -zv 100.87.208.56 8765`

### Proxmox Host Unreachable

1. Check Tailscale on proxmox-gpu
2. Try local network access if available
3. Physical console access may be required
4. Check if Tailscale service is running on host

### Beads Sync Conflict

```bash
# Nuclear option - force reset beads-sync to match main
git fetch origin beads-sync
git branch -D beads-sync || true
git checkout -b beads-sync origin/main
git push origin beads-sync --force
git checkout main
```

---

## Alerts & Thresholds

| Metric | Warning | Critical | Action |
| :--- | :--- | :--- | :--- |
| Disk Usage | 80% | 90% | Run emergency cleanup |
| Memory | 85% | 95% | Identify memory hog, restart services |
| Service Down | - | Any | Restart service, check logs |
| Host Unreachable | 5 min | 15 min | Check Tailscale, physical access |

---

## Tailscale ACL Management

### GitOps Workflow

ACL managed via `infra/tailscale/policy.jsonl`.
Changes auto-applied on push to `main`.

**To update ACL:**

1. Edit `infra/tailscale/policy.jsonl` locally
2. Commit and push to `main`
3. GitHub Actions will validate and deploy
4. Verify at [Tailscale ACL Console](https://login.tailscale.com/admin/acls)

**Manual override (emergency):**

If GitOps fails, you can still edit ACL via web UI. Re-sync by:

```bash
git pull origin main
# Copy current web ACL to infra/tailscale/policy.jsonl
git add infra/tailscale/policy.jsonl
git commit -m "Sync ACL from web UI"
git push
```

### Common ACL Changes

**Add new ResourceNode:**

1. Tag machine in web UI with `tag:ResourceNode`
2. No ACL change needed (already covered by existing rules)

**Add new user:**

No ACL change needed - `autogroup:member` covers all org members automatically.

### API Key Management

**Location:** GitHub repo → Settings → Secrets → `TAILSCALE_API_KEY`

**Rotation (every 90 days):**

1. Generate new key at [Tailscale API Keys](https://login.tailscale.com/admin/settings/keys)
2. Update GitHub secret
3. Revoke old key
