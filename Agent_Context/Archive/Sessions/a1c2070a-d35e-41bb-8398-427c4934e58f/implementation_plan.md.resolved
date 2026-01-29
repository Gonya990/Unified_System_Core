# IMPLEMENTATION PLAN: PROXMOX HARDWARE UPGRADE SHUTDOWN

This plan describes the steps to safely stop all virtual machines and containers on the 'pve' node and then shut down the host itself to prepare for physical hardware upgrades (RAM, GPU, Cooler).

## User Review Required

> [!IMPORTANT]
> **VM STICKINESS:** If any VM fails to shut down within 3 minutes, the protocol requires manual intervention. I will NOT use `stop` (force kill) without explicit command.
> **PiKVM ACCESS:** Verified IP `192.168.190.154`. Credentials: `gonya` / `gonya6550`.

## Proposed Changes

### Discovery & Safeguard (Phase 1)

1. **Identify Node IP:** Map 'pve' to a specific IP. (Candidates: 100.74.194.25, 192.168.1.x, or reachable via PiKVM dashboard).
2. **Access PiKVM:** Utilize discovered IP `192.168.190.154` for visual confirmation and power management.
3. **Access Proxmox:** Connect via Browser Agent to Web UI (typically `https://<ip>:8006`) as SSH is restricted.
4. **Inventory Guests:** Use Proxmox Web UI to identify running guests.
4. **Initiate Shutdown:**
   - Loop through running VMs: `qm shutdown <vmid>`
   - Loop through running LXCs: `pct shutdown <vmid>`
5. **Monitor Loop:** Poll VM status every 30 seconds for 3 minutes.

### Host Shutdown (Phase 2)

1. **Final Check:** Ensure all statuses are `stopped`.
2. **Host Shutdown:** Execute `shutdown -h now`.

### Verification (Phase 3)

1. **PiKVM Check:** Access PiKVM (monitoring) to confirm the machine is in S5 (soft-off) state.
2. **Notify User:** "СЕРВЕР ОБЕСТОЧЕН. ГОТОВ К ВСКРЫТИЮ."

## Verification Plan

### Automated Tests

- `ssh root@pve "qm list"` (Check for 0 running)
- `ssh root@pve "uptime"` (Verify connection still alive before final shutdown)

### Manual Verification

- Visual check of PiKVM status (if API/web access available).
