# API Key Setup Instructions

## ❌ Проблема

Все API ключи в `.env` устарели или являются placeholder'ами:

| Provider | Status | Error |
|----------|--------|-------|
| OpenAI | ❌ Invalid | 401 Incorrect API key |
| Google Gemini | ❌ Expired | 400 API key expired |
| OpenRouter | ❌ Placeholder | "PLEASE_UPDATE" |

## ✅ Решения

Выберите ОДИН вариант для получения ключа:

### Option 1: Google Gemini (FREE!)

**Рекомендуется** - бесплатный и быстрый

1. Перейдите: <https://aistudio.google.com/apikey>
2. Нажмите "Create API Key"  
3. Скопируйте ключ
4. Добавьте в `.env`:

   ```bash
   GEMINI_API_KEY=AIza...ваш_ключ
   GOOGLE_API_KEY=AIza...ваш_ключ
   ```

### Option 2: OpenAI (Paid)

1. Перейдите: <https://platform.openai.com/api-keys>
2. Create new secret key
3. Скопируйте (показывается 1 раз!)
4. Добавьте в `.env`:

   ```bash
   OPENAI_API_KEY=sk-proj-...ваш_ключ
   ```

### Option 3: OpenRouter (Pay-as-you-go)

Доступ к Claude, GPT, Gemini через один API

1. Перейдите: <https://openrouter.ai/settings/keys>
2. Create Key
3. Добавьте в `.env`:

   ```bash
   OPENROUTER_API_KEY=sk-or-v1-...ключ
   ```

## 🚀 После получения ключа

Запустите тест:

```bash
cd ~/Documents/Unified_System_Core/Projects/AI_Core
source .venv/bin/activate

# Для Gemini:
python tests/test_gemini_agent.py

# Для OpenAI:
python tests/test_agent.py
```

## ℹ️ Где находится .env

```
~/Documents/Unified_System_Core/Projects/AI_Core/.env
```

Отредактируйте этот файл и замените placeholder на реальный ключ.
