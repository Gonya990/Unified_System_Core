#!/usr/bin/env python3
"""
Консилиум — Content Research & Script Council
═══════════════════════════════════════════════
Автономный мультиагентный модуль для:
1. ТРЕНД-СКАУТ     — собирает топ-тренды (Google/YouTube/HN/Reddit)
2. АНАЛИТИК        — ранжирует по виральности для наших каналов
3. СЦЕНАРИСТ       — генерирует полный сценарий + SEO пакет
4. ДИРЕКТОР        — оркестрирует всё и выдаёт production-ready пакет

Output: outputs/consilium/YYYY-MM-DD_HH-MM/<topic>/
  - brief.json     (тренд + анализ)
  - script.json    (сценарий 15 сцен)
  - seo.json       (title/tags/description)
  - ready.json     (всё вместе для загрузки)
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import warnings
from datetime import datetime
from pathlib import Path

import feedparser
import requests
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

# ── Path setup ────────────────────────────────────────────────────────────────
SRC_DIR      = Path(__file__).parent.parent.resolve()   # Content_Factory/src
FACTORY_DIR  = SRC_DIR.parent                            # Content_Factory/
PROJECTS_DIR = FACTORY_DIR.parent                        # Projects/
ROOT_DIR     = PROJECTS_DIR.parent                       # Unified_System_Core/

sys.path.insert(0, str(SRC_DIR / "uploaders"))
sys.path.insert(0, str(SRC_DIR / "pipeline"))
sys.path.insert(0, str(SRC_DIR / "researcher"))

load_dotenv(FACTORY_DIR / ".env")
load_dotenv(PROJECTS_DIR / "AI_Core/.env", override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_ID       = os.getenv("ADMIN_ID", "708531393")

OUTPUT_BASE = FACTORY_DIR / "outputs" / "consilium"
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════════════════════════
#  АГЕНТ 1: ТРЕНД-СКАУТ
#  Собирает живые тренды из нескольких источников
# ══════════════════════════════════════════════════════════════

class TrendScout:
    """Собирает тренды из: Google News RSS, YouTube Trending API,
    Hacker News, Reddit r/technology + r/artificial, RSS feeds."""

    CHANNEL_THEMES = {
        "megaforma": [
            "artificial intelligence", "AI breakthrough", "neural network",
            "robot", "future technology", "quantum computing", "space",
            "geopolitics", "economic collapse", "singularity", "AGI",
            "OpenAI", "Gemini", "ChatGPT", "Elon Musk", "Sam Altman",
        ],
        "unifiedsystem": [
            "AI coding", "LLM development", "autonomous agents", "Python AI",
            "software architecture", "GitHub Copilot", "cursor AI", "vibe coding",
            "AI tools developer", "model context protocol", "Claude", "Gemini API",
        ],
    }

    def fetch_google_news(self, queries: list[str], max_per_query: int = 5) -> list[dict]:
        """Google News RSS — топ статьи за 24ч."""
        results = []
        for q in queries[:4]:  # Limit queries to avoid rate limits
            encoded = urllib.parse.quote(q)
            url = f"https://news.google.com/rss/search?q={encoded}+when:1d&hl=en-US&gl=US&ceid=US:en"
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:max_per_query]:
                    results.append({
                        "source": "google_news",
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "query": q,
                    })
                time.sleep(0.3)
            except Exception as e:
                print(f"   ⚠️ Google News [{q}]: {e}")
        return results

    def fetch_hacker_news(self, limit: int = 20) -> list[dict]:
        """Hacker News Top Stories (tech-focused)."""
        try:
            ids = requests.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json",
                timeout=8
            ).json()[:limit]
            items = []
            for story_id in ids:
                try:
                    item = requests.get(
                        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                        timeout=5
                    ).json()
                    if item and item.get("type") == "story":
                        items.append({
                            "source": "hacker_news",
                            "title": item.get("title", ""),
                            "link": item.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                            "score": item.get("score", 0),
                            "comments": item.get("descendants", 0),
                        })
                except Exception:
                    pass
            return sorted(items, key=lambda x: x["score"], reverse=True)[:10]
        except Exception as e:
            print(f"   ⚠️ HN fetch: {e}")
            return []

    def fetch_reddit_trending(self, subreddits: list[str] = None) -> list[dict]:
        """Reddit hot posts (no auth needed)."""
        if subreddits is None:
            subreddits = ["artificial", "technology", "MachineLearning", "singularity"]
        items = []
        headers = {"User-Agent": "UnifiedCore-ContentBot/1.0"}
        for sub in subreddits[:3]:
            try:
                r = requests.get(
                    f"https://www.reddit.com/r/{sub}/hot.json?limit=10",
                    headers=headers, timeout=8
                )
                if r.status_code == 200:
                    posts = r.json().get("data", {}).get("children", [])
                    for p in posts:
                        d = p.get("data", {})
                        if d.get("score", 0) > 100:
                            items.append({
                                "source": f"reddit/{sub}",
                                "title": d.get("title", ""),
                                "link": f"https://reddit.com{d.get('permalink', '')}",
                                "score": d.get("score", 0),
                                "comments": d.get("num_comments", 0),
                            })
                time.sleep(0.5)
            except Exception as e:
                print(f"   ⚠️ Reddit/{sub}: {e}")
        return sorted(items, key=lambda x: x["score"], reverse=True)[:15]

    def fetch_youtube_trending(self, channel: str = "megaforma") -> list[dict]:
        """YouTube Data API — trending videos in tech category."""
        yt_key = os.getenv("YOUTUBE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not yt_key:
            print("   ⚠️ No YOUTUBE_API_KEY — skipping YouTube trending")
            return []
        try:
            r = requests.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params={
                    "part": "snippet,statistics",
                    "chart": "mostPopular",
                    "regionCode": "US",
                    "videoCategoryId": "28",  # Science & Technology
                    "maxResults": 15,
                    "key": yt_key,
                },
                timeout=10
            )
            if r.status_code == 200:
                return [
                    {
                        "source": "youtube_trending",
                        "title": item["snippet"]["title"],
                        "link": f"https://youtube.com/watch?v={item['id']}",
                        "views": int(item.get("statistics", {}).get("viewCount", 0)),
                        "channel": item["snippet"]["channelTitle"],
                    }
                    for item in r.json().get("items", [])
                ]
        except Exception as e:
            print(f"   ⚠️ YT Trending: {e}")
        return []

    def gather_all(self, channel: str = "megaforma") -> dict:
        """Собирает тренды из всех источников."""
        print("🔍 ТРЕНД-СКАУТ: Сканирую источники...")
        themes = self.CHANNEL_THEMES.get(channel, self.CHANNEL_THEMES["megaforma"])
        queries = themes[:6]  # Top 6 themes for queries

        print("  📰 Google News...")
        news = self.fetch_google_news(queries)
        print(f"     {len(news)} статей найдено")

        print("  💻 Hacker News...")
        hn = self.fetch_hacker_news()
        print(f"     {len(hn)} историй")

        print("  👾 Reddit...")
        reddit = self.fetch_reddit_trending()
        print(f"     {len(reddit)} постов")

        print("  📺 YouTube Trending...")
        yt = self.fetch_youtube_trending(channel)
        print(f"     {len(yt)} видео")

        return {
            "timestamp": datetime.now().isoformat(),
            "channel": channel,
            "google_news": news,
            "hacker_news": hn,
            "reddit": reddit,
            "youtube_trending": yt,
            "total_signals": len(news) + len(hn) + len(reddit) + len(yt),
        }


# ══════════════════════════════════════════════════════════════
#  АГЕНТ 2: АНАЛИТИК
#  Ранжирует тренды, выбирает топ-3 для сценариев
# ══════════════════════════════════════════════════════════════

class TrendAnalyst:
    """Использует Gemini для анализа трендов и выбора лучших тем."""

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model   = GEMINI_MODEL

    def _gemini(self, prompt: str, json_mode: bool = True) -> str | None:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        cfg = {"maxOutputTokens": 4096, "temperature": 0.4}
        if json_mode:
            cfg["responseMimeType"] = "application/json"
        r = requests.post(
            url,
            json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": cfg},
            timeout=60
        )
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        print(f"⚠️ Gemini analyst error: {r.status_code}")
        return None

    def analyze(self, raw_trends: dict, channel: str = "megaforma", top_n: int = 3) -> list[dict]:
        """Анализирует тренды, выбирает топ-N самых виральных тем."""
        # Flatten all signals into readable list
        all_titles = []
        for item in raw_trends.get("google_news", [])[:15]:
            all_titles.append(f"[NEWS] {item['title']}")
        for item in raw_trends.get("hacker_news", [])[:10]:
            all_titles.append(f"[HN score={item['score']}] {item['title']}")
        for item in raw_trends.get("reddit", [])[:10]:
            all_titles.append(f"[Reddit score={item['score']}] {item['title']}")
        for item in raw_trends.get("youtube_trending", [])[:8]:
            all_titles.append(f"[YT views={item['views']:,}] {item['title']}")

        if not all_titles:
            print("⚠️ No trends to analyze — using evergreen fallback")
            return self._evergreen_topics(channel, top_n)

        channel_focus = {
            "megaforma": "Russian-speaking audience, AI/tech future, geopolitics, humanity's future. Inspirational, documentary tone.",
            "unifiedsystem": "Developer community, AI coding tools, autonomous agents, software architecture. Technical but accessible.",
        }.get(channel, "AI and technology")

        prompt = f"""You are a YouTube content strategist for channel: {channel}.
Channel focus: {channel_focus}

Analyze these {len(all_titles)} trending signals from today:
{chr(10).join(all_titles[:50])}

Select the TOP {top_n} topics that:
1. Are HIGHLY viral right now (evidenced by multiple signals)
2. Match the channel's audience
3. Have strong hook potential (controversy, surprise, fear, hope)
4. Can be covered in a 60-second YouTube Short

For each topic return:
- topic_title: catchy Russian-language video concept (even if original is English)
- viral_score: 1-10 (how viral this is)
- hook: the opening line/hook for the video (in Russian)
- angle: unique angle/take that makes it different from others
- format: "shorts" or "longform"
- why_now: why this is trending RIGHT NOW (1 sentence)
- english_topic: original topic in English for research

Return JSON array of {top_n} objects."""

        result = self._gemini(prompt, json_mode=True)
        if result:
            try:
                topics = json.loads(result.strip())
                if isinstance(topics, list):
                    print(f"✅ Аналитик выбрал {len(topics)} тем для производства")
                    return topics
            except Exception as e:
                print(f"⚠️ Parse error: {e}")

        return self._evergreen_topics(channel, top_n)

    def _evergreen_topics(self, channel: str, top_n: int) -> list[dict]:
        """Fallback: вечнозелёные темы когда нет живых данных."""
        evergreen = [
            {
                "topic_title": "ИИ заменит 50% профессий к 2027: что делать?",
                "viral_score": 9,
                "hook": "Половина рабочих мест исчезнет через 3 года. Это не страшилка — это McKinsey.",
                "angle": "Личный план выживания в эпоху ИИ",
                "format": "shorts",
                "why_now": "Массовые увольнения в BigTech продолжаются",
                "english_topic": "AI job displacement 2027",
            },
            {
                "topic_title": "Gemini 2.5 vs GPT-4o: кто реально лучше в 2026?",
                "viral_score": 8,
                "hook": "Я протестировал обоих на 100 задачах. Результат вас удивит.",
                "angle": "Честное сравнение без рекламы",
                "format": "shorts",
                "why_now": "Gemini 2.5 Flash только что вышел",
                "english_topic": "Gemini 2.5 vs GPT-4o comparison",
            },
            {
                "topic_title": "Автономные агенты ИИ: конец программистам?",
                "viral_score": 8,
                "hook": "Claude уже пишет весь код. Зачем нанимать разработчика?",
                "angle": "Взгляд изнутри — от разработчика который видит это каждый день",
                "format": "longform",
                "why_now": "Cursor и Copilot захватывают рынок",
                "english_topic": "AI autonomous coding agents replacing developers",
            },
        ]
        return evergreen[:top_n]


# ══════════════════════════════════════════════════════════════
#  АГЕНТ 3: СЦЕНАРИСТ
#  Генерирует полный сценарий по теме
# ══════════════════════════════════════════════════════════════

class ScriptWriter:
    """Создаёт профессиональные сценарии в стиле Megaforma/UnifiedSystem."""

    CHANNEL_STYLES = {
        "megaforma": {
            "lang": "ru",
            "tone": "Вдохновляющий, визионерский, оптимистичный. Стиль: глубокий документальный. Максим Николашин + NatGeo.",
            "structure": "Hook (5 сек) → Шок-факт → 5-7 ключевых пунктов → CTA",
            "duration": "55-58 секунд для Shorts, 12-15 мин для Longform",
            "cta": "Подпишись — здесь мы делаем будущее понятным.",
        },
        "unifiedsystem": {
            "lang": "en",
            "tone": "Technical but accessible. Like Fireship.io meets Andrej Karpathy.",
            "structure": "Problem → Context → Solution → Code example → Summary",
            "duration": "55-58 seconds for Shorts, 8-12 min for Longform",
            "cta": "Subscribe for weekly AI dev breakdowns.",
        },
    }

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model   = GEMINI_MODEL

    def _gemini(self, prompt: str, json_mode: bool = True) -> str | None:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        cfg = {"maxOutputTokens": 8192, "temperature": 0.8}
        if json_mode:
            cfg["responseMimeType"] = "application/json"
        r = requests.post(
            url,
            json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": cfg},
            timeout=90
        )
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        print(f"⚠️ Gemini scriptwriter error: {r.status_code} - {r.text[:200]}")
        return None

    def write_script(self, topic: dict, channel: str = "megaforma") -> dict:
        """Генерирует полный сценарий для одной темы."""
        style = self.CHANNEL_STYLES.get(channel, self.CHANNEL_STYLES["megaforma"])
        lang = style["lang"]
        is_shorts = topic.get("format", "shorts") == "shorts"

        duration_note = "~58 seconds when read aloud at natural pace" if is_shorts else "12-15 minutes"
        scenes_count = 8 if is_shorts else 15
        lang_name = "Russian" if lang == "ru" else "English"

        prompt = f"""You are a world-class YouTube scriptwriter for channel {channel}.

TOPIC: {topic['topic_title']}
HOOK: {topic['hook']}
ANGLE: {topic['angle']}
WHY NOW: {topic['why_now']}
FORMAT: {"YouTube Shorts (vertical 9:16)" if is_shorts else "Long-form documentary"}
DURATION: {duration_note}
LANGUAGE: {lang_name}

STYLE: {style['tone']}
STRUCTURE: {style['structure']}
CTA: {style['cta']}

Write a complete script with {scenes_count} scenes.

CRITICAL RULES:
- Language: {lang_name} ONLY (no mixing)
- Start with the hook IMMEDIATELY — no intro
- Each scene: 1-3 punchy sentences max (for Shorts)
- NO scene labels like "Scene 1:", just the spoken text
- Visual keywords in ENGLISH (for image generation)
- End with emotional CTA

Return JSON:
{{
  "title": "Final catchy title in {lang_name}",
  "script_text": "Full spoken script (narrator voice only)",
  "pinned_comment": "Engaging question for comments ({lang_name})",
  "scenes": [
    {{
      "id": "scene_01",
      "spoken": "Narrator text for this scene",
      "visual_keyword": "English prompt for AI image generation, cinematic, 9:16",
      "duration_sec": 7
    }}
  ],
  "total_duration_sec": {58 if is_shorts else 720},
  "mood": "inspiring/shocking/educational/controversial"
}}"""

        print(f"  ✍️  Пишу сценарий: {topic['topic_title'][:50]}...")
        result = self._gemini(prompt, json_mode=True)
        if result:
            try:
                script = json.loads(result.strip())
                script["channel"] = channel
                script["format"] = topic.get("format", "shorts")
                script["source_topic"] = topic
                print(f"     ✅ {len(script.get('scenes', []))} сцен, {script.get('total_duration_sec', '?')}сек")
                return script
            except Exception as e:
                print(f"     ⚠️ Parse error: {e}")

        return {"title": topic["topic_title"], "script_text": topic["hook"], "scenes": [], "error": "generation_failed"}


# ══════════════════════════════════════════════════════════════
#  АГЕНТ 4: SEO-ПАКОВЩИК
#  Упаковывает сценарий с SEO пакетом
# ══════════════════════════════════════════════════════════════

def package_with_seo(script: dict, channel: str = "megaforma") -> dict:
    """Добавляет SEO пакет к сценарию."""
    try:
        from youtube_seo import generate_full_seo_package
        lang_map = {"megaforma": "ru", "unifiedsystem": "en"}
        lang = lang_map.get(channel, "ru")

        seo = generate_full_seo_package(
            topic=script.get("title", ""),
            script=script.get("script_text", ""),
            lang=lang,
            style=script.get("format", "shorts"),
            channel_name=channel.capitalize(),
        )
        return {**script, "seo": seo}
    except Exception as e:
        print(f"  ⚠️ SEO packaging failed: {e}")
        return script


# ══════════════════════════════════════════════════════════════
#  ДИРЕКТОР — главный оркестратор
# ══════════════════════════════════════════════════════════════

def notify_telegram(message: str):
    """Отправляет уведомление в Telegram."""
    if not TELEGRAM_TOKEN:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_ID, "text": message, "parse_mode": "Markdown"},
            timeout=10
        )
    except Exception:
        pass


def run_consilium(
    channel: str = "megaforma",
    top_n: int = 3,
    notify: bool = True,
    save_outputs: bool = True,
) -> list[dict]:
    """
    Полный цикл Консилиума:
    Тренды → Анализ → Сценарии → SEO → Сохранение

    Returns: список production-ready пакетов
    """
    session_id = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_dir = OUTPUT_BASE / session_id / channel
    output_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("╔══════════════════════════════════════════════════════╗")
    print(f"║  🎓 КОНСИЛИУМ | {channel.upper():<38} ║")
    print(f"║  {session_id:<52} ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    # ── ЭТАП 1: Сбор трендов ───────────────────────────────────
    print("═" * 55)
    print("📡 ЭТАП 1: ТРЕНД-СКАУТ")
    print("═" * 55)
    scout   = TrendScout()
    raw     = scout.gather_all(channel=channel)
    print(f"   Итого сигналов: {raw['total_signals']}")

    if save_outputs:
        (output_dir / "trends_raw.json").write_text(
            json.dumps(raw, ensure_ascii=False, indent=2)
        )

    # ── ЭТАП 2: Анализ и выбор тем ────────────────────────────
    print()
    print("═" * 55)
    print("🧠 ЭТАП 2: АНАЛИТИК — выбираю топ темы")
    print("═" * 55)
    analyst = TrendAnalyst()
    topics  = analyst.analyze(raw, channel=channel, top_n=top_n)

    print("\n   🏆 Выбранные темы:")
    for i, t in enumerate(topics, 1):
        print(f"   {i}. [{t.get('viral_score', '?')}/10] {t['topic_title']}")

    if save_outputs:
        (output_dir / "topics_selected.json").write_text(
            json.dumps(topics, ensure_ascii=False, indent=2)
        )

    # ── ЭТАП 3: Написание сценариев ───────────────────────────
    print()
    print("═" * 55)
    print("✍️  ЭТАП 3: СЦЕНАРИСТ — пишу сценарии")
    print("═" * 55)
    writer   = ScriptWriter()
    packages = []

    for i, topic in enumerate(topics, 1):
        print(f"\n📝 Сценарий {i}/{len(topics)}: {topic['topic_title'][:45]}...")
        script = writer.write_script(topic, channel=channel)

        # ── ЭТАП 4: SEO упаковка ──────────────────────────────
        print("  🎯 SEO упаковка...")
        package = package_with_seo(script, channel=channel)
        package["session_id"]  = session_id
        package["channel"]     = channel
        package["created_at"]  = datetime.now().isoformat()
        package["output_dir"]  = str(output_dir)
        package["status"]      = "ready_for_production"
        packages.append(package)

        # Save individual package
        if save_outputs:
            slug = topic["topic_title"][:40].replace(" ", "_").replace("/", "-")
            pkg_dir = output_dir / f"{i:02d}_{slug}"
            pkg_dir.mkdir(exist_ok=True)
            (pkg_dir / "package.json").write_text(
                json.dumps(package, ensure_ascii=False, indent=2)
            )
            # Separate script text file for easy reading
            (pkg_dir / "script.txt").write_text(
                f"TITLE: {package.get('title', '')}\n\n"
                f"HOOK: {topic.get('hook', '')}\n\n"
                f"SCRIPT:\n{package.get('script_text', '')}\n\n"
                f"PINNED COMMENT: {package.get('pinned_comment', '')}\n\n"
                f"SEO TITLE: {package.get('seo', {}).get('title', '')}\n"
                f"TAGS: {', '.join(package.get('seo', {}).get('tags', [])[:10])}\n",
                encoding="utf-8"
            )

    # ── ФИНАЛЬНЫЙ ОТЧЁТ ───────────────────────────────────────
    print()
    print("═" * 55)
    print(f"✅ КОНСИЛИУМ ЗАВЕРШЁН | {len(packages)} пакетов готовы")
    print("═" * 55)

    summary_lines = [f"📦 Выход: {output_dir}\n"]
    for i, pkg in enumerate(packages, 1):
        title = pkg.get("title", pkg.get("source_topic", {}).get("topic_title", "?"))
        seo_title = pkg.get("seo", {}).get("title", "")
        tags_count = len(pkg.get("seo", {}).get("tags", []))
        scenes_count = len(pkg.get("scenes", []))
        print(f"\n🎬 {i}. {title}")
        print(f"   SEO: {seo_title}")
        print(f"   Тегов: {tags_count} | Сцен: {scenes_count}")
        summary_lines.append(f"{i}. {title}\n   SEO: {seo_title}\n   Тегов: {tags_count}")

    # Save full session summary
    if save_outputs:
        (output_dir / "_session_summary.json").write_text(
            json.dumps({
                "session_id": session_id,
                "channel": channel,
                "total_packages": len(packages),
                "packages": [
                    {
                        "title": p.get("title", ""),
                        "seo_title": p.get("seo", {}).get("title", ""),
                        "format": p.get("format", ""),
                        "tags_count": len(p.get("seo", {}).get("tags", [])),
                        "scenes_count": len(p.get("scenes", [])),
                        "status": p.get("status", ""),
                    }
                    for p in packages
                ],
            }, ensure_ascii=False, indent=2)
        )

    # Telegram уведомление
    if notify and TELEGRAM_TOKEN:
        msg = (
            f"🎓 *КОНСИЛИУМ* — {session_id}\n"
            f"📺 Канал: `{channel}`\n"
            f"📦 Готово: {len(packages)} пакетов\n\n"
            + "\n".join(summary_lines[:5])
        )
        notify_telegram(msg)
        print("\n📱 Telegram уведомление отправлено")

    print(f"\n📁 Все файлы: {output_dir}")
    return packages


# ══════════════════════════════════════════════════════════════
#  CLI
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="🎓 Консилиум — Research & Script Council",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 content_council.py                         # Megaforma, 3 темы
  python3 content_council.py --channel unifiedsystem # UnifiedSystem канал
  python3 content_council.py --top 5                 # 5 тем
  python3 content_council.py --channel megaforma --top 1 --no-notify
        """
    )
    parser.add_argument("--channel", choices=["megaforma", "unifiedsystem", "both"],
                        default="megaforma", help="Канал (default: megaforma)")
    parser.add_argument("--top", type=int, default=3,
                        help="Сколько тем исследовать (default: 3)")
    parser.add_argument("--no-notify", action="store_true",
                        help="Не отправлять Telegram уведомление")
    parser.add_argument("--dry-run", action="store_true",
                        help="Не сохранять файлы")
    args = parser.parse_args()

    if args.channel == "both":
        for ch in ["megaforma", "unifiedsystem"]:
            run_consilium(
                channel=ch,
                top_n=args.top,
                notify=not args.no_notify,
                save_outputs=not args.dry_run,
            )
            time.sleep(5)
    else:
        packages = run_consilium(
            channel=args.channel,
            top_n=args.top,
            notify=not args.no_notify,
            save_outputs=not args.dry_run,
        )
        print(f"\n🚀 Готово! {len(packages)} сценариев ждут производства.")
