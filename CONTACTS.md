# 📇 MCP Agent Contacts & Protocol

This document serves as the directory for all agents operating
within the Unified System Core.

## 🌐 MCP Mail Server Configuration

- **Base URL:** `http://localhost:8765/mcp` (Local) /
  `http://100.110.209.49:8765/mcp` (Network)
- **Project Key:** `home-gonya-unified-system` (Project Slug)
- **Auth Token:** `c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb`
  (Hardcoded Vibranium Token) or use `MCP_MAIL_TOKEN` env var.

## 👥 Registered Agents (The Roster)

| Agent Name | Role | Model | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **OrangeStone** | 🧠 Orchestrator | `gemini-2.0-flash` | 🟢 Online | Admin |
| **PinkLake** | ⚖️ Council | `gemini-2.0-flash` | 🟢 Online | Decision |
| **Arthur** | 👶 Apprentice | `gemini-pro` | 🔵 Restricted | ID: Artur |
| **VioletCastle** | 🧑‍💻 Kosta/Laptop | `claude-3-opus` | 🟢 Online | Dev |

## 🆔 Identity Binding

The system supports **Local Identity Mapping** to link Agents
to physical humans.

- **Source of Truth:** `/secrets/family_map.json` (.gitignored).
- **Purpose:** Context-aware permissions (e.g., Child Account).
- **Setup:** Run `Scripts/Templates/identity_setup_pattern.py`.

## 📨 Communication Protocol (How to Mail)

### 1. Check Inbox (Read)

**Tool:** `fetch_inbox`

```json
{
  "project_key": "home-gonya-unified-system",
  "agent_name": "YOUR_NAME"
}
```

### 2. Send Message (Write)

**Tool:** `send_message`

```json
{
  "project_key": "home-gonya-unified-system",
  "sender_name": "YOUR_NAME",
  "to": ["OrangeStone", "PinkLake"],
  "subject": "Mission Update",
  "body_md": "Report content here..."
}
```

### 3. Broadcast (To All)

Send to multiple recipients in `to` array.

---

#### Vibranium Era - 2026
