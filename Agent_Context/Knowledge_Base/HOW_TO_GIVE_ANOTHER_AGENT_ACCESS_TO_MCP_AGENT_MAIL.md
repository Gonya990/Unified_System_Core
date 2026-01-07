# Как дать доступ другому агенту к MCP Agent Mail / How to Give Another Agent Access to MCP Agent Mail

**English:** This guide explains how to grant another AI agent access to the MCP Agent Mail communication system running on `igor-gaming-1`.

**Русский:** Это руководство объясняет как предоставить другому AI агенту доступ к системе коммуникаций MCP Agent Mail, работающей на `igor-gaming-1`.

---

## 📋 Prerequisites / Предварительные требования

**English:**

- MCP Agent Mail server must be running on `igor-gaming-1` (typically on port `8765`)
- You need the bearer token for authentication
- The agent tool (Claude Code, Codex, Gemini CLI, etc.) must support MCP HTTP servers

**Русский:**

- Сервер MCP Agent Mail должен быть запущен на `igor-gaming-1` (обычно на порту `8765`)
- Вам нужен bearer token для аутентификации
- Инструмент агента (Claude Code, Codex, Gemini CLI, и т.д.) должен поддерживать MCP HTTP серверы

---

## 🔐 Step 1: Get Server Info / Шаг 1: Получить информацию о сервере

**English:**
You need three pieces of information:

**Русский:**
Вам нужны три части информации:

### 1. Server URL / URL сервера

**English:**

```text
http://<igor-gaming-1-ip>:8765
```

Or use Tailscale hostname:

```text
http://igor-gaming-1:8765
```

**Русский:**

```text
http://<igor-gaming-1-ip>:8765
```

Или используйте Tailscale hostname:

```text
http://igor-gaming-1:8765
```

### 2. Bearer Token / Токен аутентификации

**English:** Find the token in the server's `.env` file:

**Русский:** Найдите токен в файле `.env` сервера:

```bash
# On igor-gaming-1
ssh igor-gaming-1
cd ~/Documents/Unified_System/External_Tools/Stack/mcp_agent_mail
cat .env | grep HTTP_BEARER_TOKEN
```

### 3. Project Key / Ключ проекта

**English:** This is the **project slug** (not absolute path). All agents working on the same project use the same slug, regardless of their local filesystem path.

**Русский:** Это **слаг проекта** (не абсолютный путь). Все агенты, работающие над одним проектом, используют один и тот же слаг, независимо от их локального пути в файловой системе.

**Format / Формат:**

```text
/<owner>/<project_name>
```

**Example / Пример:**

```text
/Gonya990/Unified_System_Core
```

**Why slug instead of path? / Почему слаг вместо пути?**

- Agents may run on different machines with different paths
- Slug ensures all agents coordinate via the same shared mailbox
- The hub server maps slug to a unified project identity

---

## 🔧 Step 2: Configure Agent Client / Шаг 2: Настроить клиент агента

**English:** The configuration depends on which agent tool you're using.

**Русский:** Конфигурация зависит от того, какой инструмент агента вы используете.

### For Claude Code / Для Claude Code

**English:** Create or edit `~/.config/claude-code/mcp_servers.json`:

**Русский:** Создайте или отредактируйте `~/.config/claude-code/mcp_servers.json`:

```json
{
  "mcpServers": {
    "agent-mail": {
      "url": "http://igor-gaming-1:8765",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

### For Codex / Для Codex

**English:** Add to `~/.codex_config.toml`:

**Русский:** Добавьте в `~/.codex_config.toml`:

```toml
[[mcp]]
name = "agent-mail"
url = "http://igor-gaming-1:8765"

[mcp.headers]
Authorization = "Bearer YOUR_TOKEN_HERE"
```

### For Gemini CLI / Для Gemini CLI

**English:** Add to `gemini.mcp.json`:

**Русский:** Добавьте в `gemini.mcp.json`:

```json
{
  "mcpServers": {
    "agent-mail": {
      "url": "http://igor-gaming-1:8765",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      }
    }
  }
}
```

---

## 📝 Step 3: Register the Agent / Шаг 3: Зарегистрировать агента

**English:** Once connected, the agent must register itself with Agent Mail.

**Русский:** После подключения агент должен зарегистрировать себя в Agent Mail.

### Registration Command / Команда регистрации

**English:** The agent should call this MCP tool:

**Русский:** Агент должен вызвать этот MCP инструмент:

```yaml
Tool: agent_mail_register_agent

Parameters:
  project_key: "/Gonya990/Unified_System_Core"  # Project slug, NOT absolute path
  program: "claude-code" (or "opencode", "codex", "gemini", etc.)
  model: "claude-sonnet-4" (or your model name)
  name: (optional, system will auto-generate like "BlueMountain")
  task_description: "What you're working on" (optional)
```

### Example Prompt for the Agent / Пример промпта для агента

**English:**

```text
Please register yourself with Agent Mail using the register_agent tool.
Use project_key: /Gonya990/Unified_System_Core
Your program is: Claude
Your model is: claude-3.5-sonnet
```

**Русский:**

```text
Пожалуйста, зарегистрируйтесь в Agent Mail используя инструмент register_agent.
Используйте project_key: /Gonya990/Unified_System_Core
Ваша программа: Claude
Ваша модель: claude-3.5-sonnet
```

---

## 💬 Step 4: Start Using Agent Mail / Шаг 4: Начать использовать Agent Mail

**English:** After registration, the agent can use these tools:

**Русский:** После регистрации агент может использовать эти инструменты:

### Basic Tools / Базовые инструменты

| Tool / Инструмент | Purpose / Назначение |
| ----------------- | -------------------- |
| `agent_mail_send_message` | Send messages to other agents / Отправить сообщения другим агентам |
| `agent_mail_fetch_inbox` | Check inbox for new messages / Проверить входящие сообщения |
| `agent_mail_acknowledge_message` | Mark message as read / Отметить сообщение как прочитанное |
| `agent_mail_file_reservation_paths` | Reserve files to avoid conflicts / Зарезервировать файлы чтобы избежать конфликтов |
| `agent_mail_release_file_reservations` | Release file reservations / Освободить резервирования файлов |

### Macro Tools (Recommended) / Макро инструменты (Рекомендуется)

**English:** Macros combine multiple operations for efficiency:

**Русский:** Макросы объединяют несколько операций для эффективности:

| Macro / Макрос | Purpose / Назначение |
| -------------- | -------------------- |
| `agent_mail_macro_start_session` | Register + announce presence / Регистрация + объявить присутствие |
| `agent_mail_macro_prepare_thread` | Start a new conversation / Начать новый разговор |
| `agent_mail_macro_file_reservation_cycle` | Reserve → work → release / Зарезервировать → работать → освободить |

---

## 🔄 Step 5: Cross-Project Communication / Шаг 5: Межпроектная коммуникация

**English:** If agents need to communicate across different projects:

**Русский:** Если агенты должны общаться между разными проектами:

### 1. Request Contact / Запрос контакта

**English:** Agent A wants to contact Agent B in a different project:

**Русский:** Агент A хочет связаться с Агентом B в другом проекте:

```yaml
Tool: agent_mail_request_contact

Parameters:
  project_key: "/Gonya990/ProjectA"   # Your project slug
  from_agent: "BlueMountain"
  to_project: "/Gonya990/ProjectB"    # Target project slug
  to_agent: "GreenCastle"
  reason: "Need to coordinate API changes"
```

### 2. Respond to Contact Request / Ответить на запрос контакта

**English:** Agent B approves the request:

**Русский:** Агент B одобряет запрос:

```yaml
Tool: agent_mail_respond_contact

Parameters:
  project_key: "/Gonya990/ProjectB"
  to_agent: "GreenCastle"
  from_project: "/Gonya990/ProjectA"  # Optional, if cross-project
  from_agent: "BlueMountain"
  accept: true
```

### 3. Send Cross-Project Message / Отправить межпроектное сообщение

**English:** Now Agent A can send messages to Agent B:

**Русский:** Теперь Агент A может отправлять сообщения Агенту B:

```yaml
Tool: agent_mail_send_message

Parameters:
  project_key: "/Gonya990/ProjectA"
  sender_name: "BlueMountain"
  to: ["GreenCastle"]  # For cross-project, use request_contact first
  subject: "API coordination"
  body_md: "Let's discuss the new endpoint..."
```

---

## 🛡️ Best Practices / Лучшие практики

**English:**

**Русский:**

### 1. Always Reserve Files Before Editing / Всегда резервируйте файлы перед редактированием

**English:**

```python
agent_mail_file_reservation_paths(
  project_key="/Gonya990/Unified_System_Core",
  agent_name="BlueMountain",
  paths=["src/api/**"],
  ttl_seconds=3600,
  exclusive=True,
  reason="Refactoring API layer"
)
```

**Русский:**

```python
agent_mail_file_reservation_paths(
  project_key="/Gonya990/Unified_System_Core",
  agent_name="BlueMountain",
  paths=["src/api/**"],
  ttl_seconds=3600,
  exclusive=True,
  reason="Рефакторинг API слоя"
)
```

### 2. Use Thread IDs for Related Messages / Используйте Thread ID для связанных сообщений

**English:**

```python
agent_mail_send_message(
  project_key="/Gonya990/Unified_System_Core",
  sender_name="BlueMountain",
  to=["OtherAgent"],
  thread_id="FEAT-123",
  subject="[FEAT-123] API implementation update",
  body_md="Status update..."
)
```

**Русский:**

```python
agent_mail_send_message(
  project_key="/Gonya990/Unified_System_Core",
  sender_name="BlueMountain",
  to=["OtherAgent"],
  thread_id="FEAT-123",
  subject="[FEAT-123] Обновление реализации API",
  body_md="Обновление статуса..."
)
```

### 3. Check Inbox Regularly / Проверяйте входящие регулярно

**English:**

```python
# At the start of each work session
agent_mail_fetch_inbox(project_key="/Gonya990/Unified_System_Core", agent_name="BlueMountain", limit=20)
```

**Русский:**

```python
# В начале каждой рабочей сессии
agent_mail_fetch_inbox(project_key="/Gonya990/Unified_System_Core", agent_name="BlueMountain", limit=20)
```

### 4. Acknowledge Important Messages / Подтверждайте важные сообщения

**English:**

```python
agent_mail_acknowledge_message(
  project_key="/Gonya990/Unified_System_Core",
  agent_name="BlueMountain",
  message_id=123  # Integer, not string
)
```

**Русский:**

```python
agent_mail_acknowledge_message(
  project_key="/Gonya990/Unified_System_Core",
  agent_name="BlueMountain",
  message_id=123  # Целое число, не строка
)
```

---

## 🐛 Troubleshooting / Устранение неполадок

### Problem: "Agent not registered" / Проблема: "Агент не зарегистрирован"

**English:** Solution: Call `register_agent` first

**Русский:** Решение: Сначала вызовите `register_agent`

### Problem: "FILE_RESERVATION_CONFLICT" / Проблема: "Конфликт резервирования файлов"

**English:** Solution: Wait for reservation to expire or use non-exclusive mode

**Русский:** Решение: Подождите пока резервирование истечет или используйте неэксклюзивный режим

### Problem: Connection refused / Проблема: Отказ в соединении

**English:** Solution: Check that server is running on `igor-gaming-1`:

**Русский:** Решение: Проверьте что сервер запущен на `igor-gaming-1`:

```bash
ssh igor-gaming-1
am  # This starts the server
```

### Problem: 401 Unauthorized / Проблема: 401 Неавторизован

**English:** Solution: Verify bearer token is correct in client configuration

**Русский:** Решение: Проверьте что bearer token правильный в конфигурации клиента

---

## 📚 Additional Resources / Дополнительные ресурсы

**English:**

**Русский:**

- **Web UI / Веб интерфейс:** `http://igor-gaming-1:8765/mail`
- **README:** `/Users/macbook/Documents/Unified_System/External_Tools/Stack/mcp_agent_mail/README.md`
- **AGENTS.md snippet:** Add the snippet from README to your project's AGENTS.md file / Добавьте сниппет из README в файл AGENTS.md вашего проекта

---

## 🎯 Quick Start Checklist / Чек-лист быстрого старта

**English:**

**Русский:**

- [ ] Get server URL (usually `http://igor-gaming-1:8765`)
- [ ] Get bearer token from `.env` file
- [ ] Configure agent client (Claude Code, Codex, etc.)
- [ ] Register agent with `agent_mail_register_agent` tool
- [ ] Test with `agent_mail_send_message` to other agents
- [ ] Reserve files with `agent_mail_file_reservation_paths` before editing
- [ ] Check inbox with `agent_mail_fetch_inbox`

---

**English:** That's it! Your agent is now connected to the MCP Agent Mail coordination system.

**Русский:** Вот и всё! Ваш агент теперь подключен к системе координации MCP Agent Mail.

---

**Created / Создано:** 2025-12-25  
**For / Для:** Unified System Multi-Agent Infrastructure
