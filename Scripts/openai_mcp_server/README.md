# OpenAI MCP Server | MCP Сервер OpenAI

**English:** MCP server to connect Antigravity/Gemini with OpenAI's API
for seamless ChatGPT integration.

**Russian:** MCP сервер для подключения Antigravity/Gemini к API OpenAI
для бесшовной интеграции с ChatGPT.

## What This Does | Что это делает

Instead of manually exporting ChatGPT data, this MCP server provides:

- ✅ Direct API access to your OpenAI account
- ✅ Real-time conversation retrieval
- ✅ Profile and preferences access
- ✅ Two-way communication between Antigravity and ChatGPT
- ✅ Shared context and memory

Вместо ручного экспорта данных ChatGPT, этот MCP сервер предоставляет:

- ✅ Прямой API доступ к вашей учетной записи OpenAI
- ✅ Получение разговоров в реальном времени
- ✅ Доступ к профилю и настройкам
- ✅ Двустороннюю связь между Antigravity и ChatGPT
- ✅ Общий контекст и память

## Architecture | Архитектура

```text
┌─────────────────┐         MCP Protocol         ┌──────────────────┐
│                 │◄───────────────────────────────│                  │
│  Antigravity    │                                │  OpenAI MCP      │
│  (Gemini)       │         HTTP/JSON              │  Server          │
│                 │───────────────────────────────►│                  │
└─────────────────┘                                └────────┬─────────┘
                                                            │
                                                            │ OpenAI API
                                                            │
                                                   ┌────────▼─────────┐
                                                   │                  │
                                                   │  OpenAI          │
                                                   │  ChatGPT         │
                                                   │                  │
                                                   └──────────────────┘
```

## Features | Возможности

### 1. Conversation Access | Доступ к разговорам

- List all conversations
- Retrieve specific conversations
- Search conversation history
- Real-time sync

### 2. Message Exchange | Обмен сообщениями  

- Send messages to ChatGPT
- Receive responses
- Maintain conversation context
- Multi-turn dialogues

### 3. Custom Instructions | Пользовательские инструкции

- Retrieve your ChatGPT custom instructions
- Apply them to Antigravity
- Sync preferences bi-directionally

### 4. Shared Memory | Общая память

- Share knowledge between both AI systems
- Cross-reference conversations
- Unified context awareness

## Installation | Установка

### Prerequisites | Требования

```bash
# Python 3.8+
python3 --version

# UV (for dependency management)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup | Настройка

```bash
cd /Users/macbook/Documents/Unified_System/Scripts/openai_mcp_server

# Install dependencies
uv pip install fastmcp openai python-dotenv

# Configure OpenAI API key
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Start Server | Запуск сервера

```bash
# Start the MCP server
python server.py

# Or use systemd (for persistent service)
sudo systemctl enable openai-mcp
sudo systemctl start openai-mcp
```

## Configuration | Конфигурация

### 1. OpenAI API Key | API ключ OpenAI

Get your API key from: <https://platform.openai.com/api-keys>

```bash
# .env file
OPENAI_API_KEY=sk-proj-...your-key-here...
```

### 2. MCP Server Config | Конфигурация MCP сервера

Edit `config.json`:

```json
{
  "server": {
    "host": "127.0.0.1",
    "port": 8766,
    "protocol": "http"
  },
  "openai": {
    "model": "gpt-4",
    "max_tokens": 4000,
    "temperature": 0.7
  },
  "features": {
    "conversation_sync": true,
    "custom_instructions": true,
    "shared_memory": true
  }
}
```

### 3. Gemini MCP Client | Клиент MCP для Gemini

Add to `/Users/macbook/Documents/Unified_System/External_Tools/Stack/mcp_agent_mail/gemini.mcp.json`:

```json
{
  "mcpServers": {
    "mcp-agent-mail": {
      "type": "http",
      "url": "http://127.0.0.1:8765/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_AGENT_HUB_TOKEN"
      }
    },
    "openai-gateway": {
      "type": "http",
      "url": "http://127.0.0.1:8766/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN_HERE"
      }
    }
  }
}
```

## Usage | Использование

### From Antigravity | Из Antigravity

Once configured, you can use these MCP tools:

```python
# List conversations
conversations = mcp.openai.list_conversations(limit=20)

# Get specific conversation
conv = mcp.openai.get_conversation(conversation_id="...")

# Send message to ChatGPT
response = mcp.openai.send_message(
    conversation_id="new",
    message="Explain quantum computing"
)

# Get custom instructions
instructions = mcp.openai.get_custom_instructions()

# Sync preferences
mcp.openai.sync_preferences_to_antigravity()
```

### Benefits Over Manual Export | Преимущества перед ручным экспортом

| Feature             | Manual Export | MCP Integration |
| ------------------- | ------------- | --------------- |
| Real-time access    | ❌ No         | ✅ Yes          |
| Bi-directional sync | ❌ No         | ✅ Yes          |
| Auto-updates        | ❌ No         | ✅ Yes          |
| Shared context      | ❌ No         | ✅ Yes          |
| API limits          | N/A           | Check quotas    |

## Security | Безопасность

- ✅ API key stored in .env (gitignored)
- ✅ MCP authentication tokens
- ✅ Local-only communication (127.0.0.1)
- ✅ No external data sharing
- ✅ Encrypted connections option

## Troubleshooting | Устранение неполадок

### API Key Invalid | Неверный API ключ

```bash
# Verify your API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Server Won't Start | Сервер не запускается

```bash
# Check port availability
lsof -i :8766

# Check logs
tail -f logs/openai-mcp.log
```

### Rate Limits | Ограничения скорости

OpenAI API has rate limits. Configure in `config.json`:

```json
{
  "rate_limiting": {
    "requests_per_minute": 60,
    "tokens_per_minute": 90000
  }
}
```

## Next Steps | Следующие шаги

1. **Set up OpenAI API account** | **Настройте учетную запись OpenAI API**
2. **Get API key** | **Получите API ключ**
3. **Configure server** | **Настройте сервер**
4. **Start MCP server** | **Запустите MCP сервер**
5. **Test connection** | **Проверьте подключение**
6. **Enjoy seamless integration!** | **Наслаждайтесь бесшовной интеграцией!**

---

**Status:** Ready for implementation | Готов к реализации  
**Priority:** High (better than manual export)
**Complexity:** Medium | Средний  
**Time:** 1-2 hours setup | 1-2 часа на настройку
