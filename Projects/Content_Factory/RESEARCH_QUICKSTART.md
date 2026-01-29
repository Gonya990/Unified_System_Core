# 🚀 Multi-Source Research - Quick Start

## В Чем Фишка?

Раньше Content Factory брал идеи только из:
- Google News
- Evergreen topics

**СЕЙЧАС** анализирует **ВСЕ**:
- ✅ Telegram (@vitalycontentcreate - 1,730 views на топ-посты!)
- ✅ Reddit (r/technology, r/Futurology, r/artificial)
- ✅ Hacker News (топ tech stories)
- ✅ Wikipedia trending
- ✅ Google News
- ✅ **ТВОИ ССЫЛКИ** (любые URLs, которые ты добавишь!)

---

## Как Запустить (30 секунд)

### 1. Добавь Свои Ссылки (Опционально)

```bash
nano /Users/macbook/Documents/Unified_System/Reports/research_links.json
```

Добавь любые интересные URLs:

```json
{
  "links": [
    {
      "url": "https://example.com/cool-article",
      "category": "AI Tools",
      "priority": "high",
      "notes": "Viral method for free Sora access"
    }
  ]
}
```

### 2. Запусти Исследование

```bash
cd /Users/macbook/Documents/Unified_System/Projects/Content_Factory
python3 src/researcher/multi_source_researcher.py
```

### 3. Проверь Результат

```bash
# Последний отчет
ls -lt ~/Documents/Unified_System/Reports/multi_source_research_*.json | head -1

# Или открой в VS Code
code ~/Documents/Unified_System/Reports/multi_source_research_*.json
```

---

## Что Внутри Отчета?

```json
{
  "total_insights": 56,
  "sources_summary": {
    "telegram": 10,    // Топ-посты с vitalycontentcreate
    "user_links": 3,   // Твои URLs
    "reddit": 20,      // Hot posts
    "hackernews": 10,  // Top stories
    "wikipedia": 8,    // Trending topics
    "google_news": 5   // Latest tech news
  },
  "script_ideas": [
    {
      "title": "🚨 Sora 2 БЕСПЛАТНО: Метод с 1,730 просмотрами",
      "hook": "СТОП! Прежде чем платить за Sora 2...",
      "key_points": ["Temp mail", "Unlimited access", "Step-by-step"],
      "viral_potential": 9
    }
  ]
}
```

---

## Интеграция с Content Factory

### Вариант 1: Ручной

1. Запусти исследование
2. Открой отчет
3. Выбери топ-идею
4. Запусти factory_scheduler с этой идеей

### Вариант 2: Автоматический (Рекомендуется)

Обнови `factory_scheduler.py` чтобы читать из `multi_source_research_*.json`:

```python
# В factory_scheduler.py
from pathlib import Path
import json

# Load latest research
reports = sorted(Path('Reports').glob('multi_source_research_*.json'))
if reports:
    latest = json.loads(reports[-1].read_text())
    top_idea = latest['script_ideas'][0]

    # Use top_idea for script generation
    script = f"""
    Title: {top_idea['title']}
    Hook: {top_idea['hook']}
    Key Points: {', '.join(top_idea['key_points'])}
    """

    # Continue with production...
```

---

## Автоматизация (Запуск Каждые 12 Часов)

### macOS (Launchd)

Создай файл: `~/Library/LaunchAgents/com.unified.research.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.unified.research</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/macbook/Documents/Unified_System/Projects/Content_Factory/src/researcher/multi_source_researcher.py</string>
    </array>
    <key>StartInterval</key>
    <integer>43200</integer>
    <key>StandardOutPath</key>
    <string>/tmp/research.log</string>
</dict>
</plist>
```

Затем:

```bash
launchctl load ~/Library/LaunchAgents/com.unified.research.plist
```

---

## Примеры Добавления Ссылок

### AI Tools

```json
{
  "url": "https://www.reddit.com/r/artificial/comments/xyz/",
  "category": "AI Tools",
  "priority": "high",
  "notes": "Free ChatGPT alternatives discussion"
}
```

### Tech News

```json
{
  "url": "https://news.ycombinator.com/item?id=12345678",
  "category": "Tech Innovation",
  "priority": "medium",
  "notes": "Breakthrough in quantum computing"
}
```

### YouTube Videos

```json
{
  "url": "https://youtu.be/abc123",
  "category": "Content Strategy",
  "priority": "high",
  "notes": "Viral video formula analysis"
}
```

---

## Мониторинг

### Проверка Последнего Запуска

```bash
# Когда последний раз запускалось
ls -lt ~/Documents/Unified_System/Reports/multi_source_research_*.json | head -1

# Сколько insights
python3 -c "import json; print(json.load(open(sorted(glob.glob('Reports/multi_source_research_*.json'))[-1]))['total_insights'])"
```

### Agent Mail Notifications

После каждого исследования ты получишь broadcast:

```
🔍 Multi-Source Research Complete

Sources Analyzed: 56 insights
- Telegram: 10 trending posts
- User Links: 3 URLs
- Reddit: 20 hot posts
- ...

Top 3 Ideas:
1. Sora 2 Free Access Method
2. VEO 3.1 Tutorial
3. AI Factory Automation
```

---

## FAQ

**Q: Можно ли добавить свои Telegram каналы?**

A: Да! Запусти Telegram scraper для любого канала:

```bash
TELEGRAM_CHANNEL=other_channel python3 Scripts/Research/scrape_telegram_web.py
```

**Q: Как часто запускать исследование?**

A: Рекомендуется **каждые 12 часов** для свежих трендов.

**Q: Что делать если идеи не генерируются?**

A: Проверь:
1. OpenAI API key: `echo $OPENAI_API_KEY`
2. Наличие insights: должно быть > 10
3. Лог: `tail -50 /tmp/research.log`

---

## Next Steps

1. ✅ Запусти исследование прямо сейчас
2. ✅ Добавь 3-5 своих любимых источников в research_links.json
3. ✅ Настрой автоматизацию (launchd)
4. ✅ Интегрируй с factory_scheduler
5. ✅ Отслеживай какие insights дают лучший engagement

---

**Готово! Теперь у тебя круг исследований в 10x раз шире!** 🎯

Полная документация: `docs/MULTI_SOURCE_RESEARCH.md`