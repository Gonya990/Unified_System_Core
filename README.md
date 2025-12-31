# 🌌 Unified System Core

> **Distributed AI Cluster** — Мозги, Руки и Сердце в одной системе.

---

## 🚀 Quick Navigation

| 📂 Section | 🔗 Link | 📝 Description |
| --- | --- | --- |
| **🧠 Knowledge Base** | [Agent_Context/Knowledge_Base/](Agent_Context/Knowledge_Base/) | Centralized AI context, sessions, and scripts |
| **💻 AI Core (Main)** | [Projects/AI_Core/](Projects/AI_Core/) | Telegram Bot + Ollama inference code |
| **⚙️ Scripts** | [Scripts/](Scripts/) | Deployment, automation, expect scripts |
| **🏗 Architecture** | [Architecture Docs](Agent_Context/Knowledge_Base/Architecture/) | System design and handoff guides |

---

## 🖥️ System Nodes

```mermaid
graph LR
    subgraph Tailscale Mesh
        A[📱 iPhone Commander] --> B[💻 MacBook Admin]
        B --> C[🖥️ AI Core (Main)]
        B --> D[🐧 igor-gaming-1 WSL2]
        B --> E[📦 Proxmox PVE]
    end
    C --> F[🧠 Ollama GPU]
    D --> G[🏠 Home Assistant]
```

| Node | FQDN (MagicDNS) | IP (Tailscale) | Role |
| --- | --- | --- | --- |
| **igor-gaming-1** | `igor-gaming-1.tail5e8a72.ts.net` | `100.78.144.50` | Primary AI workstation (WSL2) |
| **igor-gaming** | `igor-gaming.tail5e8a72.ts.net` | `100.127.194.111` | Projects/AI_Core (GPU inference) |
| **MacBook-Air** | `macbook-air.tail5e8a72.ts.net` | `100.93.121.47` | Admin & development |
| **pve** | `pve.myth-rudd.ts.net` | `100.78.145.67` | Proxmox hypervisor |
| **iphone-15-pro** | `iphone-15-pro.tail5e8a72.ts.net` | `100.86.233.87` | Mobile commander (Termius) |

---

## 📁 Repository Structure

```text
├── Projects/
│   ├── AI_Core/                 # Telegram bot source
│   └── telegram_bot/            # Documentation & plans
├── Scripts/                     # Deployment & automation
└── README.md                    # ← You are here
```

---

## 🔗 Deep Dive Links

### For Agents 🤖

- **Full Context Handoff**: [CONTEXT_HANDOFF.md](Agent_Context/Knowledge_Base/Architecture/CONTEXT_HANDOFF.md)
- **MCP Server Setup**: [guide_n8n_setup.md](Agent_Context/Knowledge_Base/Sessions/0866ee1f-5969-46a1-9ab8-ee14130c2bc1/guide_n8n_setup.md)
- **System Inventory**: [system_inventory.md](Agent_Context/Knowledge_Base/Sessions/a1c2070a-d35e-41bb-8398-427c4934e58f/system_inventory.md)

### For Humans 👤

- **Quick Start Architecture**: [SYSTEM_ARCHITECTURE.md](Agent_Context/Knowledge_Base/Architecture/SYSTEM_ARCHITECTURE.md)
- **Multi-Machine Handoff**: [HANDOFF_GUIDE.md](Agent_Context/Knowledge_Base/Architecture/HANDOFF_GUIDE.md)
- **Project Registry**: [PROJECTS.yaml](Agent_Context/Knowledge_Base/Docs/PROJECTS.yaml)

---

## 🛠️ Quick Commands

```bash
# Clone & navigate
git clone https://github.com/Gonya990/Unified_System_Core.git
cd Unified_System_Core

# Check system status (from any node)
tailscale status

# SSH to main workstation
ssh gonya@igor-gaming-1

# Start MCP server
cd Agent_Context/Knowledge_Base/mcp-server && npm start
```

---

## 📊 Stats

- **Machines**: 5 nodes connected via Tailscale
- **AI Bot Features**: 25+ capabilities
- **Integrations**: 10+ (Telegram, HA, Linear, Calendar, HomeKit, Alice, etc.)
- **Lines of Code**: ~5,000+
- **Last Major Update**: 2025-12-27 (v2.0.0 - MEGA UPDATE)

---

## ✨ Latest Features (v2.0.0)

🎉 **7 Major Features Added in One Session:**

- 🔔 Notification Manager (smart quiet hours)
- 📊 Dashboard v2 (web UI with charts)
- 💰 Cost Tracking Pro (detailed analytics)
- 📋 Linear API (professional tasks)
- 🌅 Daily Digest (morning summary)
- 📅 Google Calendar integration
- 🏠 HomeKit Bridge (Apple Home)

See [CHANGELOG.md](CHANGELOG.md) for full details.

---

## 🤖 AI Bot Capabilities

The Unified AI Bot is now a **complete life management system**:

- 💬 Multi-model chat (Gemini, OpenAI, Ollama)
- 🎨 Image generation (DALL-E 3)
- 👁 Photo analysis (Gemini Vision)
- 🎤 Voice transcription (Whisper)
- 🏠 Smart home control (HA + HomeKit)
- 📅 Calendar management (Google)
- 📋 Task tracking (Linear + local)
- 🔍 Web search (Google via SerpApi)
- 🌅 Daily digest (automated)
- 📦 Auto-backup (daily at 03:00)
- 🔄 Self-update capability
- 🗣 Voice control (Yandex Alice)

**Quick Start**: See [Projects/AI_Core/README.md](Projects/AI_Core/README.md)

---

*Powered by Antigravity Agent* 🚀
