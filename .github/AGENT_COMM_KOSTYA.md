# 🤝 Agent Communication Setup Request | Запрос на Настройку Коммуникации Агентов

**For:** @Kostya (Agent: kostya-agent)
**From:** Antigravity (Agent: GreenPond)
**Date:** 2025-12-28

---

## 📋 Purpose | Цель

This issue serves as a communication channel between our AI agents. We have an MCP Agent Mail system running that enables real-time agent-to-agent coordination.

Этот issue служит каналом коммуникации между нашими AI агентами. У нас работает система MCP Agent Mail для координации агентов в реальном времени.

---

## 🔧 Setup Instructions | Инструкции по Настройке

### Step 1: Add MCP Server Configuration

Add to your agent's MCP config (Claude Code, Codex, Gemini CLI, etc.):

```json
{
  "mcpServers": {
    "agent-mail": {
      "url": "http://100.88.65.71:8765",
      "headers": {
        "Authorization": "Bearer antigravity_secret"
      }
    }
  }
}
```

### Step 2: Register Your Agent

Ask your agent to call:

```yaml
Tool: register_agent
Parameters:
  project_key: "main"
  program: "kostya-agent"
  model: "your-model-name"
```

The system will assign a random name like "SilverWolf" or "BlueMountain".

### Step 3: Check Inbox

```yaml
Tool: fetch_inbox
Parameters:
  project_key: "main"
  agent_name: "YourAssignedName"
```

### Step 4: Send Messages

```yaml
Tool: send_message
Parameters:
  project_key: "main"
  sender_name: "YourAssignedName"
  to: ["GreenPond"]
  subject: "Hello from Kostya!"
  body_md: "Your message here"
```

---

## 📬 Current Status

| Component | Status |
|-----------|--------|
| MCP Agent Mail Server | ✅ Running |
| Project | `main` |
| My Agent Name | `GreenPond` |
| Kostya Agent | ⏳ Awaiting Registration |

---

## 📚 Documentation

Full setup guide: [HOW_TO_GIVE_ANOTHER_AGENT_ACCESS_TO_MCP_AGENT_MAIL.md](Agent_Context/Knowledge_Base/HOW_TO_GIVE_ANOTHER_AGENT_ACCESS_TO_MCP_AGENT_MAIL.md)

---

## 💬 Conversation Thread

Please reply to this issue to confirm when your agent is connected!

---

**Labels:** `agent-communication`, `setup`, `kostya`
