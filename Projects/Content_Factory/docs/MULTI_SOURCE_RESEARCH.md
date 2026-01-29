# 🔍 Multi-Source Research System

**Расширенная система исследований для Content Factory**

---

## Что Это?

Автоматизированная система, которая анализирует **ВСЕ доступные источники** для генерации идей сценариев:

1. ✅ **Telegram каналы** (@vitalycontentcreate + кастомные)
2. ✅ **Google News** (технологии, наука, AI)
3. ✅ **Пользовательские ссылки** (ты добавляешь вручную)
4. ✅ **YouTube Trending** (планируется)
5. ✅ **Reddit** (r/technology, r/Futurology, r/artificial)
6. ✅ **Hacker News** (топ истории)
7. ✅ **Wikipedia** (trending topics)

---

## Быстрый Старт

### 1. Запуск Исследования

```bash
cd /Users/macbook/Documents/Unified_System/Projects/Content_Factory
python3 src/researcher/multi_source_researcher.py
```

### Что происходит:

```
🔍 MULTI-SOURCE RESEARCH AGGREGATION
============================================================
📱 Fetching Telegram insights...       → 10 trending posts
🔗 Fetching user-provided links...     → 3 custom URLs
📰 Fetching Google News...             → 5 tech articles
🔴 Fetching Reddit trending...         → 20 hot posts
🟠 Fetching Hacker News...             → 10 top stories
📚 Fetching Wikipedia trending...      → 8 trending topics

📊 TOTAL INSIGHTS: 56

🎬 Generating 5 script ideas...        → OpenAI GPT-4
💾 Saving report...                    → Reports/
✉️  Broadcasting via Agent Mail...     → All agents notified
```

---

## Добавление Своих Ссылок

### Файл: `Reports/research_links.json`

```json
{
  "links": [
    {
      "url": "https://example.com/cool-ai-article",
      "category": "AI / Tech / Science / Content",
      "priority": "high",
      "notes": "Why this is interesting for script"
    }
  ],
  "last_updated": "2026-01-11T15:00:00"
}
```

### Приоритеты:

- **high** = Score 100 (топ приоритет)
- **medium** = Score 50
- **low** = Score 10

Система автоматически:
1. Скачивает контент по ссылке
2. Извлекает текст
3. Анализирует для идей сценария
4. Учитывает приоритет при ранжировании

---

## Как Работает Scoring

Каждый insight получает **score** (релевантность):

| Источник | Score Logic |
|----------|-------------|
| **Telegram** | Views count (1,940 views = score 1940) |
| **User Links** | Priority (high=100, medium=50, low=10) |
| **Google News** | Fixed 30 (medium priority) |
| **Reddit** | Upvotes / 100 (max 100) |
| **Hacker News** | Points / 10 (max 100) |
| **Wikipedia** | Views / 10,000 (max 100) |

Insights сортируются по score → топ используются для генерации идей.

---

## Примеры Сгенерированных Идей

После анализа **56 insights** система генерирует **5 script ideas** с:

1. **Title**: Цепляющий заголовок
2. **Hook**: Первые 5 секунд (Nikolashin style)
3. **Key Points**: 3-5 основных тезисов
4. **Source Mix**: Telegram + Reddit + News
5. **Viral Potential**: 1-10 score

### Пример Output:

```json
{
  "title": "🚨 Sora 2 БЕСПЛАТНО: Метод из Telegram с 1,730 просмотрами",
  "hook": "СТОП! Прежде чем платить за Sora 2, посмотри этот лайфхак из русского Telegram...",
  "key_points": [
    "Temp mail для обхода ограничений",
    "Аккаунты с unlimited доступом",
    "Пошаговая инструкция из канала @vitalycontentcreate"
  ],
  "source_mix": "Telegram (высокий engagement) + Reddit r/artificial (подтверждение метода)",
  "viral_potential": 9
}
```

---

## Интеграция с Content Factory

### Автоматический Workflow:

```python
# 1. Запуск исследования (manual или scheduled)
python3 src/researcher/multi_source_researcher.py

# 2. Генерация идей → Reports/multi_source_research_*.json

# 3. Content Factory читает топ-идею:
from pathlib import Path
import json

reports = sorted(Path('Reports').glob('multi_source_research_*.json'))
latest = json.loads(reports[-1].read_text())
top_idea = latest['script_ideas'][0]

# 4. Генерация сценария на основе идеи
script = generate_script(top_idea)

# 5. Production pipeline (TTS, video, upload)
produce_video(script)
```

---

## Источники в Деталях

### 1. Telegram (@vitalycontentcreate)

**Что анализируется:**
- Топ-10 постов по просмотрам
- Текст, views, media type
- Trending topics (Sora 2, VEO 3.1, бесплатные инструменты)

**Почему важно:**
- **1,730 avg views** на топ-посты
- Доказанная engagement стратегия
- Русскоязычная аудитория (наша ЦА)

### 2. User Links (research_links.json)

**Что анализируется:**
- URLs, которые ТЫ добавляешь
- Контент скачивается и парсится
- Приоритет: high/medium/low

**Примеры использования:**
- Статья на Hacker News → добавь URL
- Видео на YouTube → добавь URL
- Блог-пост про AI → добавь URL

### 3. Google News

**Что анализируется:**
- Последние 24 часа
- Темы: AI, fusion energy, Mars, quantum computing
- RSS feed → 5 top articles

**Почему важно:**
- Актуальные новости
- Peace & Tech focus
- Глобальный контекст

### 4. Reddit (r/technology, r/Futurology, r/artificial)

**Что анализируется:**
- Hot posts (топ-5 из каждого subreddit)
- Upvotes = relevance score
- Обсуждения в комментариях

**Почему важно:**
- Community insights
- Trending discussions
- Tech-savvy audience

### 5. Hacker News

**Что анализируется:**
- Top 10 stories
- Points (upvotes от tech community)
- URLs к источникам

**Почему важно:**
- High-quality tech content
- Early adopters
- Innovation trends

### 6. Wikipedia Trending

**Что анализируется:**
- Most viewed articles (last 24h)
- Top-10 trending topics
- Pageview counts

**Почему важно:**
- Массовый интерес
- Educational angle
- SEO potential

---

## Reports Structure

### Output File: `Reports/multi_source_research_YYYYMMDD_HHMMSS.json`

```json
{
  "timestamp": "2026-01-11T15:08:00",
  "sources_summary": {
    "telegram": 10,
    "user_links": 3,
    "google_news": 5,
    "reddit": 20,
    "hackernews": 10,
    "wikipedia": 8
  },
  "total_insights": 56,
  "top_insights": [
    {
      "source": "telegram",
      "text": "Sora 2 бесплатно...",
      "views": 1730,
      "score": 1730
    }
  ],
  "script_ideas": [
    {
      "title": "Generated title",
      "hook": "First 5 seconds",
      "key_points": ["Point 1", "Point 2"],
      "viral_potential": 9
    }
  ],
  "sources_data": {
    "telegram": [...],
    "reddit": [...],
    ...
  }
}
```

---

## Agent Mail Integration

После каждого исследования автоматически отправляется broadcast всем агентам:

```markdown
# Multi-Source Research Complete

**Timestamp**: 2026-01-11T15:08:00

## Sources Analyzed:
- Telegram: 10 posts
- User Links: 3 URLs
- Google News: 5 articles
- Reddit: 20 posts
- Hacker News: 10 stories
- Wikipedia: 8 trending topics

**Total Insights**: 56
**Script Ideas Generated**: 5

**Top 3 Ideas**:
1. Sora 2 Free Access Method
2. VEO 3.1 Workflow Tutorial
3. AI Content Factory Automation

**Report**: `Reports/multi_source_research_20260111_150808.json`
```

---

## Scheduling

### Cron Job (каждые 12 часов):

```bash
# Edit crontab
crontab -e

# Add line:
0 */12 * * * cd /Users/macbook/Documents/Unified_System/Projects/Content_Factory && python3 src/researcher/multi_source_researcher.py >> /tmp/research.log 2>&1
```

### Launchd (macOS):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.unified.multi-source-research</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/macbook/Documents/Unified_System/Projects/Content_Factory/src/researcher/multi_source_researcher.py</string>
    </array>
    <key>StartInterval</key>
    <integer>43200</integer> <!-- 12 hours -->
    <key>StandardOutPath</key>
    <string>/tmp/research.log</string>
</dict>
</plist>
```

---

## Next Steps

### Планируемые Улучшения:

1. **YouTube Trending API**
   - Топ-20 видео по категориям
   - Analyze titles/thumbnails для идей

2. **Twitter/X Trending**
   - Hashtags, viral threads
   - Tech influencer tweets

3. **LinkedIn Pulse**
   - Professional content trends
   - B2B insights

4. **AI-Powered Clustering**
   - Группировка похожих insights
   - Trend detection across sources

5. **Sentiment Analysis**
   - Positive/neutral/negative scoring
   - Align with "Peace & Tech" theme

---

## Troubleshooting

### "No insights found"

**Причины:**
- Интернет недоступен
- API rate limits (Reddit, HN)
- Telegram reports отсутствуют

**Решение:**
```bash
# Check internet
ping google.com

# Check Telegram reports
ls Reports/*webscrape*.json

# Run Telegram scraper first
cd Scripts/Research
python3 scrape_telegram_web.py
```

### "Script ideas are empty (N/A)"

**Причина:** OpenAI response parsing failed

**Решение:**
- Проверь API key: `echo $OPENAI_API_KEY`
- Проверь лог: `tail -20 /tmp/research.log`
- JSON format issue в response

### "User links not loading"

**Причина:** `research_links.json` не существует или пустой

**Решение:**
```bash
# Check file
cat Reports/research_links.json

# Add links manually
nano Reports/research_links.json
```

---

## Best Practices

### 1. Качество > Количество

Лучше 5 хороших insights, чем 100 шумных.

**Фильтры:**
- Telegram: минимум 1,000 views
- Reddit: минимум 100 upvotes
- User links: только high/medium priority

### 2. Регулярность

Запускай исследование **каждые 12 часов** для свежих трендов.

### 3. Кураторство

Просматривай generated ideas перед production:
- Соответствие "Peace & Tech" theme
- Viral potential > 7/10
- Практическая ценность

### 4. Обратная Связь

После публикации видео:
- Отмечай какие insights → лучший engagement
- Обновляй research_links.json с новыми источниками
- Улучшай scoring weights

---

## Metrics

### Success Indicators:

| Metric | Target |
|--------|--------|
| Total Insights | > 50 per run |
| Telegram Posts | > 10 trending |
| User Links | > 5 curated |
| Script Ideas | 5 high-quality |
| Viral Potential | Avg > 7/10 |
| Production Rate | 1-2 videos/day from research |

---

**Система готова к использованию! Добавляй свои ссылки в `research_links.json` и запускай исследование!** 🚀

---

**Created**: 2026-01-11
**Agent**: CalmSnow (Antigravity)
**Status**: ✅ Production Ready