# Project Antigravity: Multi-Model AI Hub

## Phase 1: Foundation (Docker + GPU)

- [x] Connect n8n to Local Docker (Execute Command) <!-- id: 20 -->
- [x] Integrate Local GPU (Ollama) or NVIDIA API <!-- id: 21 -->
- [x] Prepare `server_config.env` for Windows Server <!-- id: 22 -->

## Phase 2: Brains (AI Models)

- [x] Google Vertex AI (Knowledge Base Deployed) <!-- id: 23 -->
- [x] Connect OpenAI (GPT-4) <!-- id: 24 -->
- [x] Implement AI Router (n8n Workflow) <!-- id: 25 -->

## Phase 3: Hands (Tools)

- [x] Connect GitHub (Repo Management) <!-- id: 26 -->
- [x] Configure Ngrok (External Access) <!-- id: 27 -->

## Phase 4: Integration

- [x] Assemble "Super-Scenario" (AI Agent Node) <!-- id: 28 -->
- [x] Auto-Deploy via API (`scripts/deploy_workflows.js`) <!-- id: 29 -->

## Phase 5: MCP Server (The New Core)

- [x] Scaffold `antigravity-mcp-server` project <!-- id: 30 -->
- [x] Implement `check_docker` & `check_gpu` tools <!-- id: 31 -->
- [x] Configure Stdio/HTTP transport <!-- id: 32 -->
- [x] Create Windows Launch Script (`start_mcp.bat`) <!-- id: 33 -->

## Phase 6: Command Center Setup (MacOS)

- [x] Install System Tools (gcloud, terraform, gemini-cli) <!-- id: 34 -->
- [x] Initialize Terraform (Google Cloud Repo) <!-- id: 35 -->
- [x] Create `scripts/n8n_check.js` (Sync Logic) <!-- id: 36 -->
- [x] Configure SSH access to Windows Server <!-- id: 37 -->
