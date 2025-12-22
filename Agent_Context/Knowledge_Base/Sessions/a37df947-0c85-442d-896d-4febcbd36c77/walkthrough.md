# Руководство по настройке n8n

Мы успешно установили и запустили n8n локально.

## Доступ к n8n

# Проект "Антигравити": Walkthrough

Мы строим Единый Мульти-модельный AI Хаб.
**Текущий статус:** Переход от простых тестов к архитектуре "Все-в-одном".

## 1. Активированные "Мозги" (Brains)

### Google Vertex AI (Knowledge Base) 🟢

Инфраструктура развернута через Terraform.

- **Bucket Docs:** `knowledge-base-docs-gen-lang-client-0982257437` (Сюда кидать PDF/Docs)
- **Bucket Webhook:** `knowledge-base-bucket-gen-lang-client-0982257437`
- **Vertex AI Index:** `projects/gen-lang-client-0982257437/...` (Векторный поиск готов)

### Gemini CLI 🟢

Работает в терминале как "быстрый советник".

## 2. Активированные "Руки" (Hands)

### n8n (Conductor) 🟢

Запущен на Windows Server (доступен через Tailscale).

- **Следующий шаг:** Настроить Docker и GPU управление.

## 3. Инструкция для Windows Server

Чтобы превратить ваш Windows n8n в полноценный командный центр:

1. **Скачайте этот конфиг:** [server_config.env](file:///Users/macbook/.gemini/antigravity/playground/solar-curie/server_config.env)
2. Перенесите его на вашу Windows машину.
3. Отредактируйте параметры (вставьте свои ключи OpenAI/Nvidia/Github).
4. Перезапустите n8n с этими переменными окружения.

## 4. Результаты Развертывания (Project Antigravity) 🚀

Я автоматически развернул все сценарии на ваш Windows-сервер (`igor-gaming-1`).
Вот они в вашем списке Workflows:

1. **Antigravity: Docker & GPU Access Check** (ID: `wUVk7LqlFZJuCfla`)
    - *Проверяет Docker и Ollama.*
2. **Antigravity: GitHub Connection Check** (ID: `VZYlxrKpZ3d9kKR8`)
    - *Проверяет доступ к GitHub.*
3. **Antigravity: AI Commander (Router)** (ID: `Zi4rG3uEdpX73D5N`) 👑
    - *Главный агент. Я уже связал его с первыми двумя инструментами.*

![Deployed Workflows](file:///Users/macbook/.gemini/antigravity/brain/a37df947-0c85-442d-896d-4febcbd36c77/n8n_workflows_list_1765937248629.png)

## 5. Последний штрих (Credentials)

Сценарии загружены, но они "пустые" без ключей.
Зайдите в n8n на Windows и настройте Credentials:

1. Откройте **Antigravity: AI Commander**.
2. Зайдите в узел **Google Gemini Chat**.
3. Выберите/Создайте **Google Vertex AI Credentials**.
4. Сохраните.

Теперь нажмите **Chat** и управляйте своей империей! 🌍

## 6. Устранение неполадок

Если n8n выдает ошибки с правами:

- Убедитесь, что процесс n8n имеет доступ к `docker.sock` (если в докере) или запущен от Admin (если нативно).

## 7. Расширенные возможности (OpenAI & Ngrok)

### 🧠 Как переключиться на GPT-4

Я добавил узел **OpenAI** в сценарий "AI Commander". Чтобы сменить мозг:

1. Откройте сценарий.
2. Удалите связь между *AI Agent* и *Google Gemini*.
3. Протяните связь от *AI Agent* к *OpenAI Chat Model*.
4. В настройках узла OpenAI выберите Credential.

### 🌐 Как включить доступ из интернета (Ngrok)

Чтобы управлять агентом с телефона:

1. На Windows сервере откройте терминал.
2. Запустите:

    ```powershell
    ngrok http 5678
    ```

3. Скопируйте ссылку `https://...ngrok-free.app`.
4. Теперь ваш n8n доступен из любой точки мира!

## 8. Активация "Antigravity Core" (MCP Server)

Мы создали сердце системы — **MCP Server**. Он заменит сложные настройки n8n.

### 1. Развертывание на Windows (Manual)

Так как автоматика требует пароля (SSH ключи не настроены), выполните эти команды в вашем терминале (на Маке):

1. **Загрузка архива (Файл `mcp-server.tgz` готов и лежит в `playground/solar-curie`):**

    ```bash
    scp /Users/macbook/.gemini/antigravity/playground/solar-curie/mcp-server.tgz gonya@igor-gaming-1.tail5e8a72.ts.net:~/
    ```

    *(Введите пароль при запросе)*

2. **Запуск сервера:**

    ```bash
    ssh -t gonya@igor-gaming-1.tail5e8a72.ts.net "tar -xzf mcp-server.tgz && cd antigravity-mcp-server && npm install && npm start"
    ```

![Cloud Config Check](file:///Users/macbook/.gemini/antigravity/brain/a37df947-0c85-442d-896d-4febcbd36c77/mcp_client_url_1765986525500.png)

Сервер запустится на удаленной машине, слушая порт 3000. В консоли вы увидите: `Antigravity MCP Server (HTTP) running on port 3000`.

### Как подключить клиент (Gemini Desktop / Claude)

В конфиге вашего AI-клиента добавьте:

```json
{
  "mcpServers": {
    "antigravity": {
      "command": "node",
      "args": ["C:\\path\\to\\antigravity-mcp-server\\dist\\index.js"]
    }
  }
}
```

Теперь вы можете просить Gemini: *"Проверь докер"* или *"Перезагрузи контейнер"*, и он сделает это напрямую!
