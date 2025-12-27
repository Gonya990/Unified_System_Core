# Unified AI Bot (Gonya)

Мощный Telegram бот, объединяющий управление умным домом, задачи, генерацию контента и поиск информации. Работает на базе `python-telegram-bot` и интегрируется с Gemini, OpenAI, Ollama, Home Assistant и Yandex Alice.

## 🚀 Функциональность

| Feature      | Описание | Команда / Инструмент |
| :---         | :---     | :---                 |
| **AI Chat**  | Умный диалог с поддержкой контекста. Поддержка Gemini 2.0, GPT-4, Llama 3. | Обычный текст |
| **Voice Msgs** | Распознавание речи (Whisper) и ответ текстом. | Голосовое сообщение |
| **Image Gen** | Генерация изображений через DALL-E 3. | `/imagine <prompt>` |
| **Home Control** | Управление светом и статусом Home Assistant. | `/ha status`, `/ha lights on/off` |
| **Web Search** | Поиск информации в интернете (DuckDuckGo). | `/search <query>` |
| **Task Manager** | Простой список задач (SQLite). | `/todo add/list/done` |
| **Reminders** | Напоминания по времени. | `/remind 10m text` |
| **Infra Map** | Статус серверов и сервисов. | `/infra` |
| **Vision** | Анализ изображений (Gemini Vision). | Отправь фото (+caption) |
| **Cost Tracking** | Учет использования токенов. | `/usage` |
| **Job Hunter** | Запуск скрипта поиска вакансий. | `/scan` |
| **Alice Skill** | Голосовое управление через Яндекс Алису. | Webhook port 8090 |

## 🛠 Установка и Запуск

### Требования

- Python 3.10+
- `cloudflared` (для Алисы)
- Redis (опционально для кэша)

### 1. Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Конфигурация (.env)

Создайте файл `.env` в корне проекта:

```ini
TELEGRAM_BOT_TOKEN=your_token
ALLOWED_USERS=12345678,87654321

# Inference Providers
INFERENCE_PROVIDER=gemini  # ollama / openai / gemini
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key
OLLAMA_BASE_URL=http://localhost:11434

# Home Assistant
HA_API_URL=http://homeassistant:8123
HA_API_TOKEN=your_ha_token

# Databases
USAGE_DB_PATH=usage.db
TASKS_DB_PATH=tasks.db
```

### 3. Запуск

```bash
# Прямой запуск
python -m src.main

# Systemd (Linux)
sudo systemctl start ai-bot
```

## 🗣 Настройка Яндекс Алисы (Alice Skill)

Бот запускает веб-сервер на порту `8090` для приема команд от Алисы.

1. **Запустите туннель** (если сервер за NAT):

   ```bash
   cloudflared tunnel --url http://localhost:8090
   ```

2. **Создайте навык** в [Яндекс.Диалогах](https://dialogs.yandex.ru/developer).
3. **Webhook URL**: Используйте URL от cloudflared + `/alice` (например, `https://xyz.trycloudflare.com/alice`).
4. **Примеры фраз**:
   - "Попроси Гоню включить свет на кухне"
   - "Спроси у Гони статус сервера"

## 📚 Команды Бота

- `/start` - Приветствие
- `/help` - Помощь
- `/status` - Статус системы и модели
- `/models` - Выбор AI модели
- `/setprovider` - Переключение провайдера (Gemini/Ollama/OpenAI)
- `/setmodel` - Установка конкретной модели
- `/imagine` - Генерация картинки
- `/search` - Поиск в Google/DDG
- `/todo` - Управление задачами
- `/ha` - Управление Home Assistant
- `/usage` - Статистика использования
- `/scan` - Запуск Job Hunter
- `/clear` - Очистка контекста диалога

## 🔒 Безопасность

- Доступ только для пользователей из `ALLOWED_USERS`.
- Чувствительные команды (`[[RUN:CMD]]`) фильтруются через whitelist.
- API ключи шифруются при сохранении (если настроено).

---
Developed by Gonya for Unified System.

## 🛡️ Monitoring (Watchdog)

Для автоматического мониторинга здоровья бота используется `ai-watchdog.service`.
Он проверяет `/health` endpoint каждые 60 секунд.

**Установка:**
```bash
sudo cp Windows_AI_Core/config/ai-watchdog.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ai-watchdog
sudo systemctl start ai-watchdog
```
