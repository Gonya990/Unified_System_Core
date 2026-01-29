# Kubernetes + GPU Gaming Cluster - Agent Handoff Document

## Project Overview

**Owner:** Igoryan/Kostya - Senior Infrastructure & DevOps Engineer
**Background:** Experienced with K3s at work (Scopio Labs), AWS/on-premises hybrid infrastructure, Terraform, HIPAA/GDPR compliance

**Goal:** Deploy a Kubernetes cluster across 4 hosts to manage mixed workloads:
- LLM inference (vLLM, Ollama, etc.)
- AI workloads (Stable Diffusion, Whisper, etc.)
- Windows gaming VMs with GPU passthrough for 3 gamers

**Key Requirement:** When gamers use GPUs, AI workloads must gracefully yield without impacting gaming performance.

---

## Hardware Inventory

| Host | GPUs | Notes |
|------|------|-------|
| Node 1 | 1-2 GPUs (RTX 3080, RTX 2080 mix) | TBD exact config |
| Node 2 | 1-2 GPUs (RTX 3080, RTX 2080 mix) | TBD exact config |
| Node 3 | 1-2 GPUs (RTX 3080, RTX 2080 mix) | TBD exact config |
| Node 4 | 1-2 GPUs (RTX 3080, RTX 2080 mix) | TBD exact config |

**Total:** ~6-8 GPUs across 4 hosts, 3 gamers need GPU access

---

## Architecture Decision: Option 2 - Hybrid Approach

After evaluating options, the chosen architecture is:

```
┌──────────────────────────────────────────────────────────────────┐
│  Each Host                                                       │
│                                                                  │
│  ┌─────────────────────┐     ┌─────────────────────────────────┐│
│  │ libvirt/QEMU        │     │ K3s Agent                       ││
│  │                     │     │                                 ││
│  │ Windows Gaming VMs  │     │  ┌─────────┐  ┌─────────┐      ││
│  │ (on-demand)         │     │  │ vLLM    │  │ SD      │      ││
│  │                     │     │  │ Pod     │  │ Pod     │      ││
│  └──────────┬──────────┘     └──┴────┬────┴──┴────┬────┴──────┘│
│             │                        │            │             │
│             ▼                        ▼            ▼             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   GPU Arbiter Service                     │  │
│  │          (manages driver binding + K3s taints)            │  │
│  └──────────────────────────────────────────────────────────┘  │
│             │                        │            │             │
│             ▼                        ▼            ▼             │
│         GPU 0                    GPU 1        GPU 2            │
│      (vfio/nvidia)            (nvidia)      (nvidia)           │
└──────────────────────────────────────────────────────────────────┘
```

### Why This Approach

| Component | Manager | Rationale |
|-----------|---------|-----------|
| Windows gaming VMs | **libvirt/QEMU** | GPU passthrough is mature, well-documented, reliable |
| AI workloads | **K3s** | Container orchestration, scaling, scheduling |
| GPU arbitration | **Custom scripts** | Bridges the two, handles driver switching |

### Why NOT KubeVirt for Gaming VMs

1. Added complexity — KubeVirt is another layer on top of libvirt
2. GPU hot-plug limitations — less flexible for passthrough
3. Debugging pain — Kubernetes → KubeVirt → libvirt → QEMU stack
4. Overkill — 3 fixed gaming VMs, not dynamically scaling

---

## Distribution Decision

### Recommended: NixOS

**Rationale:**
- Declarative configuration fits managing 4 identical hosts
- One config, deploy everywhere
- Atomic rollbacks (critical for GPU driver experiments)
- Reproducibility across all nodes
- Infrastructure-as-code native

**Alternative:** Ubuntu 24.04 LTS or Fedora Server if faster deployment is needed

**Avoid:** Proxmox (hypervisor conflict), Rocky/Alma (old kernel), Talos (no libvirt)

---

## GPU Lifecycle Management

### The Core Challenge

GPU passthrough for gaming requires **exclusive** GPU access via VFIO. Cannot time-slice between passthrough VM and containers.

**Model:** Gaming claims GPU → AI workloads yield → Gaming releases → AI reclaims

### Mechanism: Taints + Labels

| Mechanism | Purpose |
|-----------|---------|
| `Taint: NoExecute` | Evicts running AI pods from GPU |
| `Labels` | Visibility, scheduling decisions |

### Launch Flow (Gamer Starts Gaming)

```
Gamer triggers "Start Gaming"
            │
            ▼
┌──────────────────────────────────────┐
│ 1. Add NoExecute taint to node       │
│    kubectl taint nodes $NODE         │
│    gpu-$INDEX=gaming:NoExecute       │
│    (pods start evicting)             │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 2. Wait for GPU-using pods to        │
│    terminate (with timeout ~120s)    │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 3. Unbind GPU from nvidia driver     │
│    echo $PCI > nvidia/unbind         │
│    Bind to vfio-pci                  │
│    echo $PCI > vfio-pci/bind         │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 4. Start Windows VM via libvirt      │
│    virsh start win-gaming-$INDEX     │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 5. Update label for visibility       │
│    gpu-$INDEX-status=gaming          │
└──────────────────────────────────────┘
```

### Shutdown Flow (Gamer Stops Gaming)

```
Gamer shuts down Windows / triggers "Stop Gaming"
            │
            ▼
┌──────────────────────────────────────┐
│ 1. VM shuts down (graceful + force)  │
│    virsh shutdown $VM                │
│    sleep 30                          │
│    virsh destroy $VM (if needed)     │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 2. Unbind GPU from vfio-pci          │
│    Bind back to nvidia driver        │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 3. Remove NoExecute taint            │
│    kubectl taint nodes $NODE         │
│    gpu-$INDEX=gaming:NoExecute-      │
└──────────────────┬───────────────────┘
                   ▼
┌──────────────────────────────────────┐
│ 4. Update label                      │
│    gpu-$INDEX-status=available       │
└──────────────────┬───────────────────┘
                   ▼
        K8s scheduler sees GPU available
        AI pods can schedule again
```

---

## Known Risk: GPU Reset Bug

### The Problem

Some NVIDIA GPUs don't properly reset state when VM shuts down:
- VM shuts down → GPU stays "dirty" → Next VM start fails or nvidia rebind fails
- **Requires host reboot to recover**

### Affected Cards

| Card | Status |
|------|--------|
| RTX 2080 | Generally works, some reports of issues |
| RTX 3080 | Mixed reports — varies by vendor/VBIOS |

### Mitigation Options

1. **Test first** — Run reset cycle test before committing to architecture
2. **vendor-reset kernel module** — Community fix for problematic GPUs
3. **Dedicated GPUs** — Don't share if reset bug is present
4. **Scheduled transitions** — Reboot between modes if needed

### Pre-Flight Test Script

```bash
#!/bin/bash
# Test GPU reset cycle - run BEFORE full setup

GPU_PCI="${1:-0000:01:00.0}"
CYCLES="${2:-5}"

echo "Testing GPU reset on $GPU_PCI for $CYCLES cycles"

for i in $(seq 1 $CYCLES); do
    echo "=== Cycle $i/$CYCLES ==="
    
    # Unbind nvidia
    echo "$GPU_PCI" > /sys/bus/pci/drivers/nvidia/unbind 2>/dev/null || true
    sleep 1
    
    # Bind vfio
    echo "vfio-pci" > /sys/bus/pci/devices/$GPU_PCI/driver_override
    echo "$GPU_PCI" > /sys/bus/pci/drivers/vfio-pci/bind
    sleep 2
    
    # Unbind vfio
    echo "$GPU_PCI" > /sys/bus/pci/drivers/vfio-pci/unbind
    sleep 1
    
    # Rebind nvidia
    echo "" > /sys/bus/pci/devices/$GPU_PCI/driver_override
    echo "$GPU_PCI" > /sys/bus/pci/drivers/nvidia/bind
    sleep 2
    
    # Test
    if nvidia-smi > /dev/null 2>&1; then
        echo "✓ Cycle $i passed"
    else
        echo "✗ Cycle $i FAILED - reset bug detected"
        exit 1
    fi
done

echo "=== All $CYCLES cycles passed - GPU handles reset properly ==="
```

---

## NixOS Configuration Structure

### Flake Layout

```
~/nixos-cluster/
├── flake.nix
├── flake.lock
├── modules/
│   ├── common.nix        # Base system, users, SSH
│   ├── nvidia.nix        # nvidia driver, container toolkit
│   ├── vfio.nix          # VFIO modules, IOMMU config
│   ├── libvirt.nix       # libvirt, QEMU, OVMF
│   ├── k3s.nix           # K3s server/agent config
│   └── gpu-arbiter.nix   # GPU switching scripts
└── hosts/
    ├── node1.nix         # Server node, GPU mappings
    ├── node2.nix         # Agent node
    ├── node3.nix         # Agent node
    └── node4.nix         # Agent node
```

### flake.nix

```nix
{
  description = "AI + Gaming Cluster";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  };

  outputs = { self, nixpkgs }: {
    nixosConfigurations = {
      node1 = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./modules/common.nix
          ./modules/nvidia.nix
          ./modules/vfio.nix
          ./modules/libvirt.nix
          ./modules/k3s.nix
          ./modules/gpu-arbiter.nix
          ./hosts/node1.nix
        ];
      };
      
      node2 = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          ./modules/common.nix
          ./modules/nvidia.nix
          ./modules/vfio.nix
          ./modules/libvirt.nix
          ./modules/k3s.nix
          ./modules/gpu-arbiter.nix
          ./hosts/node2.nix
        ];
      };
      
      # node3, node4 similar
    };
  };
}
```

### modules/common.nix

```nix
{ config, pkgs, ... }:

{
  system.stateVersion = "24.05";
  
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;
  boot.kernelPackages = pkgs.linuxPackages_latest;
  
  # IOMMU - critical for passthrough
  boot.kernelParams = [
    "intel_iommu=on"  # or amd_iommu=on
    "iommu=pt"
  ];
  
  environment.systemPackages = with pkgs; [
    vim git htop pciutils usbutils lshw tmux jq kubectl k9s
  ];
  
  services.openssh.enable = true;
  
  networking.firewall = {
    enable = true;
    allowedTCPPorts = [ 22 6443 10250 ];
  };
  
  users.users.admin = {
    isNormalUser = true;
    extraGroups = [ "wheel" "libvirtd" "docker" ];
    openssh.authorizedKeys.keys = [
      "ssh-ed25519 AAAA... your-key-here"
    ];
  };
  
  security.sudo.wheelNeedsPassword = false;
}
```

### modules/nvidia.nix

```nix
{ config, pkgs, lib, ... }:

{
  services.xserver.videoDrivers = [ "nvidia" ];
  
  hardware.nvidia = {
    package = config.boot.kernelPackages.nvidiaPackages.stable;
    modesetting.enable = true;
    powerManagement.enable = false;
    open = false;
    nvidiaSettings = false;
  };
  
  hardware.opengl = {
    enable = true;
    driSupport = true;
    driSupport32Bit = true;
  };
  
  hardware.nvidia-container-toolkit.enable = true;
  
  # Allow vfio to claim GPU before nvidia if configured
  boot.extraModprobeConfig = ''
    softdep nvidia pre: vfio-pci
  '';
}
```

### modules/vfio.nix

```nix
{ config, pkgs, lib, ... }:

{
  boot.kernelModules = [
    "vfio_pci"
    "vfio"
    "vfio_iommu_type1"
  ];
  
  boot.initrd.kernelModules = [
    "vfio_pci"
    "vfio"
    "vfio_iommu_type1"
  ];
  
  boot.extraModprobeConfig = ''
    options vfio-pci disable_vga=1
  '';
  
  # IOMMU group checker utility
  environment.systemPackages = with pkgs; [
    (writeShellScriptBin "iommu-groups" ''
      for d in /sys/kernel/iommu_groups/*/devices/*; do
        n=$(basename $(dirname $(dirname $d)))
        echo "IOMMU Group $n: $(${pkgs.pciutils}/bin/lspci -nns ''${d##*/})"
      done | sort -V
    '')
  ];
}
```

### modules/libvirt.nix

```nix
{ config, pkgs, ... }:

{
  virtualisation.libvirtd = {
    enable = true;
    
    qemu = {
      package = pkgs.qemu_kvm;
      
      ovmf = {
        enable = true;
        packages = [ pkgs.OVMFFull.fd ];
      };
      
      verbatimConfig = ''
        cgroup_device_acl = [
          "/dev/null", "/dev/full", "/dev/zero",
          "/dev/random", "/dev/urandom",
          "/dev/ptmx", "/dev/kvm",
          "/dev/vfio/vfio"
        ]
      '';
    };
  };
  
  environment.systemPackages = with pkgs; [
    virt-manager virt-viewer spice-gtk
  ];
}
```

### modules/k3s.nix

```nix
{ config, pkgs, lib, ... }:

{
  services.k3s = {
    enable = true;
    role = "agent";  # Override to "server" on node1
    serverAddr = "https://node1:6443";
    tokenFile = "/etc/k3s/token";
    extraFlags = toString [
      "--kubelet-arg=feature-gates=DevicePlugins=true"
    ];
  };
  
  environment.systemPackages = with pkgs; [
    kubectl kubernetes-helm k9s
  ];
  
  environment.etc."k3s/token" = {
    text = "CHANGE-THIS-CLUSTER-TOKEN";
    mode = "0600";
  };
}
```

### modules/gpu-arbiter.nix

```nix
{ config, pkgs, lib, ... }:

let
  gpu-arbiter = pkgs.writeShellScriptBin "gpu-arbiter" ''
    #!${pkgs.bash}/bin/bash
    set -euo pipefail
    
    export PATH="${lib.makeBinPath [ 
      pkgs.coreutils pkgs.pciutils pkgs.kmod 
      pkgs.libvirt pkgs.kubectl pkgs.jq 
    ]}:$PATH"
    
    source /etc/gpu-arbiter/config
    
    log() { echo "[$(date '+%H:%M:%S')] $*"; }
    
    claim_gpu() {
      local gpu_index="$1"
      local pci_addr="''${GPU_PCI[$gpu_index]}"
      local vm_name="''${VM_NAMES[$gpu_index]}"
      
      log "Claiming GPU $gpu_index ($pci_addr) for gaming..."
      
      # Taint to evict pods
      kubectl taint nodes "$NODE_NAME" \
        "gpu-$gpu_index=gaming:NoExecute" --overwrite || true
      
      kubectl label nodes "$NODE_NAME" \
        "gpu-$gpu_index-status=draining" --overwrite
      
      # Wait for drain
      log "Waiting for pods to drain..."
      sleep 30
      
      # Switch driver
      echo "$pci_addr" > /sys/bus/pci/drivers/nvidia/unbind 2>/dev/null || true
      echo "vfio-pci" > "/sys/bus/pci/devices/$pci_addr/driver_override"
      echo "$pci_addr" > /sys/bus/pci/drivers/vfio-pci/bind
      
      # Start VM
      virsh start "$vm_name"
      
      kubectl label nodes "$NODE_NAME" \
        "gpu-$gpu_index-status=gaming" --overwrite
      
      log "✓ GPU $gpu_index claimed for gaming"
    }
    
    release_gpu() {
      local gpu_index="$1"
      local pci_addr="''${GPU_PCI[$gpu_index]}"
      local vm_name="''${VM_NAMES[$gpu_index]}"
      
      log "Releasing GPU $gpu_index..."
      
      # Stop VM
      virsh shutdown "$vm_name" 2>/dev/null || true
      sleep 30
      virsh destroy "$vm_name" 2>/dev/null || true
      
      # Switch driver back
      echo "$pci_addr" > /sys/bus/pci/drivers/vfio-pci/unbind 2>/dev/null || true
      echo "" > "/sys/bus/pci/devices/$pci_addr/driver_override"
      echo "$pci_addr" > /sys/bus/pci/drivers/nvidia/bind
      
      # Remove taint
      kubectl taint nodes "$NODE_NAME" \
        "gpu-$gpu_index=gaming:NoExecute-" || true
      
      kubectl label nodes "$NODE_NAME" \
        "gpu-$gpu_index-status=available" --overwrite
      
      log "✓ GPU $gpu_index released to AI workloads"
    }
    
    status() {
      echo "GPU Status:"
      for i in "''${!GPU_PCI[@]}"; do
        local pci="''${GPU_PCI[$i]}"
        local driver=$(lspci -k -s "$pci" | grep "Kernel driver" | awk '{print $5}')
        local k8s_status=$(kubectl get node "$NODE_NAME" \
          -o jsonpath="{.metadata.labels.gpu-$i-status}" 2>/dev/null || echo "unknown")
        echo "  GPU $i ($pci): driver=$driver, k8s=$k8s_status"
      done
    }
    
    case "''${1:-status}" in
      claim)   claim_gpu "''${2:?GPU index required}" ;;
      release) release_gpu "''${2:?GPU index required}" ;;
      status)  status ;;
      *)       echo "Usage: gpu-arbiter {claim|release|status} [gpu_index]" ;;
    esac
  '';

in {
  environment.systemPackages = [ gpu-arbiter ];
  
  environment.etc."gpu-arbiter/config" = {
    text = ''
      declare -A GPU_PCI
      declare -A VM_NAMES
      NODE_NAME="$(hostname)"
      
      # Override per host in hosts/*.nix
      GPU_PCI[0]="0000:01:00.0"
      VM_NAMES[0]="win-gaming-0"
    '';
  };
}
```

### hosts/node1.nix (K3s Server)

```nix
{ config, pkgs, ... }:

{
  networking.hostName = "node1";
  
  services.k3s = {
    role = "server";
    extraFlags = toString [
      "--cluster-init"
      "--disable=traefik"
    ];
  };
  
  environment.etc."gpu-arbiter/config" = {
    text = ''
      declare -A GPU_PCI
      declare -A VM_NAMES
      NODE_NAME="node1"
      
      GPU_PCI[0]="0000:01:00.0"  # RTX 3080
      GPU_PCI[1]="0000:02:00.0"  # RTX 2080
      
      VM_NAMES[0]="win-gaming-0"
      VM_NAMES[1]="win-gaming-1"
    '';
    mode = "0644";
  };
  
  networking.interfaces.enp0s31f6.ipv4.addresses = [{
    address = "192.168.1.101";
    prefixLength = 24;
  }];
}
```

---

## AI Workload Configuration

### Example Deployment (vLLM)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-inference
  namespace: ai-workloads
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vllm
  template:
    metadata:
      labels:
        app: vllm
    spec:
      # Graceful termination for preemption
      terminationGracePeriodSeconds: 30
      
      # Only schedule on nodes with available GPUs
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: gpu-0-status
                operator: In
                values: ["available"]
            - matchExpressions:
              - key: gpu-1-status
                operator: In
                values: ["available"]
      
      # NO toleration for gpu-X=gaming:NoExecute
      # This ensures eviction when taint is applied
      
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        resources:
          limits:
            nvidia.com/gpu: 1
        
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 5"]
        
        env:
        - name: MODEL
          value: "mistralai/Mistral-7B-Instruct-v0.2"
```

---

## Host Prerequisites Checklist

Before setup, verify on each host:

```bash
# 1. IOMMU enabled
dmesg | grep -i iommu

# 2. GPU PCI addresses
lspci | grep -i nvidia

# 3. IOMMU groups (GPUs should be isolated)
# Use iommu-groups script after NixOS install, or:
for d in /sys/kernel/iommu_groups/*/devices/*; do
  n=$(basename $(dirname $(dirname $d)))
  echo "IOMMU Group $n: $(lspci -nns ${d##*/})"
done | sort -V

# 4. Check BIOS settings
# - VT-d (Intel) or AMD-Vi enabled
# - IOMMU enabled
# - ACS if available
```

### Good IOMMU Group (isolated)

```
IOMMU Group 12: 01:00.0 VGA compatible controller: NVIDIA RTX 3080
IOMMU Group 12: 01:00.1 Audio device: NVIDIA HD Audio
```

### Bad IOMMU Group (shared - problematic)

```
IOMMU Group 1: 00:01.0 PCI bridge
IOMMU Group 1: 01:00.0 VGA compatible controller: NVIDIA RTX 3080
IOMMU Group 1: 02:00.0 USB controller   <-- problem
```

If groups are bad, options:
- ACS override patch (security tradeoff)
- Different PCIe slot
- Different motherboard

---

## Deployment Steps

### Phase 1: Test Reset Bug

On each host (before NixOS install if possible):

1. Run reset cycle test on each GPU
2. If passes → proceed with dynamic switching
3. If fails → install vendor-reset module or use dedicated GPUs

### Phase 2: NixOS Installation

```bash
# On each node
git clone https://github.com/YOUR_REPO/nixos-cluster.git
cd nixos-cluster

# Node 1 (server)
sudo nixos-rebuild switch --flake .#node1

# Node 2-4 (agents)
sudo nixos-rebuild switch --flake .#node2
# etc.

# Or remote deploy from workstation
nixos-rebuild switch --flake .#node1 --target-host root@node1
```

### Phase 3: K3s Cluster Setup

1. Verify cluster health: `kubectl get nodes`
2. Install NVIDIA device plugin
3. Deploy AI workloads with proper affinity rules
4. Test taint/drain mechanism manually

### Phase 4: Windows VM Setup

1. Create Windows VMs with GPU passthrough in libvirt
2. Configure OVMF/UEFI boot
3. Test manual GPU switching
4. Test full lifecycle with gpu-arbiter

### Phase 5: Automation & Triggers

Options for how gamers trigger GPU claim:
- CLI script (ssh + sudo gpu-arbiter claim 0)
- Simple web UI (FastAPI service)
- Discord bot
- Home Assistant integration

---

## Open Questions for Next Agent

1. **Exact hardware inventory** — Need PCI addresses for each GPU on each host
2. **Network topology** — Static IPs, which node is K3s server
3. **Gaming schedule** — Predictable (evenings) vs unpredictable (anytime)?
4. **Reset bug testing** — Has each GPU been tested?
5. **Trigger preference** — How should gamers claim GPUs?
6. **Monitoring requirements** — Grafana, alerts?

---

## Key Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| VM management | libvirt (not KubeVirt) | Simpler, more reliable GPU passthrough |
| K8s distribution | K3s | Owner's familiarity, lightweight |
| Host OS | NixOS | Reproducibility, rollback safety |
| GPU arbitration | NoExecute taints + labels | K8s-native eviction mechanism |
| Scheduling | Affinity rules | Prevents AI pods on claimed GPUs |

---

## Reference Links

- [Arch Wiki - PCI Passthrough](https://wiki.archlinux.org/title/PCI_passthrough_via_OVMF)
- [NixOS Manual - Virtualization](https://nixos.wiki/wiki/Libvirt)
- [vendor-reset module](https://github.com/gnif/vendor-reset)
- [K3s Documentation](https://docs.k3s.io/)
- [NVIDIA Device Plugin](https://github.com/NVIDIA/k8s-device-plugin)

---

*Document generated: Handoff for Kubernetes + GPU Gaming Cluster Project*
