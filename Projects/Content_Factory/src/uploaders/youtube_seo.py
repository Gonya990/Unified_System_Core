#!/usr/bin/env python3
"""
YouTube SEO Engine — UnifiedCore Content Factory
Generates optimized titles, descriptions, tags, and thumbnails
using Gemini AI + trending data analysis.
"""

import json
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Setup paths
UPLOADERS_DIR = Path(__file__).parent.resolve()
SRC_DIR = UPLOADERS_DIR.parent
FACTORY_DIR = SRC_DIR.parent
ROOT_DIR = FACTORY_DIR.parent.parent

# Load env
load_dotenv(FACTORY_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


# ─────────────────────────────────────────────
#  GEMINI CLIENT (lightweight, no heavy deps)
# ─────────────────────────────────────────────

# Best available model (auto-select)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _gemini_generate(prompt: str, max_tokens: int = 1024, json_mode: bool = False) -> Optional[str]:
    """Call Gemini API directly via requests."""
    try:
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        gen_config = {"maxOutputTokens": max_tokens, "temperature": 0.7}
        if json_mode:
            gen_config["responseMimeType"] = "application/json"
            gen_config["temperature"] = 0.3  # Lower temp for structured output
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": gen_config,
        }
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"⚠️ Gemini error: {e}")
        return None


def _openai_generate(prompt: str, max_tokens: int = 1024, json_mode: bool = False) -> Optional[str]:
    """Call OpenAI API as fallback."""
    try:
        import requests
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.3 if json_mode else 0.7,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        r = requests.post("https://api.openai.com/v1/chat/completions",
                          headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"⚠️ OpenAI error: {e}")
        return None


def _ai_generate(prompt: str, max_tokens: int = 1024, json_mode: bool = False) -> Optional[str]:
    """Try Gemini first, then OpenAI."""
    if GEMINI_API_KEY:
        result = _gemini_generate(prompt, max_tokens, json_mode=json_mode)
        if result:
            return result
    if OPENAI_API_KEY:
        return _openai_generate(prompt, max_tokens, json_mode=json_mode)
    return None


# ─────────────────────────────────────────────
#  SEO TITLE GENERATOR
# ─────────────────────────────────────────────

def generate_optimized_title(
    topic: str,
    lang: str = "ru",
    style: str = "shorts",  # "shorts" | "longform" | "documentary"
    max_chars: int = 100,
) -> dict:
    """
    Generate 3 optimized YouTube title variants.
    Returns: {"titles": [...], "recommended": "..."}
    """
    lang_map = {"ru": "Russian", "en": "English", "he": "Hebrew"}
    lang_name = lang_map.get(lang, "Russian")

    style_instructions = {
        "shorts": "Short, punchy, curiosity-gap. Use numbers when possible. Max 60 chars.",
        "longform": "Detailed, SEO-rich. Include primary keyword early. Max 100 chars.",
        "documentary": "Cinematic, dramatic. Sounds like a Netflix title. Max 80 chars.",
    }

    prompt = f"""You are a YouTube SEO expert with 10M+ view channels.

Generate 3 highly clickable YouTube titles for this content:
Topic: {topic}
Language: {lang_name}
Style: {style_instructions.get(style, style_instructions['shorts'])}

Rules:
- Hook the viewer in first 3 words
- Use power words (secret, revolutionary, shocking, finally, exposed)
- Include main keyword naturally
- NO clickbait that disappoints (deliver on the promise)
- {lang_name} language ONLY

Return JSON:
{{
  "titles": ["title1", "title2", "title3"],
  "recommended": "title1",
  "primary_keyword": "main keyword used"
}}"""

    result = _ai_generate(prompt, 512, json_mode=True)
    if not result:
        # Fallback
        return {
            "titles": [topic[:max_chars]],
            "recommended": topic[:max_chars],
            "primary_keyword": topic.split()[0] if topic else "AI",
        }

    try:
        # json_mode guarantees clean JSON
        data = json.loads(result.strip())
        # Handle case where Gemini wraps in extra key
        if isinstance(data, dict) and "titles" not in data:
            # Try to extract from first list value
            for v in data.values():
                if isinstance(v, list):
                    return {"titles": v, "recommended": v[0] if v else topic[:max_chars], "primary_keyword": topic}
        return data
    except Exception:
        # Parse manually
        lines = [line.strip().strip('"').strip("'") for line in result.split("\n") if line.strip() and len(line) > 10]
        titles = lines[:3] if len(lines) >= 3 else [topic[:max_chars]]
        return {"titles": titles, "recommended": titles[0], "primary_keyword": topic}


# ─────────────────────────────────────────────
#  SEO DESCRIPTION GENERATOR
# ─────────────────────────────────────────────

def generate_description(
    topic: str,
    script: str = "",
    chapters: list = None,
    tags: list = None,
    lang: str = "ru",
    channel_name: str = "Megaforma",
) -> str:
    """
    Generate full SEO-optimized YouTube description.
    Includes: hook, body, chapters, links, hashtags.
    """
    lang_map = {"ru": "Russian", "en": "English", "he": "Hebrew"}
    lang_name = lang_map.get(lang, "Russian")

    script_preview = script[:500] if script else ""
    chapters_text = "\n".join(chapters) if chapters else ""

    prompt = f"""You are a YouTube SEO expert. Write a full video description.

Topic: {topic}
Language: {lang_name}
Script excerpt: {script_preview}
Channel: {channel_name}

Description must include (in this order):
1. HOOK (2-3 sentences that expand on the title, make viewer want to watch)
2. WHAT YOU'LL LEARN (3-5 bullet points)
3. TIMESTAMPS (if chapters provided below, use them exactly)
4. SUBSCRIBE CTA
5. HASHTAGS (10-15 relevant, mix popular + niche)

Timestamps section:
{chapters_text if chapters_text else "(no chapters for this video)"}

Write ONLY the description text, no extra commentary.
Use {lang_name} for main content, hashtags in English+{lang_name}."""

    result = _ai_generate(prompt, 1024, json_mode=False)  # Free-text for description
    if not result:
        # Minimal fallback
        hashtags = " ".join(f"#{t}" for t in (tags or ["AI", "Technology", "Future"])[:15])
        return f"{topic}\n\n🔔 Подписывайся на канал {channel_name}!\n\n{hashtags}"

    return result.strip()


# ─────────────────────────────────────────────
#  TAGS GENERATOR
# ─────────────────────────────────────────────

def generate_tags(
    topic: str,
    script: str = "",
    lang: str = "ru",
    max_tags: int = 35,
) -> list:
    """
    Generate 35 YouTube tags: mix of broad, medium, and long-tail.
    """
    prompt = f"""Generate exactly {max_tags} YouTube tags for this video about: {topic}
Language context: {lang}

Tag strategy:
- 5 broad tags (1-2 words, high volume) e.g. AI, technology, нейросети
- 15 medium tags (2-4 words) e.g. artificial intelligence 2026
- 15 long-tail tags (4-7 words) e.g. how AI will change the world 2026

Rules:
- Mix Russian and English tags for multilingual discovery
- Include year 2026 in some tags
- NO duplicate meaning, most relevant first

IMPORTANT: Output ONLY a raw JSON array, nothing else. No markdown, no explanation.
Example format: ["tag1", "tag2", "tag3"]"""

    result = _ai_generate(prompt, 800, json_mode=True)
    if not result:
        return ["AI", "технологии", "будущее", "искусственный интеллект",
                "artificial intelligence", "technology 2026", "AI news",
                "tech future", "нейросети", "neural networks"]

    # Strip any markdown fences
    cleaned = result.strip()
    for fence in ["```json", "```"]:
        if fence in cleaned:
            cleaned = cleaned.split(fence)[1].split("```")[0].strip()
            break

    # Try JSON parse on the whole result first
    try:
        tags = json.loads(cleaned)
        if isinstance(tags, list):
            return [str(t) for t in tags if t][:max_tags]
    except Exception:
        pass

    # Try to find JSON array anywhere in result
    import re
    match = re.search(r'\[.*?\]', cleaned, re.DOTALL)
    if match:
        try:
            tags = json.loads(match.group())
            if isinstance(tags, list):
                return [str(t) for t in tags if t][:max_tags]
        except Exception:
            pass

    # Last resort: line-by-line parse
    tags = [
        line.strip().strip('"').strip("'").strip(",").strip()
        for line in cleaned.split("\n")
        if line.strip() and len(line.strip()) > 2 and not line.strip().startswith("[")
    ]
    return [tag for tag in tags if tag and len(tag) > 1][:max_tags]


# ─────────────────────────────────────────────
#  FULL SEO PACKAGE
# ─────────────────────────────────────────────

def generate_full_seo_package(
    topic: str,
    script: str = "",
    chapters: list = None,
    lang: str = "ru",
    style: str = "shorts",
    channel_name: str = "Megaforma",
) -> dict:
    """
    Generate complete SEO package: title + description + tags.
    Returns dict ready to pass to youtube_uploader.upload_video()
    """
    print(f"🔍 Generating SEO package for: {topic[:50]}...")

    # 1. Title
    title_data = generate_optimized_title(topic, lang=lang, style=style)
    title = title_data.get("recommended", topic[:100])
    print(f"  📝 Title: {title}")

    # 2. Tags
    tags = generate_tags(topic, script=script, lang=lang)
    print(f"  🏷️  Tags: {len(tags)} generated")

    # 3. Description
    description = generate_description(
        topic, script=script, chapters=chapters,
        tags=tags, lang=lang, channel_name=channel_name
    )
    print(f"  📄 Description: {len(description)} chars")

    return {
        "title": title,
        "title_alternatives": title_data.get("titles", []),
        "description": description,
        "tags": tags,
        "primary_keyword": title_data.get("primary_keyword", topic),
    }


# ─────────────────────────────────────────────
#  CATEGORY SELECTOR
# ─────────────────────────────────────────────

YOUTUBE_CATEGORIES = {
    "tech": "28",         # Science & Technology
    "education": "27",   # Education
    "news": "25",        # News & Politics
    "entertainment": "24", # Entertainment
    "people": "22",      # People & Blogs
    "gaming": "20",      # Gaming
}

def get_category_id(topic: str, script: str = "") -> str:
    """Auto-detect the best YouTube category ID."""
    text = (topic + " " + script[:200]).lower()

    if any(w in text for w in ["технология", "technology", "ai", "программ", "код", "software", "hardware"]):
        return YOUTUBE_CATEGORIES["tech"]
    elif any(w in text for w in ["политика", "news", "новости", "геополитика"]):
        return YOUTUBE_CATEGORIES["news"]
    elif any(w in text for w in ["урок", "обучение", "learn", "tutorial", "как", "how to"]):
        return YOUTUBE_CATEGORIES["education"]
    else:
        return YOUTUBE_CATEGORIES["tech"]  # Default for our channel


# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="YouTube SEO Engine")
    parser.add_argument("--topic", required=True, help="Video topic")
    parser.add_argument("--lang", default="ru", choices=["ru", "en", "he"])
    parser.add_argument("--style", default="shorts", choices=["shorts", "longform", "documentary"])
    parser.add_argument("--script", default="", help="Script text (optional)")
    args = parser.parse_args()

    result = generate_full_seo_package(
        topic=args.topic,
        script=args.script,
        lang=args.lang,
        style=args.style,
    )

    print("\n" + "=" * 60)
    print("📊 SEO PACKAGE READY")
    print("=" * 60)
    print(f"🎯 TITLE: {result['title']}")
    print(f"\n🏷️  TAGS ({len(result['tags'])}):\n  {', '.join(result['tags'][:10])}...")
    print(f"\n📄 DESCRIPTION (first 300 chars):\n{result['description'][:300]}...")
