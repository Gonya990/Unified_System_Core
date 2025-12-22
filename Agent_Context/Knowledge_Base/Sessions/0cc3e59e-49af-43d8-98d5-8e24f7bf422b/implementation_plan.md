# IMPLEMENTATION PLAN: GRAND UNIFICATION (RELEASE CANDIDATE)

[CORE OBJECTIVE]
Establish a fully distributed, AI-driven infrastructure across the Tailscale Mesh, utilizing the specific strengths of each node: Mac (Orchestrator), Windows (Browser/GPU Gateway), and NODE-01 (TITAN GPU/AI).

[Orchestration Logic - FRACTAL AGENT TOPOLOGY]

* **Orchestrator Role (Mac):** High-level coordination, decision making, and n8n orchestration. Sends high-level objectives to specialized Sub-Agents.
* **Browser Gateway (Windows - 100.127.194.111):** The "Muscle" for browser execution. Each tab/extension is a "Sub-Agent" with context isolation.
* **Distributed Execution (MESH-TO-LOCAL):**
  * **Logic:** Stop monolithic browser management. Treat every service/port as a mesh resource.
  * **Network Fix:** Open Port 9222 (Windows Firewall) and launch Chrome with `--remote-debugging-address=0.0.0.0`.
* **"Learn before Act" Protocol:**
  * If an interface is unknown, use a "Search Agent" tab to find documentation/best practices.
  * Ingest findings and select Control Mode (Code/API preferred, Visual/Vision fallback).
* **Browsing/Surfing Protocol:**
  * Route all "Surf", "Scrape", or "Visit" requests directly to `100.127.194.111:9222`.
  * IGNORE Mac localhost for browsing.

[Phase 5: OMNISCIENCE & n8n Fixes]

* **n8n Workflow Update:**
  * Update all n8n nodes on the Mac to target `100.127.194.111` or `100.88.65.71` as appropriate.
  * Ensure "MCP Windows" tool uses Raw JSON and JSON-RPC 2.0.
* **Credential Extraction (Manual/CLI Strategy):**
  * **Primary:** `gcloud auth login --no-browser` via SSH on NODE-01.
  * **Secondary:** Manual download of `credentials.json` on Windows machine if CLI fails.
  * **Reason:** Automation over SSH tunnel is unreliable due to high latency.

[Phase 2: BIOS/Firmware Integration]

* **PiKVM Access:** Manage BIOS remotely via virtual console.
* **BIOS Tweaks:** Enable SVM, Above 4G Decoding, Re-size BAR.

[Verification Plan]

1. **Application Layer Test (CRITICAL):** `curl http://100.127.194.111:9222/json/version` from Mac. Success = Application-level connectivity.
2. **n8n Link Test:** Execute `check_docker` via fixed JSON targeting NODE-01.
3. **Firewall Audit:** `sudo ufw status` on NODE-01 to resolve closed ports issue.
4. **Credential Test:** Verify extracted keys work for Google Workspace/GitHub integrations.

[Protocol: NODE_INTEGRATION_V1 & TITAN]

* **NODE-01 (100.88.65.71):**
  * SSH Recovery Strategy: Prompt user to add public key via PiKVM or reset `gonya` password via console if unreachable.
  * Hardware Audit: Run `nvidia-smi` to confirm 24GB Titan RTX.
  * AI Deployment: Deploy Ollama (Llama-3-70b) if VRAM permits.

[NEW: NODE-PVE Integration]

* **Proxmox VE (100.74.194.25):**
  * Check port 8006 (Web UI) via Tailscale.
  * Assess resources for auxiliary AI services/DBs.

[Verification Plan]

1. **Tailscale Routing Test (CRITICAL):** Attempt to load a webpage via the Windows Machine's IP from the Mac Agent. Success = Content retrieved without local browser launch.
2. **n8n Link Test:** Execute `check_docker` via fixed JSON.
3. **NODE-01 Scan:** Verify Titan RTX via SSH.
