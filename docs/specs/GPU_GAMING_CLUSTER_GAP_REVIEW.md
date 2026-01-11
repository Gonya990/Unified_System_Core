# GPU Gaming Cluster Spec - Gap Analysis Review

**Spec:** `docs/specs/GPU_GAMING_CLUSTER_SPEC.md`  
**Bead:** US-4fx  
**Reviewed:** 2026-01-11  

---

## Executive Summary

The spec provides a solid foundation for the hybrid K3s + libvirt architecture. However, the review identified **3 critical gaps**, **5 high-severity gaps**, and **3 spec errors** that need addressing before implementation.

**Most Critical Issues:**
1. Race conditions during GPU claim window (no admission control)
2. Driver switch failures have no rollback mechanism
3. vendor-reset mitigation is **invalid for NVIDIA GPUs** (AMD-only)

---

## Spec Errors (Factual Corrections Needed)

### E1. vendor-reset Does NOT Work for NVIDIA GPUs

| Severity | CRITICAL |
|----------|----------|
| Location | "Known Risk: GPU Reset Bug" → "Mitigation Options" |
| Problem | Spec lists `vendor-reset kernel module` as mitigation. **vendor-reset is AMD-only** - it does not help NVIDIA GPUs. |
| Fix | Remove vendor-reset from NVIDIA mitigations. Replace with: preflight reset testing, persistent VFIO binding, or dedicated GPU assignment. |

### E2. MIG Not Available on Consumer RTX

| Severity | LOW |
|----------|-----|
| Location | Implicit in AI workload discussion |
| Problem | MIG (Multi-Instance GPU) only works on data center GPUs (A100, H100). RTX 3080/2080 cannot use MIG. |
| Fix | Clarify that time-slicing (no memory isolation) is the only sharing option for RTX cards. |

### E3. NixOS hardware.opengl Renamed

| Severity | LOW |
|----------|-----|
| Location | `modules/nvidia.nix` |
| Problem | NixOS 24.11+ renamed `hardware.opengl` to `hardware.graphics`. The spec targets 24.05 but should note this for future upgrades. |
| Fix | Add comment noting the rename for 24.11+ compatibility. |

---

## Critical Gaps

### G1. Race Condition During GPU Claim Window

| Severity | CRITICAL |
|----------|----------|
| Problem | Between adding taint and driver switch, new pods can still be scheduled (scheduler sees GPU available). |
| Impact | AI pod starts on GPU being claimed → driver switch fails or data corruption. |

**Current Flow (Vulnerable):**
```
1. Add NoExecute taint          ← Pods start evicting
2. Wait for drain (30s)         ← NEW PODS CAN STILL SCHEDULE HERE
3. Driver switch                ← May fail if pod grabbed GPU
4. Start VM
```

**Recommended Fix:**
```
1. kubectl cordon $NODE         ← Block ALL new scheduling
2. Add NoExecute taint          ← Start eviction
3. kubectl drain --grace=120s   ← Wait for graceful termination
4. Verify GPU released          ← nvidia-smi shows no processes
5. Driver switch
6. Start VM
7. (Keep node cordoned while gaming)
```

**Better Fix:** Implement admission webhook that rejects GPU pods when `gpu-X-status=claiming`.

---

### G2. Driver Switch Failure - No Rollback

| Severity | CRITICAL |
|----------|----------|
| Problem | If driver unbind/bind fails mid-way, system is left in inconsistent state. No automatic recovery. |
| Impact | GPU stuck unusable by both AI and gaming until manual intervention or reboot. |

**Current Flow (No Rollback):**
```
1. Unbind nvidia               ← Success
2. Bind vfio-pci               ← FAILS (GPU busy, IOMMU issue, etc.)
3. ???                         ← GPU now bound to nothing
```

**Recommended Fix - Transactional Steps:**
```bash
claim_gpu() {
  # Pre-checks
  if ! verify_gpu_idle "$pci_addr"; then
    log "ERROR: GPU still in use, aborting"
    return 1
  fi
  
  # Unbind with rollback
  echo "$pci_addr" > /sys/bus/pci/drivers/nvidia/unbind || {
    log "ERROR: Failed to unbind nvidia"
    return 1
  }
  
  # Bind vfio with rollback
  echo "vfio-pci" > "/sys/bus/pci/devices/$pci_addr/driver_override"
  if ! echo "$pci_addr" > /sys/bus/pci/drivers/vfio-pci/bind; then
    log "ERROR: Failed to bind vfio, rolling back to nvidia"
    echo "" > "/sys/bus/pci/devices/$pci_addr/driver_override"
    echo "$pci_addr" > /sys/bus/pci/drivers/nvidia/bind
    kubectl taint nodes "$NODE_NAME" "gpu-$gpu_index=gaming:NoExecute-" || true
    return 1
  fi
  
  # Verify bind succeeded
  current_driver=$(readlink "/sys/bus/pci/devices/$pci_addr/driver" | xargs basename)
  if [[ "$current_driver" != "vfio-pci" ]]; then
    log "ERROR: Driver mismatch after bind, expected vfio-pci got $current_driver"
    # Rollback...
    return 1
  fi
}
```

---

### G3. State Mismatch - K8s Labels vs Actual Driver

| Severity | CRITICAL |
|----------|----------|
| Problem | K8s labels (`gpu-0-status=gaming`) can drift from actual driver state. No reconciliation. |
| Impact | Scheduler makes decisions based on stale/wrong state. Pods scheduled on unavailable GPUs. |

**Scenarios:**
- Label says "gaming" but VM crashed → GPU actually available
- Label says "available" but driver stuck in vfio → AI pods fail
- Node rebooted → Labels persist, driver state reset to nvidia

**Recommended Fix - CRD + Reconciler:**

```yaml
apiVersion: gpu.cluster.local/v1alpha1
kind: GpuClaim
metadata:
  name: node1-gpu-0
spec:
  node: node1
  gpuIndex: 0
  pciAddress: "0000:01:00.0"
  desiredState: gaming  # or "ai"
status:
  actualDriver: vfio-pci
  vmRunning: true
  lastReconciled: "2026-01-11T12:00:00Z"
  conditions:
    - type: Ready
      status: "True"
```

Controller reconciles every 30s:
1. Read actual driver from `/sys/bus/pci/devices/$PCI/driver`
2. Check VM status via `virsh domstate`
3. Update `status.actualDriver` and `status.vmRunning`
4. If mismatch with `spec.desiredState`, trigger transition
5. Update node labels/taints to match actual state

---

## High-Severity Gaps

### G4. No Periodic Reconciliation Loop

| Severity | HIGH |
|----------|------|
| Problem | Script runs once on claim/release. No background process verifying state consistency. |
| Impact | Drift accumulates. Manual intervention required to fix. |
| Fix | Run reconciler as systemd service or K8s DaemonSet checking state every 30-60s. |

---

### G5. Observability Gaps

| Severity | HIGH |
|----------|------|
| Problem | No metrics, events, or structured logging for GPU state transitions. |
| Impact | Debugging failures requires manual log spelunking. No alerting. |

**Recommended Additions:**
- **Metrics** (Prometheus): `gpu_claim_state{node,gpu_index}`, `gpu_claim_duration_seconds`, `gpu_driver_switch_failures_total`
- **Events**: K8s events on GpuClaim CR for state transitions
- **Logs**: Structured JSON logging with correlation IDs
- **Alerts**: GPU stuck in transitioning state > 5min, driver mismatch detected

---

### G6. RBAC / Security for GPU Claims

| Severity | HIGH |
|----------|------|
| Problem | `gpu-arbiter` script requires root + kubectl access. No access control on who can claim GPUs. |
| Impact | Any user with node access can claim any GPU. No audit trail. |

**Recommended Fix:**
- Wrap claims in API (REST or K8s CR)
- RBAC: Only `gamer-1` can claim `gpu-0`, etc.
- Audit log all claim/release actions
- Consider: Discord bot / Home Assistant with user authentication

---

### G7. NoExecute vs NoSchedule Taint Strategy

| Severity | HIGH |
|----------|------|
| Problem | Spec uses `NoExecute` which immediately evicts pods. This is aggressive. |
| Impact | In-flight inference requests are terminated abruptly. No graceful completion. |

**Comparison:**
| Taint | Behavior |
|-------|----------|
| `NoSchedule` | Prevents new pods, existing pods continue |
| `NoExecute` | Prevents new pods AND evicts existing pods |

**Recommended Approach:**
```bash
# Phase 1: Stop new scheduling
kubectl taint nodes $NODE gpu-$INDEX=claiming:NoSchedule

# Phase 2: Wait for in-flight work (optional grace period)
sleep 60  # Let current requests complete

# Phase 3: Force eviction only if still running
kubectl taint nodes $NODE gpu-$INDEX=gaming:NoExecute
```

---

### G8. VM Lifecycle Gaps

| Severity | HIGH |
|----------|------|
| Problem | No VM health monitoring, start timeout, or automatic recovery. |
| Impact | VM fails to start → GPU stuck in vfio → manual intervention required. |

**Missing:**
- Timeout on `virsh start` (what if it hangs?)
- Health check after VM boot (is it actually running?)
- Auto-rollback if VM fails within 60s of start
- Graceful shutdown timeout before `virsh destroy`

---

## Medium-Severity Gaps

### G9. Per-GPU vs Per-Node Scheduling

| Severity | MEDIUM |
|----------|--------|
| Problem | Taints are node-level. If node has 2 GPUs and only 1 is gaming, current approach is clunky. |
| Impact | Workarounds needed for partial GPU availability. |
| Fix | Use extended resources + node labels per GPU index. Scheduler uses affinity rules. |

---

### G10. IOMMU Group Handling

| Severity | MEDIUM |
|----------|--------|
| Problem | Spec mentions bad IOMMU groups but doesn't address resolution. |
| Impact | If GPUs share IOMMU group with other devices, passthrough fails. |
| Fix | Add pre-flight IOMMU group checker. Document ACS override patch for problematic motherboards. |

---

### G11. K3s Token Security

| Severity | MEDIUM |
|----------|--------|
| Problem | Token stored in plaintext in Nix config (`/etc/k3s/token`). |
| Impact | Token visible in Nix store, git history. |
| Fix | Use sops-nix or agenix for secrets management. |

---

## Recommended Implementation Order

1. **P0 - Fix Spec Errors**: Update vendor-reset section, add MIG clarification
2. **P1 - Race Condition**: Implement cordon+drain+verify flow
3. **P1 - Rollback Logic**: Add transactional driver switching with rollback
4. **P1 - Reconciliation**: Basic state-check loop (can be simple bash + systemd initially)
5. **P2 - Observability**: Add logging, basic Prometheus metrics
6. **P2 - RBAC**: Implement claim API with user authentication
7. **P3 - CRD+Controller**: Full Kubernetes-native solution (can defer if complexity too high)

---

## Questions for Owner Before Implementation

1. **Recovery preference**: Auto-rollback on failure, or alert-and-wait for manual intervention?
2. **Grace period**: How long should AI workloads get to finish in-flight requests? (30s? 60s? 120s?)
3. **Claim interface**: CLI-only acceptable, or need web UI / Discord bot?
4. **Dedicated GPUs**: If a card fails reset testing, is dedicating it to gaming-only acceptable?
5. **Monitoring stack**: Existing Prometheus/Grafana, or need to deploy?

---

## Appendix: Updated gpu-arbiter Skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail

# ... (config sourcing)

verify_gpu_idle() {
  local pci="$1"
  # Check no processes using GPU
  if nvidia-smi --query-compute-apps=pid --format=csv,noheader -i "$pci" | grep -q .; then
    return 1
  fi
  return 0
}

claim_gpu() {
  local gpu_index="$1"
  local pci_addr="${GPU_PCI[$gpu_index]}"
  local vm_name="${VM_NAMES[$gpu_index]}"
  
  log "=== Claiming GPU $gpu_index ($pci_addr) ==="
  
  # Phase 1: Cordon node to prevent new scheduling
  log "Phase 1: Cordoning node"
  kubectl cordon "$NODE_NAME"
  
  # Phase 2: Taint to start eviction
  log "Phase 2: Adding NoExecute taint"
  kubectl taint nodes "$NODE_NAME" "gpu-$gpu_index=gaming:NoExecute" --overwrite
  kubectl label nodes "$NODE_NAME" "gpu-$gpu_index-status=draining" --overwrite
  
  # Phase 3: Wait for GPU to be idle
  log "Phase 3: Waiting for GPU to be idle (max 120s)"
  for i in {1..24}; do
    if verify_gpu_idle "$pci_addr"; then
      log "GPU is idle"
      break
    fi
    if [[ $i -eq 24 ]]; then
      log "ERROR: GPU still in use after 120s, aborting"
      kubectl taint nodes "$NODE_NAME" "gpu-$gpu_index=gaming:NoExecute-" || true
      kubectl uncordon "$NODE_NAME"
      return 1
    fi
    sleep 5
  done
  
  # Phase 4: Driver switch with rollback
  log "Phase 4: Switching driver to vfio-pci"
  kubectl label nodes "$NODE_NAME" "gpu-$gpu_index-status=switching" --overwrite
  
  echo "$pci_addr" > /sys/bus/pci/drivers/nvidia/unbind 2>/dev/null || true
  echo "vfio-pci" > "/sys/bus/pci/devices/$pci_addr/driver_override"
  
  if ! echo "$pci_addr" > /sys/bus/pci/drivers/vfio-pci/bind; then
    log "ERROR: Failed to bind vfio-pci, rolling back"
    echo "" > "/sys/bus/pci/devices/$pci_addr/driver_override"
    echo "$pci_addr" > /sys/bus/pci/drivers/nvidia/bind || true
    kubectl taint nodes "$NODE_NAME" "gpu-$gpu_index=gaming:NoExecute-" || true
    kubectl label nodes "$NODE_NAME" "gpu-$gpu_index-status=error" --overwrite
    kubectl uncordon "$NODE_NAME"
    return 1
  fi
  
  # Phase 5: Start VM with timeout
  log "Phase 5: Starting VM $vm_name"
  if ! timeout 60 virsh start "$vm_name"; then
    log "ERROR: VM failed to start, rolling back"
    # Rollback driver...
    echo "$pci_addr" > /sys/bus/pci/drivers/vfio-pci/unbind 2>/dev/null || true
    echo "" > "/sys/bus/pci/devices/$pci_addr/driver_override"
    echo "$pci_addr" > /sys/bus/pci/drivers/nvidia/bind || true
    kubectl taint nodes "$NODE_NAME" "gpu-$gpu_index=gaming:NoExecute-" || true
    kubectl label nodes "$NODE_NAME" "gpu-$gpu_index-status=error" --overwrite
    kubectl uncordon "$NODE_NAME"
    return 1
  fi
  
  # Phase 6: Verify and finalize
  log "Phase 6: Verifying VM running"
  sleep 5
  if ! virsh domstate "$vm_name" | grep -q running; then
    log "ERROR: VM not running after start"
    # Rollback...
    return 1
  fi
  
  kubectl label nodes "$NODE_NAME" "gpu-$gpu_index-status=gaming" --overwrite
  log "=== GPU $gpu_index claimed successfully ==="
}

# ... (release_gpu with similar improvements)
```

---

*Review completed by: Sisyphus Agent*  
*Next: Address owner questions, then implement P0/P1 fixes*
