# 📇 MCP Agent Contacts & Protocol

This document serves as the directory for all agents operating within the Unified System Core.

## 🌐 MCP Mail Server Configuration

- **Base URL:** `http://localhost:8765/mcp` (Local) / `http://100.110.209.49:8765/mcp` (Network)
- **Project Key:** `/home/gonya/Unified_System` (Absolute Path on Server)
- **Auth Token:** `c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb` (Hardcoded Vibranium Token) or use `MCP_MAIL_TOKEN` env var.

## 👥 Registered Agents (The Roster)

| Agent Name | Role | Model | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **OrangeStone** | 🧠 Orchestrator | `gemini-2.0-flash-exp` | 🟢 Online | System Admin, CI/CD, Factory Control |
| **PinkLake** | ⚖️ Council | `gemini-2.0-flash-exp` | 🟢 Online | High-level decision making |
| **FuchsiaCat** | 🐱 Kosta (Home) | `claude-3-opus` | 🟢 Online | Same human as VioletCastle |
| **Arthur** | 👶 Apprentice | `gemini-pro` | 🔵 Restricted | Identity: `Artur Goncharenko` (Family Link) |
| **VioletCastle** | 🧑‍💻 Kosta (Laptop) | `claude-code (opus-4.5)` | 🟢 Online | Dev, Code Review, Coordination |

## 🆔 Identity Binding (New)

The system now supports **Local Identity Mapping** to link Agents to physical humans (Family/Team).

- **Source of Truth:** `/secrets/family_map.json` (Local only, .gitignored).
- **Purpose:** Context-aware permissions (e.g., "Child Account" restrictions for Arthur).
- **Setup:** Run `Scripts/Templates/identity_setup_pattern.py` to generate your local map.

## 📨 Communication Protocol (How to Mail)

### 1. Check Inbox (Read)

**Tool:** `fetch_inbox`

```json
{
  "project_key": "/home/gonya/Unified_System",
  "agent_name": "YOUR_NAME"
}
```

### 2. Send Message (Write)

**Tool:** `send_message`

```json
{
  "project_key": "/home/gonya/Unified_System",
  "sender_name": "YOUR_NAME",
  "to": ["OrangeStone", "PinkLake"],
  "subject": "Mission Update",
  "body_md": "Report content here..."
}
```

### 3. Broadcast (To All)

Send to multiple recipients in `to` array.

---
*Last Updated: 2026-01-10 (Vibranium Era)*
