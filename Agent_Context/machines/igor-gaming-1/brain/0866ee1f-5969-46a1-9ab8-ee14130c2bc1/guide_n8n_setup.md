# N8N & AI Integration Guide

Follow these steps to connect N8N to your new Antigravity MCP Server and configure OpenAI.

## 1. Fix N8N Docker Permissions

**Problem**: Your N8N container cannot see the host's Docker daemon.
**Solution**: Update your `docker-compose.yml` to mount the socket.

**Step 1.1**: Open `/home/gonya/docker-compose.yml` (or wherever you are runnign it from).
**Step 1.2**: Add the following line to the `volumes` section of the `n8n` service:

```yaml
    volumes:
      - /home/gonya/n8n/data:/home/node/.n8n
      - /var/run/docker.sock:/var/run/docker.sock:ro  # <--- ADD THIS LINE
      - /usr/bin/docker:/usr/bin/docker:ro              # <--- OPTIONAL: For CLI access
```

**Step 1.3**: Recreate the container:

```bash
docker-compose up -d --force-recreate n8n
```

Alternatively, if you are running it manually:

```bash
docker run -d --name n8n -p 5678:5678 -v /var/run/docker.sock:/var/run/docker.sock -v /home/gonya/n8n/data:/home/node/.n8n n8nio/n8n
```

## 2. Connect N8N to MCP Server (HTTP/SSE)

Since use configured the MCP server with an HTTP endpoint, N8N can talk to it easily.

**Start the MCP Server in SSE Mode**:
Run this in a terminal (use `screen` or `tmux` to keep it running):

```bash
./start_server.sh
```

*It should say: "Antigravity MCP Server (HTTP) running on port 3005"*

**N8N Workflow (Copy & Paste)**:
Copy the JSON below and paste it directly into your N8N canvas (Ctrl+V).

```json
{
  "nodes": [
    {
      "parameters": {
        "method": "POST",
        "url": "http://100.88.65.71:3005/message",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "x-mcp-api-key",
              "value": "antigravity-secret"
            }
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyParameters": {
          "parameters": [
            {
              "name": "jsonrpc",
              "value": "2.0"
            },
            {
              "name": "method",
              "value": "tools/call"
            },
            {
              "name": "params",
              "value": "={{ {\"name\": \"docker_list\", \"arguments\": {}} }}"
            },
            {
              "name": "id",
              "value": 1
            }
          ]
        },
        "options": {}
      },
      "id": "e5f8e0e0-1234-4321-abcd-567890abcdef",
      "name": "Call MCP Tool",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [
        460,
        300
      ]
    }
  ],
  "connections": {}
}
```

*Note: `100.88.65.71` is your verified host interface IP. If that fails, try `172.17.0.1` or `host.docker.internal`.*

## 3. OpenAI Configuration

To give N8N specific OpenAI powers, creating a credential is easiest.

**Steps**:

1. Go to **Credentials** -> **Add Credential**.
2. Search for **OpenAI API**.
3. **API Key**: `sk-...` (Your Key).
4. **Organization ID**: (Optional, leave blank).

**Quick Test Workflow (Copy & Paste)**:

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "gpt-4-turbo",
        "prompt": {
          "messages": [
            {
              "role": "user",
              "content": "Hello via MCP Orchestrator!"
            }
          ]
        }
      },
      "id": "a1b2c3d4-5678-9012-3456-7890abcdef12",
      "name": "OpenAI Chat",
      "type": "@n8n/n8n-nodes-langchain.chainOpenAi",
      "typeVersion": 1,
      "position": [
        680,
        300
      ],
      "credentials": {
        "openAiApi": {
          "id": "YOUR_CREDENTIAL_ID_HERE",
          "name": "OpenAI account"
        }
      }
    }
  ],
  "connections": {}
}
```

## 4. Ngrok (Windows)

If you need cloud agents to reach this:

1. On your **Windows** machine (assuming it can see the Linux machine).
2. Run: `ngrok http <LINUX_IP_ADDRESS>:3005`
3. The generated URL (e.g., `https://random.ngrok-free.app`) is your **MCP Server URL**.

## 5. Ready-to-Use JSON Payloads

Use these in your N8N `HTTP Request` node (Body -> JSON) to control the server.

### List Docker Containers

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "docker_list",
    "arguments": {}
  },
  "id": 1
}
```

### Check Ollama Health

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "ollama_check",
    "arguments": {}
  },
  "id": 2
}
```

### Restart Container

Replace `CONTAINER_ID` with the actual ID.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "docker_restart",
    "arguments": {
      "container_id": "CONTAINER_ID"
    }
  },
  "id": 3
}
```

## 6. Unified Topology (Mac + Linux/Windows)

To "sew" your Mac Agent and this Linux Node together using Tailscale IP `100.88.65.71`, use the following resources.

### A. Mac Agent Prompt (System Override)

Copy and paste this to your Agent on Mac:

```text
SYSTEM OVERRIDE: NETWORK TOPOLOGY UPDATE

Внимание. Ты больше не работаешь локально. Ты — Центр Управления распределенной системой.
Забудь про localhost для тяжелых задач.

ТВОЯ ЦЕЛЬ: Управлять удаленным узлом "GONYA-WSL".

ПАРАМЕТРЫ УДАЛЕННОГО УЗЛА (WINDOWS):
1.  **IP-адрес (Tailscale):** `100.88.65.71` (Это "Железобетонный" адрес. Испольуй ТОЛЬКО его).
2.  **MCP Server (Руки/Docker):** `http://100.88.65.71:3005/message`
3.  **OpenCode (Кодинг):** `http://100.88.65.71:4096`
4.  **Ollama (Мозги):** `http://100.88.65.71:11434`

ИНСТРУКЦИЯ ПО ИНТЕГРАЦИИ:
1. Когда я прошу "Проверить Докер" — ты генерируешь запрос на порт **3005** по IP **100.88.65.71**.
2. Когда я прошу "Написать код" — ты обращаешься к порту **4096** по IP **100.88.65.71**.
3. НЕ ПРЕДЛАГАЙ мне SSH-туннели. Сеть Tailscale уже работает. Используй прямой доступ.

Подтверди получение топологии.
```

### B. N8N Telegram Workflow (Unified Registry)

Use this workflow in N8N. It uses the Verified IP and connects Telegram triggers to the MCP Docker tool.

**NOTE**: I have corrected the tool name to `docker_list` (system actual name) instead of `check_docker`.

```json
{
  "nodes": [
    {
      "parameters": {
        "updates": [
          "message"
        ],
        "additionalFields": {}
      },
      "id": "telegram-trigger",
      "name": "Telegram Trigger",
      "type": "n8n-nodes-base.telegramTrigger",
      "typeVersion": 1.1,
      "position": [
        460,
        300
      ],
      "webhookId": "antigravity-unified",
      "credentials": {
        "telegramApi": {
          "id": "YOUR_TELEGRAM_CRED_ID",
          "name": "Telegram account"
        }
      }
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://100.88.65.71:3005/message",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "x-mcp-api-key",
              "value": "antigravity-secret"
            }
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyParameters": {
          "parameters": [
            {
              "name": "jsonrpc",
              "value": "2.0"
            },
            {
              "name": "method",
              "value": "tools/call"
            },
            {
              "name": "params",
              "value": "={{ {\"name\": \"docker_list\", \"arguments\": {}} }}"
            },
            {
              "name": "id",
              "value": 1
            }
          ]
        },
        "options": {}
      },
      "id": "check-windows-tailscale",
      "name": "🔌 Connect to Windows (Tailscale)",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [
        700,
        300
      ]
    },
    {
      "parameters": {
        "chatId": "={{ $json.message.chat.id }}",
        "text": "={{ '🔗 **Связь установлена!**\\nАдрес: 100.88.65.71\\n\\n📊 **Docker Status:**\\n' + JSON.stringify($json.result.content[0].text).slice(0, 500) }}",
        "additionalFields": {
          "parse_mode": "Markdown"
        }
      },
      "id": "telegram-reply",
      "name": "Reply to User",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.1,
      "position": [
        920,
        300
      ],
      "credentials": {
        "telegramApi": {
          "id": "YOUR_TELEGRAM_CRED_ID",
          "name": "Telegram account"
        }
      }
    }
  ],
  "connections": {
    "Telegram Trigger": {
      "main": [
        [
          {
            "node": "🔌 Connect to Windows (Tailscale)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "🔌 Connect to Windows (Tailscale)": {
      "main": [
        [
          {
            "node": "Reply to User",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```
