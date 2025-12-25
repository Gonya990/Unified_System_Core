# 💍 Multi-Agent Orchestration: Antigravity & Kostya-Agent

## 💍 Мульти-агентная оркестрация: Antigravity и Kostya-Agent

> **Concept:** Federated Swarm Coordination for Unified System.  
> **Концепция:** Федеративное взаимодействие роя в рамках Unified System.

---

## 1. 🌐 Network & Communication / Сеть и протоколы

- **Private Mesh:** Both agents communicate via **Tailscale**.
  - Antigravity IP: `100.93.121.47`
  - Kostya-Agent IP: [To be confirmed]
- **Protocol:** **MCP Agent Mail** (HTTP/SSE via Private Mesh).
  - Port: `8765`
  - Endpoint: `/mcp/`
  - Features: Multi-agent inbox, file leases, searchable threads.
- **Private Mesh:** Оба агента общаются через **Tailscale**.
  - IP Antigravity: `100.93.121.47`
  - Kostya-Agent IP: [Уточняется]
- **Протокол:** **MCP Agent Mail** (HTTP/SSE через Private Mesh).
  - Порт: `8765`
  - Эндпоинт: `/mcp/`
  - Функции: Инбоксы для агентов, аренда файлов (leases), поиск по веткам обсуждений.

---

## 2. 🛡️ Privacy & Data Protection / Приватность и защита данных

- **Context Isolation:** Agents **cannot** read each other's `.env` or password files.
- **Filtering Layer:** A pre-processor that replaces personal strings with placeholders (e.g., `Goncharenko` -> `[USER_ADMIN_1]`) before sending context to the other agent.
- **Shared Docs:** Only files in `Agent_Context/Knowledge_Base/Shared/` are indexed by both agents.
- **Изоляция контекста:** Агенты **не могут** читать `.env` или файлы паролей друг друга.
- **Слой фильтрации:** Препроцессор, который заменяет личные данные на заглушки (например, `Goncharenko` -> `[USER_ADMIN_1]`) перед отправкой контекста другому агенту.
- **Общие документы:** Только файлы в `Agent_Context/Knowledge_Base/Shared/` индексируются обоими агентами.

---

## 3. 🤝 Collaborative Logic / Логика взаимодействия

- **Inter-Agent Communication (ACP/MCP):**
  - Standard: **Agent Communication Protocol (ACP)** principles for messaging.
  - Implementation: **MCP Agent Mail** (HTTP/SSE via Private Mesh).
  - Features: Multi-agent inbox, file leases, searchable threads.
- **Unified Task Board:** **Beads (.beads/)**.
  - Tooling: `bd` (CLI) and `bv` (TUI/Robot).
  - Workflow: Agents track dependencies and pick tasks.
- **Sync Mechanism:** One agent acts as "Primary", another as "Verifier" using **Agent Mail threads**.
- **Меж-агентное общение (ACP/MCP):**
  - Стандарт: Принципы **Agent Communication Protocol (ACP)** для обмена сообщениями.
  - Реализация: **MCP Agent Mail** (HTTP/SSE через Private Mesh).
  - Функции: Инбоксы для агентов, аренда файлов (leases), поиск по веткам обсуждений.
- **Общая доска задач:** **Beads (.beads/)**.
  - Инструменты: `bd` (CLI) и `bv` (TUI/Robot).
  - Рабочий процесс: Агенты отслеживают зависимости и выбирают задачи.
- **Синхронизация:** Один агент выступает как «Основной», другой — как «Проверяющий», используя **ветки обсуждений в Agent Mail**.

---

## 4. 🚀 Centralized Coordination / Централизованная координация

- **Single Hub Hosting:** All core agent messaging (`mcp_agent_mail`) and shared task status (`beads`) MUST be hosted on the **Service Node** (`100.88.65.71`) to act as the single source of truth.
- **Unified Messaging:**
  - Antigravity and Kostya-Agent use the same server to send and receive messages.
  - Asynchronous coordination ensures tasks are never lost even if one agent node is offline.
- **Централизованный хаб:** Весь основной обмен сообщениями (`mcp_agent_mail`) и общий статус задач (`beads`) ДОЛЖНЫ быть размещены на **Service Node** (`100.88.65.71`), который выступает единым источником истины.
- **Единая система сообщений:**
  - Antigravity и Kostya-Agent используют один и тот же сервер для отправки и получения сообщений.
  - Асинхронная координация гарантирует, что задачи никогда не будут потеряны, даже если один из узлов агента находится в автономном режиме.

---

## 5. ⏭️ Immediate Next Steps / Следующие шаги

1. Define the shared IP for Kostya's agent. (Определить общий IP агента Кости).
2. Create the `Shared/` directory in the Knowledge Base. (Создать директорию `Shared/` в базе знаний).
3. Implement a basic health-check script that "pings" the other agent's status. (Написать скрипт проверки связи, который «пингует» статус другого агента).
