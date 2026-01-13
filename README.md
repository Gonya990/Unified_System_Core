# 🌌 Unified System Core

> **Distributed AI Cluster** — Мозги, Руки и Сердце в одной системе.

---

## 🚀 Quick Navigation

| 📂 Section | 🔗 Link | 📝 Description |
| --- | --- | --- |
| **🧠 Knowledge Base** | [Agent_Context/Knowledge_Base/](Agent_Context/Knowledge_Base/) | Centralized AI context, sessions, and scripts |
| **💻 AI Core (Main)** | [Projects/AI_Core/](Projects/AI_Core/) | Gonya Telegram Bot — personal AI assistant with smart home, calendar, tasks & multi-model chat |
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

| Node | MagicDNS | IP (TS) | Role |
| --- | --- | --- | --- |
| **igor-gaming-1** | `igor-1...` | `100.78...` | Primary AI Workstation |
| **igor-gaming** | `igor...` | `100.127...` | AI Core / GPU |
| **MacBook-Air** | `mac...` | `100.93...` | Admin & Dev |
| **pve** | `pve...` | `100.74.137.122` | Hypervisor |
| **iphone-15** | `iph...` | `100.86...` | Mobile |

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

## 🌍 Communication & Translation

All agents operating in this system follow the **English Translation Protocol**:
- Final output is always in **English**.
- The tag **[russian]** is added if the original context was Russian.
- Original Russian text is **removed** to maintain clarity.

---

*Powered by Antigravity Agent* 🚀
