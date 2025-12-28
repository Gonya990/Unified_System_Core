# 🔑 API Keys & Credentials Map (Detailed)

> **Last Updated:** 2025-12-28 20:26 IST
> **Host:** igor-gaming-1 (WSL2 Ubuntu on Windows)

---

## 🏗️ Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                            igor-gaming-1 (WSL2)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    SYSTEMD SERVICES (Native)                          │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  ai-bot.service ──────> EnvironmentFile=.env                          │   │
│  │  ollama.service ──────> OLLAMA_HOST=0.0.0.0:11434 (no API key)       │   │
│  │  gcp-metrics.service ─> GOOGLE_APPLICATION_CREDENTIALS=json file     │   │
│  │  nodered.service ─────> PATH only (keys stored in Node-RED flows)    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DOCKER CONTAINERS                                   │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  acfs-hub-server-1 ───> HTTP_BEARER_TOKEN env var                     │   │
│  │  n8n ─────────────────> WEBHOOK_URL (credentials in n8n UI)           │   │
│  │  chrome-headless ─────> No credentials                                 │   │
│  │  postgres:16 ─────────> Internal DB for acfs-hub                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Complete Service Inventory

### 1. **ai-bot.service** (Telegram Bot)

| Property | Value |
|----------|-------|
| **Type** | systemd (system) |
| **Status** | ✅ Running |
| **WorkingDirectory** | `/home/gonya/Documents/Unified_System/Windows_AI_Core` |
| **ExecStart** | `python -m src.main` |
| **EnvironmentFile** | `/home/gonya/Documents/Unified_System/Windows_AI_Core/.env` |

#### Environment Variables (from /proc)

```bash
TELEGRAM_BOT_TOKEN=8518131338:AAFzuwI6PJ7ftiZVe3u8cWtjYz1pSU_QIqQ
GEMINI_API_KEY=AIzaSyArS5zpJFROWX0VQ33RdW0XMn-XW94Ud7E
OPENAI_API_KEY=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
OPENAI_BASE_URL=https://api.openai.com
INFERENCE_API_KEY=
SERPAPI_KEY=e0c281fcc3fc567af344c430e4c1d15c808aa38672274f8319716f9bc5ae1c9c
LINEAR_API_KEY=lin_api_3BlNd7FQOgeJQpJEojnJVSaVPXqRatQM1TmwfghK
```

#### How Keys Are Used

**TELEGRAM_BOT_TOKEN:**

```python
# bot_config.py (HARDCODED - redundant!)
BOT_TOKEN = "8518131338:AAFzuw..."

# config_manager.py (via .env)
"TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN", "")

# ai_telegram_bot.py uses:
token = bot_config.BOT_TOKEN  # ← Uses hardcoded version!
```

**GEMINI_API_KEY:**

```python
# config_manager.py
"GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))

# inference_client.py
def api_key(self) -> str:
    if provider == "gemini":
        return self.config.get("GEMINI_API_KEY", ...)

# Used in:
client = genai.Client(api_key=api_key)  # Line 26
```

**OPENAI_API_KEY:**

```python
# inference_client.py
def api_key(self) -> str:
    if provider == "openai":
        return self.config.get("OPENAI_API_KEY", self.config.get("INFERENCE_API_KEY", ""))

# Used in:
headers = {"Authorization": f"Bearer {current_key}"}  # Line 95
```

**SERPAPI_KEY:**

```python
# web_search.py
self.serp_api_key = os.getenv("SERPAPI_KEY")  # Line 16

# Used in:
search = GoogleSearch({
    "q": query,
    "api_key": self.serp_api_key,  # Line 43
})
```

**LINEAR_API_KEY:**

```text
# Currently loaded but not actively used in main bot code
# Reserved for future Linear.app integration
```

---

### 2. **ollama.service** (Local LLM)

| Property | Value |
|----------|-------|
| **Type** | systemd (system) |
| **Status** | ✅ Running |
| **ExecStart** | `/home/gonya/bin/ollama serve` |

#### Environment Variables

```bash
OLLAMA_HOST=0.0.0.0:11434
OLLAMA_ORIGINS=*
```

#### How It's Used

```python
# inference_client.py
def base_url(self) -> str:
    if provider == "ollama":
        return self.config.get("OLLAMA_BASE_URL", "http://localhost:11434")

# No API key needed - local service
# Bot calls: http://localhost:11434/api/generate
```

---

### 3. **gcp-metrics-collector.service** (GCP Monitoring)

| Property | Value |
|----------|-------|
| **Type** | systemd (user) |
| **Status** | ✅ Running |

#### GCP Environment Variables

```bash
GOOGLE_APPLICATION_CREDENTIALS=/home/gonya/gcp-monitoring-key.json
GCP_PROJECT_ID=my-home-435112
```

#### GCP Keys Usage

```python
# gcp_metrics_collector.py
# Uses Application Default Credentials (ADC)
# The GOOGLE_APPLICATION_CREDENTIALS env var points to service account JSON

client = monitoring_v3.MetricServiceClient()  # Line 116
# Client auto-loads credentials from GOOGLE_APPLICATION_CREDENTIALS

client.create_time_series(...)  # Line 130
```

---

### 4. **nodered.service** (Node-RED Automation)

| Property | Value |
|----------|-------|
| **Type** | systemd (user) |
| **Status** | ✅ Running |

#### Node-RED Environment Variables

```bash
NODE_OPTIONS=--max-old-space-size=512
PATH=/home/gonya/.nvm/versions/node/v24.11.1/bin:...
```

#### Node-RED Keys Usage

- **No API keys in environment**
- Keys stored in Node-RED flows (`~/.node-red/flows.json`)
- Configured via Node-RED UI at `http://localhost:1880`

---

## 🐳 Docker Containers

### 5. **acfs-hub-server-1** (MCP Agent Mail)

| Property | Value |
|----------|-------|
| **Image** | `acfs-hub-server` (custom) |
| **Status** | ✅ Running |
| **Port** | 8765:8765 |
| **Compose** | `/home/gonya/acfs-hub/docker-compose.yml` |

#### ACFS-Hub Environment Variables

```bash
DATABASE_URL=sqlite+aiosqlite:////opt/mcp-agent-mail/data/agent_mail.db
HTTP_BEARER_TOKEN=antigravity_secret
HTTP_HOST=0.0.0.0
```

#### ACFS-Hub Keys Usage

```yaml
# docker-compose.yml
environment:
  HTTP_BEARER_TOKEN: antigravity_secret

# Clients must send:
# Authorization: Bearer antigravity_secret
```

---

### 6. **n8n** (Workflow Automation)

| Property | Value |
|----------|-------|
| **Image** | `n8nio/n8n` |
| **Status** | ✅ Running |
| **Port** | 5678:5678 |

#### n8n Environment Variables

```bash
WEBHOOK_URL=http://localhost:5678/
```

#### n8n Keys Usage

- **No API keys in Docker env**
- All credentials stored in n8n's encrypted database
- Configured via n8n UI at `http://localhost:5678`
- Supports: Telegram, OpenAI, HTTP, etc. via credential manager

---

### 7. **chrome-headless** (Browser Automation)

| Property | Value |
|----------|-------|
| **Image** | `zenika/alpine-chrome:latest` |
| **Status** | ✅ Running |
| **Port** | 9222:9222 |

- No API keys required
- Used for web scraping/automation

---

### 8. **acfs-hub-db-1** (PostgreSQL)

| Property | Value |
|----------|-------|
| **Image** | `postgres:16-alpine` |
| **Status** | ✅ Running |
| **Port** | 5432 (internal) |

- Internal database for acfs-hub
- No external API keys

---

## 📁 File Locations Summary

```text
/home/gonya/
├── Documents/Unified_System/
│   └── Windows_AI_Core/
│       ├── .env                           # ← MAIN BOT CONFIG
│       │   ├── TELEGRAM_BOT_TOKEN
│       │   ├── GEMINI_API_KEY
│       │   ├── OPENAI_API_KEY
│       │   ├── SERPAPI_KEY
│       │   └── LINEAR_API_KEY
│       ├── src/
│       │   ├── bot_config.py              # ⚠️ Hardcoded BOT_TOKEN
│       │   ├── config_manager.py          # Loads .env via dotenv
│       │   ├── inference_client.py        # Uses API keys for LLM
│       │   ├── web_search.py              # Uses SERPAPI_KEY
│       │   └── gmail_client.py            # Uses OAuth credentials
│       └── config/
│           └── gmail_credentials.json     # OAuth client config
│
├── Scripts/homeassistant/
│   └── ha_client.py                       # ⚠️ Hardcoded HA_TOKEN
│
├── gcp-monitoring-key.json                # GCP service account
│
├── acfs-hub/
│   ├── docker-compose.yml                 # HTTP_BEARER_TOKEN
│   └── .env                               # AUTH_TOKEN=antigravity_secret
│
└── antigravity-mcp-server/
    └── .env                               # ⚠️ OPENROUTER_API_KEY (3x duplicate)
```

---

## 🔄 Key Loading Flow Diagram

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI-BOT KEY LOADING FLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  systemd starts ai-bot.service                                               │
│         │                                                                    │
│         ▼                                                                    │
│  EnvironmentFile=/home/gonya/.../Windows_AI_Core/.env                       │
│         │                                                                    │
│         ▼ (injects into process env)                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  os.environ now contains:                                              │   │
│  │    TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, OPENAI_API_KEY, etc.           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│         │                                                                    │
│         ▼                                                                    │
│  config_manager.py calls load_dotenv()                                       │
│         │                                                                    │
│         ▼                                                                    │
│  ConfigManager._load_config() reads:                                         │
│    self._config = {                                                          │
│        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY"),                  │
│        ...                                                                   │
│    }                                                                         │
│         │                                                                    │
│         ▼                                                                    │
│  InferenceClient(config) initialized                                         │
│         │                                                                    │
│         ▼                                                                    │
│  client.api_key returns key based on current provider                        │
│         │                                                                    │
│         ▼                                                                    │
│  API call with Authorization header or client SDK                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Issues & Recommendations

| Issue                       | Location              | Severity | Status      |
|-----------------------------|----------------------|----------|-------------|
| Telegram token hardcoded    | `bot_config.py:4`    | Medium   | ✅ FIXED    |
| HA token hardcoded          | `ha_client.py:17`    | Medium   | ✅ FIXED    |
| OpenRouter key 3x duplicate | `antigravity-mcp/.env` | Low    | ✅ FIXED    |
| Default provider was gemini | `.env`               | High     | ✅ FIXED    |
| ai-watchdog crashing        | `.env`               | Medium   | ✅ FIXED    |
| Gemini API enabled          | GCP                  | High     | ✅ DISABLED |
| Gmail OAuth incomplete      | `config/`            | Medium   | Pending     |
| ACFS token weak             | `acfs-hub/`          | Low      | Pending     |
| Linear key unused           | `.env`               | Info     | Pending     |

---

## 🔒 Security Notes

1. **Host environment is clean** - No global API keys exposed
2. **Keys properly scoped** - Each service has only what it needs
3. **Docker isolation** - Containers have separate credentials
4. **OAuth credentials** vs **tokens** - Gmail uses OAuth flow, not static keys
5. **Service account** - GCP uses short-lived tokens from JSON key
