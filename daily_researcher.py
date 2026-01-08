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
    """Lazy initialization of OpenAI client"""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        "autonomous vehicles level 5"
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

def run_daily_research():
    """
    DEEP RESEARCH: News -> Browsing -> LLM Insight
    """
    print("🧠 Starting DEEP RESEARCH (Browsing + Sentiment Analysis)...")
    news = get_latest_tech_news()
    
    if not news:
        return None
        
    research_context = ""
    for item in news[:2]: # Browse top 2 links
        print(f"🔍 Browsing: {item['title']}...")
        content = get_page_content(item['link'])
        research_context += f"TOPIC: {item['title']}\nCONTENT: {content}\n\n"

    print("🧠 Analyzing human mindset shifts and generating viral script...")
    
    prompt = f"""
    Analyze the following tech news and the deep content from the pages:
    {research_context}
    
    Your task:
    1. Identify the most impactful 'vibe' or 'mindset shift' this technology brings.
    2. Create a high-energy, futuristic script in RUSSIAN (Impact Vision style).
    3. The script should be formatted for 15 scenes.
    4. Provide 15 cinematic image keywords for Pexels.
    
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
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are a master content strategist and AI trend researcher."},
                      {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        data = json.loads(response.choices[0].message.content)
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

def generate_vision_assets(scenes, output_dir: Path):
    """
    Pexels Image/Video asset generation.
    """
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
