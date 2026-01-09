#!/usr/bin/env python3
import os
import sys
import feedparser
import json
import requests
import random
from bs4 import BeautifulSoup
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()
load_dotenv(ROOT_DIR / ".env")

# Configuration
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "5KikfJFyT75Rlibf2u829q4qZOTm0FVfttKCb5znbJSYqb96qAKarEDY")

def get_client():
    """Lazy initialization of OpenAI client with forced base_url to avoid 404s"""
    api_key = os.getenv("OPENAI_API_KEY")
    # Force override to ensure we use the same proven key as orchestrator
    if not api_key:
        api_key = "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"
    
    return OpenAI(
        api_key=api_key,
        base_url="https://api.openai.com/v1"
    )

def get_latest_tech_news():
    """
    Fetches news from Google News RSS with randomized experimental topics.
    """
    topics = [
        "artificial intelligence future tech",
        "quantum computing breakthroughs 2026",
        "neuralink brain computer interface",
        "humanoid robots boston dynamics",
        "spacex mars colonization progress",
        "metaverse web3 evolution",
        "biotechnology longevity research",
        "autonomous vehicles level 5",
        "renewable energy revolution 2026",
        "robotics in healthcare surgery",
        "ai in cybersecurity threat hunting",
        "blockchain beyond crypto 2026",
        "nanotechnology in medicine",
        "6G network release and edge computing",
        "smart cities and digital twins"
    ]
    query = random.choice(topics)
    print(f"📡 Researching topic: {query}")
    
    import urllib.parse
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}+when:1d&hl=en-US&gl=US&ceid=US:en"
    
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:5]: # Take top 5
            items.append({"title": entry.title, "link": entry.link})
        print(f"✅ Found {len(items)} news items.")
        return items
    except Exception as e:
        print(f"❌ News fetch failed: {e}")
        return []

def get_page_content(url):
    """
    BROWSING: Extracts text from a web page to understand the 'mindset'.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for s in soup(["script", "style"]):
            s.decompose()
        text = soup.get_text(separator=' ')
        return " ".join(text.split())[:3000] # Cleaned text, max 3k chars
    except Exception as e:
        print(f"⚠️ Failed to browse {url}: {e}")
        return ""

def run_daily_research(style="impact"):
    """
    DEEP RESEARCH: News -> Browsing -> LLM Insight
    Style: 'impact' (Default) or 'cartoon' (Fun/3D)
    """
    print(f"🧠 Starting DEEP RESEARCH (Browsing + Sentiment Analysis) [Style: {style.upper()}]...")
    news = get_latest_tech_news()
    
    if not news:
        return None
        
    research_context = ""
    for item in news[:2]: # Browse top 2 links
        print(f"🔍 Browsing: {item['title']}...")
        content = get_page_content(item['link'])
        research_context += f"TOPIC: {item['title']}\nCONTENT: {content}\n\n"

    print("🧠 Analyzing human mindset shifts and generating viral script...")
    
    # Style-Specific Prompts
    if style == "cartoon":
        style_prompt = """
        2. Create a FUN, PLAYFUL, and EXCITING script in RUSSIAN.
           - Tone: Enthusiastic, like a Pixar movie intro or a energetic YouTuber.
           - Focus: Wonder, magic of tech, fun possibilities.
           - Style: Simple words, lots of energy!
        3. The script should be formatted for 15 scenes.
        4. Provide 15 visual keywords:
           - MUST include: "3d render", "cartoon style", "cute", "colorful", "animation".
           - Avoid realistic terms.
        """
    else:
        style_prompt = """
        2. Create a high-energy, futuristic script in RUSSIAN (Impact Vision style).
           - Tone: Epic, deep, motivational.
        3. The script should be formatted for 15 scenes.
        4. Provide 15 cinematic image keywords for Pexels (e.g. "cinematic 4k", "dark moody", "cyberpunk").
        """
    
    prompt = f"""
    Analyze the following tech news and the deep content from the pages:
    {research_context}
    
    Your task:
    1. Identify the most impactful 'vibe' or 'mindset shift' this technology brings.
    {style_prompt}
    
    Format output as JSON:
    {{
        "selected_topic": "Dynamic Title",
        "description": "Short social media description",
        "script_ru": "Full text with ... pauses",
        "scenes": [
            {{"image": "scene_1", "keyword": "cinematic keyword"}},
            ... up to 15
        ]
    }}
    """
    
    try:
        response = get_client().chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are a master content strategist and AI trend researcher. Return ONLY a JSON object."},
                      {"role": "user", "content": prompt}]
        )
        # Handle both JSON mode and text response
        content = response.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"❌ LLM Deep Research failed: {e}")
        return None

def translate_to_hebrew(text):
    """
    High-quality translation to Hebrew for the Weekly Special.
    """
    try:
        response = get_client().chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Translate the following futuristic script to HEBREW. Maintain the 'Impact Vision' energy. Return ONLY text."},
                      {"role": "user", "content": text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Hebrew translation failed: {e}")
        return "העתיד כבר כאן. בינה מלאכותית משנה את העולם."
def translate_to_english(text):
    """
    High-quality translation to English for the Weekly Special.
    """
    try:
        response = get_client().chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Translate the following futuristic script to ENGLISH. Maintain the 'Impact Vision' energy. Return ONLY text."},
                      {"role": "user", "content": text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ English translation failed: {e}")
        return "The future is here. AI is transforming the world."

def generate_dalle_assets(scenes, output_dir: Path):
    """
    DALL-E 3 Image generation for the 'Cartoon' look.
    """
    print(f"🎨 Generating {len(scenes)} ORIGINAL CARTOON ASSETS via DALL-E 3...")
    resolved = []
    client = get_client()

    for i, scene in enumerate(scenes):
        try:
            prompt = f"3D animation style, Pixar inspired, high quality, vibrant colors, {scene['keyword']}. Vertical 9:16 aspect ratio focus."
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792", # Portrait mode for Reels
                quality="standard",
                n=1
            )
            
            img_url = response.data[0].url
            img_data = requests.get(img_url).content
            path = output_dir / f"{scene['image']}.jpg"
            with open(path, "wb") as f:
                f.write(img_data)
            
            scene["resolved_path"] = str(path)
            resolved.append(scene)
            print(f"   ✅ DALL-E Asset ready: {scene['image']}")
        except Exception as e:
            print(f"   ⚠️ DALL-E Asset failed for {scene['keyword']}: {e}")
            
    return resolved

def generate_vision_assets(scenes, output_dir: Path, style="impact"):
    """
    Pexels Image/Video or DALL-E asset generation based on style.
    """
    if style == "cartoon":
        return generate_dalle_assets(scenes, output_dir)
        
    print(f"🎨 Generating {len(scenes)} visual assets via Pexels...")
    resolved = []
    
    for scene in scenes:
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {"Authorization": PEXELS_API_KEY}
            params = {"query": scene["keyword"], "per_page": 1, "orientation": "portrait"}
            
            res = requests.get(url, headers=headers, params=params)
            data = res.json()
            
            if data.get("photos"):
                img_url = data["photos"][0]["src"]["large2x"]
                img_data = requests.get(img_url).content
                path = output_dir / f"{scene['image']}.jpg"
                with open(path, "wb") as f:
                    f.write(img_data)
                scene["resolved_path"] = str(path)
                resolved.append(scene)
                print(f"   ✅ Asset ready: {scene['image']}")
        except Exception as e:
            print(f"   ⚠️ Asset failed for {scene['keyword']}: {e}")
            
    return resolved
