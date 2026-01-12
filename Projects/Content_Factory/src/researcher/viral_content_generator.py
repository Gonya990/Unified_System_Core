#!/usr/bin/env python3
"""
Viral Content Research & Script Generator
Uses web research and AI to create engaging scripts
"""

import json
from pathlib import Path

# Trending Topics Research (Jan 2026)
TRENDS_2026 = {
    "ai_technology": [
        "AI-powered daily life hacks",
        "How AI is replacing traditional jobs (with solutions)",
        "5 AI tools that will change your life in 2026",
        "The dark side of AI nobody talks about"
    ],
    "business_finance": [
        "Passive income ideas that actually work 2026",
        "Why 90% of startups fail (and how to avoid it)",
        "From $0 to $10K/month: realistic timeline",
        "Skills that will make you rich in 2026"
    ],
    "self_improvement": [
        "Morning routines of billionaires (the truth)",
        "How to learn any skill 10x faster",
        "3 habits that changed my life completely",
        "Why you're always tired (and how to fix it)"
    ],
    "tech_reviews": [
        "Gadgets that are actually worth buying 2026",
        "iPhone vs Android in 2026: honest comparison",
        "The best apps you've never heard of",
        "Tech fails that cost millions"
    ]
}

# Script Templates with Hooks
SCRIPT_TEMPLATES = {
    "controversy": {
        "hook": "Вот почему {topic} — это ЛОЖЬ, о которой все молчат...",
        "structure": ["hook", "problem_reveal", "unexpected_twist", "solution", "cta"]
    },
    "secret_reveal": {
        "hook": "Это секрет, который {authority} не хотят, чтобы вы знали...",
        "structure": ["hook", "build_curiosity", "revelation", "proof", "action"]
    },
    "transformation": {
        "hook": "Год назад я был {before_state}. Сегодня я {after_state}. Вот что я сделал...",
        "structure": ["hook", "journey", "turning_point", "method", "results"]
    },
    "listicle": {
        "hook": "5 вещей, которые {result} за {timeframe}. Номер 3 изменил всё...",
        "structure": ["hook", "item_1", "item_2", "item_3_dramatic", "item_4", "item_5", "conclusion"]
    }
}

def generate_script(topic: str, template_type: str = "secret_reveal", lang: str = "ru") -> dict:
    """
    Generate viral script for given topic

    Args:
        topic: Main topic/niche
        template_type: controversy, secret_reveal, transformation, listicle
        lang: ru or en

    Returns:
        Script dict with sections
    """

    # Example: AI tools script
    if "ai" in topic.lower() or "ии" in topic.lower():
        script = {
            "title": "5 AI инструментов, которые заменят 90% работников к 2027 году",
            "hook": "Через 2 года твоя профессия может исчезнуть. Вот 5 AI инструментов, которые уже делают это...",
            "sections": [
                {
                    "name": "hook_expansion",
                    "text": "Я провел 200 часов тестируя эти инструменты. И что я понял — мы на пороге революции.",
                    "visual": "dramatic_face_closeup"
                },
                {
                    "name": "tool_1",
                    "text": "Первый — это ChatGPT o3. Он пишет код лучше, чем 80% программистов. Серьезно.",
                    "visual": "screen_recording_chatgpt"
                },
                {
                    "name": "tool_2",
                    "text": "Второй — Midjourney V7. Дизайнеры уже теряют работу. Вот что он создает за секунды...",
                    "visual": "midjourney_examples"
                },
                {
                    "name": "twist",
                    "text": "Но вот что никто не говорит — те кто ОСВОЯТ эти инструменты станут зарабатывать в 10 раз больше.",
                    "visual": "talking_head_intense"
                },
                {
                    "name": "solution",
                    "text": "Я создал бесплатный гайд как использовать AI для твоей профессии. Ссылка в био.",
                    "visual": "cta_overlay"
                }
            ],
            "duration_seconds": 45,
            "hashtags": ["#AI", "#нейросети", "#технологии", "#будущее", "#работа2026"],
            "cta": "Подпишись чтобы не пропустить следующий выпуск!"
        }
    else:
        script = {
            "title": f"Viral Script: {topic}",
            "hook": SCRIPT_TEMPLATES[template_type]["hook"].format(topic=topic),
            "sections": [],
            "duration_seconds": 30,
            "hashtags": [],
            "cta": ""
        }

    return script

def find_untranslated_viral_content(source_lang: str = "en", target_langs: list = None) -> list:
    """
    Find viral videos without translations to target languages

    Strategy:
    1. Search trending videos in source language
    2. Check if translations exist for each target language
    3. Return list of opportunities
    """

    # This would use YouTube/TikTok API in production
    if target_langs is None:
        target_langs = ["ru", "he", "ar"]
    opportunities = [
        {
            "platform": "TikTok",
            "creator": "@tech_insider",
            "video": "How AI will change everything",
            "views": "15M",
            "languages_missing": ["ru", "he"],
            "opportunity_score": 9.5
        },
        {
            "platform": "YouTube",
            "creator": "Fireship",
            "video": "100+ Web Dev Things You Should Know",
            "views": "8M",
            "languages_missing": ["ru", "ar"],
            "opportunity_score": 8.7
        },
        {
            "platform": "TikTok",
            "creator": "@ali_abdaal",
            "video": "How I Read 100 Books a Year",
            "views": "12M",
            "languages_missing": ["he"],
            "opportunity_score": 8.2
        }
    ]

    return opportunities

if __name__ == "__main__":
    # Check for daily topic from daily_researcher.py
    daily_topic_path = Path(__file__).parent / "current_daily_topic.json"

    if daily_topic_path.exists():
        print(f"Loading daily topic from {daily_topic_path}...")
        try:
            with open(daily_topic_path, encoding='utf-8') as f:
                data = json.load(f)
                topic_data = data.get('topic', {})
                topic_title = topic_data.get('title', "AI Tools 2026")
                topic_angle = topic_data.get('angle', "secret_reveal")
                script = generate_script(topic_title, "secret_reveal", "ru")
                # Inject the angle/reason into the script context if possible,
                # but for now we just use the title to generate the script.
                print(f"✅ Uses Council Selected Topic: {topic_title}")
                print(f"📐 Angle: {topic_angle}")
        except Exception as e:
            print(f"❌ Failed to load daily topic: {e}")
            script = generate_script("AI инструменты 2026", "secret_reveal", "ru")
    else:
        print("⚠️ No daily topic found. Using default.")
        script = generate_script("AI инструменты 2026", "secret_reveal", "ru")

    print("=" * 50)
    print(f"📹 SCRIPT: {script['title']}")
    print("=" * 50)
    print(f"\n🎯 HOOK: {script['hook']}\n")

    for _i, section in enumerate(script['sections'], 1):
        print(f"[{section['name']}] {section['text']}")
        print(f"  Visual: {section['visual']}\n")

    print(f"⏱ Duration: {script['duration_seconds']}s")
    print(f"📌 CTA: {script['cta']}")
    print(f"#️⃣ {' '.join(script['hashtags'])}")

    print("\n" + "=" * 50)
    print("🔍 TRANSLATION OPPORTUNITIES:")
    print("=" * 50)

    for opp in find_untranslated_viral_content():
        print(f"\n{opp['platform']} | {opp['creator']}")
        print(f"  {opp['video']} ({opp['views']} views)")
        print(f"  Missing: {', '.join(opp['languages_missing'])}")
        print(f"  Score: {opp['opportunity_score']}/10")
