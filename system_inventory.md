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
  - **VMs**:
    - `100/101` (Gaming/Old).
    - `106` (unified-home-core): Ubuntu 22.04 Cloud, 4GB RAM, 2 Cores. (Deploying...)

### 4. Планшет Артура (Контроль ребёнка)

- **Device**: Lenovo TB-J606F (Tab P11)
- **Tailscale IP**: `100.114.27.103`
- **Local IP**: `192.168.190.111`
- **Role**: Детский планшет с родительским контролем
- **User**: Артур (<arturgoncarenko92@gmail.com>)
- **Parents**: <gonya90.gg@gmail.com>, <OksanaGorodetski@gmail.com>
- **Components**:
  - **Family Link**: ✅ Активен (родительский контроль)
  - **ADB (5555)**: ✅ Открыт через Tailscale
  - **Geolocation**: ✅ HIGH_ACCURACY
  - **Tailscale VPN**: ✅ Постоянно подключен

## Software Resources (Программные Ресурсы)

### Active Working Zones (Unified_System)

- **Location**: `/Users/macbook/Documents/Unified_System`
- **Modules**:
  - `Windows_AI_Core`: RTX AI setup (Cleaned & Structured: src/scripts/docs).
  - `_Archive/Home_Assistant_Config`: Archived (Old config).
  - `Sandbox`: Testing and script development area.

### Network

- **Mesh**: Tailscale (Active on all nodes)
- **Local Access**: Admin verified.
