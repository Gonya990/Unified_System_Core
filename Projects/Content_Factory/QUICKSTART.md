# 🚀 AI CONTENT FACTORY - QUICK START

## ⚡ Быстрая команда для теста

```bash
ssh unified-home-core-cloud \
"cd /home/gonya/Unified_System_Core/Projects/Content_Factory && \
python3 test_ai_factory.py"
```

---

## 🎯 Активация AI (когда будут ключи)

### 1. Редактировать .env

```bash
ssh unified-home-core-cloud
nano /home/gonya/Unified_System_Core/Projects/Content_Factory/.env
```

### 2. Добавить ключи

```bash
SUNO_API_KEY=sk-...
ELEVENLABS_API_KEY=...
RUNWAY_API_KEY=...

USE_AI_MUSIC=true
USE_AI_VOICE=true
USE_AI_VIDEO=true
```

### 3. Сохранить (Ctrl+O, Enter, Ctrl+X)

### 4. Перезапустить (если в PM2)

```bash
pm2 restart factory
```

---

## 📝 Команды бота (когда будут добавлены)

```text
/aimusic upbeat electronic 60    - Suno музыка
/aivoice excited Hello AI!       - ElevenLabs голос
/aisub impact Amazing future     - Impact субтитры
```

---

## 📚 Документация

- **Полная инструкция:** `AI_FACTORY_README.md`
- **Отчёт о развёртывании:** `DEPLOYMENT_REPORT.md`
- **Шаблон конфигурации:** `.env.ai_template`

---

## ✅ Текущий статус

- ✅ Все модули на железе
- ✅ Субтитры работают 100%
- ✅ Музыка (fallback режим)
- ⏸️ Голос (нужен API key)
- ⏸️ Видео (нужен API key)

**Готовность:** 76% (100% с API ключами)

---

🔥 **ПОЛНЫЙ ВПЕРЁД!**
