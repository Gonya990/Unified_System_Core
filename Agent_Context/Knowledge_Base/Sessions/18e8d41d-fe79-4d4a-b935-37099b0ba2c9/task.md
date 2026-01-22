 Task: System Synchronization and Status Check (Sequential Plan)

## Phase 1: A - Network & Server Status (Wake on LAN) <!-- id: 100 -->

- [x] Verify Local Network (Tailscale Up) <!-- id: 101 -->
- [x] Ping Servers (igor-gaming, pve) <!-- id: 102 -->

- [ ] Attempt Wake-on-LAN (if offline) <!-- id: 103 -->

## Phase 2: B - Data Synchronization (GitHub cloud) <!-- id: 200 -->

- [x] Local Commit (Autosave) <!-- id: 201 -->
- [x] Push to GitHub (Vibranium Sync) <!-- id: 202 -->
- [ ] Verify GitHub Artifacts <!-- id: 203 -->

## Phase 3: C - Access Control (SSH) <!-- id: 300 -->

- [x] Check SSH Status <!-- id: 301 -->
- [x] Enable Remote Login (User Manual Action) <!-- id: 302 -->
- [x] Verify Connection from generic device <!-- id: 303 -->

## Phase 4: D - Unified Core Deployment (Factory Restart) <!-- id: 400 -->

- [x] Establish SSH Alias for igor-windows <!-- id: 401 -->
- [x] Connect Google Cloud Project (Vertex AI) <!-- id: 402 -->
- [x] Enable Billing & APIs (Linked: `01981C-43E011-FC0292`) <!-- id: 402b -->
- [x] Define AI Providers Configuration <!-- id: 403 -->
- [x] Install Git LFS on Mac (Completed manually) <!-- id: 403b -->
- [/] Deploy OpenCode/Ollama on Windows (WSL Bypass Active - Pulling Images...) <!-- id: 404 -->
- [ ] Launch Docker Containers (Unified Core) <!-- id: 405 -->
