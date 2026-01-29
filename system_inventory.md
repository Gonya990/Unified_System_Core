# System Inventory / Инвентаризация Системы

## Hardware Resources (Аппаратные Ресурсы)

### 1. Primary Host (Admin Control)

- **Device**: MacBook
- **Role**: Management & Control Plane (Рабочая зона управления)
- **User**: igor/gonya
- **Tailscale IP**: `100.93.121.47` (MacBook Air)

### 2. Windows AI Host (igor-gaming)

- **Device**: Windows PC (RTX AI Core)
- **Tailscale IP**: `100.127.194.111` (Active, Direct Connection)
- **Role**: AI Inference, N8N, & Computation.
- **Components**:
  - **WSL/SSH (22)**: ✅ Open/Verified.
  - **RDP (3389)**: ✅ Open/Verified.
  - **N8N (5678)**: ✅ Open/Verified (Automation Layer).
  - **GPU**: ASUS GeForce (Ready).

### 3. Proxmox Virtual Environment

- **Device**: Server (Virtualization)
- **Tailscale IP**: `100.74.194.25` (Active, SSH Open)
- **Role**: Host for VMs and Containers.
- **Components**:
  - **RAM**: ✅ **64GB Verified** (62Gi Total available).
  - **Status**: Online.

## Software Resources (Программные Ресурсы)

### Active Working Zones (Unified_System)

- **Location**: `/Users/macbook/Documents/Unified_System`
- **Modules**:
  - `Windows_AI_Core`: RTX AI setup scripts.
  - `Home_Assistant_Config`: Smart home automation config.
  - `Sandbox`: Testing and script development area.

### Network

- **Mesh**: Tailscale (Active on all nodes)
- **Local Access**: Admin verified.
