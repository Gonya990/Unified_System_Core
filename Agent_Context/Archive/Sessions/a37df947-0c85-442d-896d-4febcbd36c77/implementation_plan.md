# Project Antigravity: Implementation Plan

## Goal
Build a "Unified Command Center" where n8n acts as the orchestrator for a Multi-Model AI Agent, managing "Brains" (AI Models) and "Hands" (Docker, GitHub, System).

## Architecture

### 1. The Conductor (n8n Setup)
- **Host:** Windows Server (User's Machine)
- **Access:** Localhost / Tailscale
- **Orchestration:** Directed Acyclic Graphs (workflows) routing tasks to specialized agents.

### 2. The Brains (AI Models)
| Model | Status | Use Case |
| :--- | :--- | :--- |
| **Vertex AI** | ✅ Deployed | Context, Docs, Enterprise Search |
| **OpenAI (GPT)** | ⏳ Pending | Coding, Complex Logic |
| **NVIDIA/Ollama** | ⏳ Pending | Local GPU, Privacy, 24/7 Tasks |

### 3. The Hands (Tools)
- **Docker:** Controlled via `Execute Command` node.
- **GitHub:** Native n8n integration.
- **Ngrok:** Tunneling for external webhooks.

## Execution Steps

### Step 1: Foundation (Docker + GPU)
- [ ] **Config:** generated `server_config.env` for Windows.
- [ ] **Docker:** Validate `Execute Command` node rights.
- [ ] **GPU:** Connect Ollama (http://host.docker.internal:11434).

### Step 2: Integration
- Configure Credentials in n8n for OpenAI, GitHub, NVIDIA.
- Build the "AI Router" workflow.

## Phase 5: Migration to MCP (Model Context Protocol)

We are moving away from n8n as the "tool executor" to a dedicated **MCP Server**.

### Architecture
1.  **Antigravity MCP Server (Node.js)**
    *   Runs on Windows.
    *   Uses `@modelcontextprotocol/sdk`.
    *   Exposes Tools: `docker_control`, `gpu_status`.
2.  **Transport**
    *   **Stdio:** For local LLM (Claude App / Gemini Desktop).
    *   **SSE/HTTP (via Ngrok):** For cloud-based Agents (n8n Cloud, etc).

### Server Structure
- `src/index.ts`: Main server entrypoint.
- `src/tools/docker.ts`: Dockerode / API integration.
- `src/tools/ollama.ts`: Ollama API integration.


## Требуется участие пользователя
- **API Keys**: Для настройки подключения мне понадобятся API ключи от обоих экземпляров n8n (Settings -> API).

## Предлагаемые изменения

### Скрипты
#### [NEW] [scripts/n8n_check.js](file:///Users/macbook/.gemini/antigravity/playground/solar-curie/scripts/n8n_check.js)
Скрипт для проверки доступности и синхронизации рабочих процессов между серверами.

### Gemini CLI
#### [NEW] [Установка]
Установим `gemini-cli` глобально или локально для использования в терминале.
Команда: `npm install -g @google/gemini-cli`.

## Что делать с Google Cloud Repo?
Этот репозиторий требует `gcloud` и `terraform`.

### Установка инструментов
#### [NEW] [gcloud CLI]
Установка Google Cloud SDK для аутентификации в облаке.
Команда: `brew install --cask google-cloud-sdk`

#### [NEW] [Terraform]
Установка Terraform для развертывания инфраструктуры.
Команда: `brew install terraform`

### Развертывание
1. Аутентификация: `gcloud auth application-default login`
2. Инициализация: `terraform init`
3. Применение: `terraform apply`
