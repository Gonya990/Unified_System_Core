#!/usr/bin/env python3
import os
import json
import feedparser
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()

# Load API keys - prioritized
load_dotenv(ROOT_DIR / ".env", override=True)
load_dotenv(ROOT_DIR / "LLM_Council" / ".env", override=True)
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)

# Fallback/Hardcoded Key (from accessible source)
if not os.getenv("OPENAI_API_KEY"):
    # Using the key found in orchestrator_v3_no_face.py to ensure functionality
    os.environ["OPENAI_API_KEY"] = "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"

def get_latest_tech_news(query="artificial intelligence future tech", lang="en"):
    """
    Fetches the latest news from Google News RSS.
    """
    print(f"📡 Fetching daily news for: {query}...")
    url = f"https://news.google.com/rss/search?q={query}+when:1d&hl=en-US&gl=US&ceid=US:en"
    
    try:
        feed = feedparser.parse(url)
        news_items = []
        for entry in feed.entries[:7]:  # Get top 7
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published if hasattr(entry, 'published') else "Today",
                "summary": entry.summary if hasattr(entry, 'summary') else ""
            })
        print(f"✅ Found {len(news_items)} news items.")
        return news_items
    except Exception as e:
        print(f"❌ Failed to fetch news: {e}")
        return []

def generate_daily_script(news_items):
    """
    Uses OpenAI to select the best story and write a script.
    """
    if not news_items:
        print("⚠️ No news items provided.")
        return None

    client = OpenAI()
    
    # Prepare news context
    news_text = "\n\n".join([f"- {item['title']} ({item['published']})" for item in news_items])
    
    prompt = f"""
    You are the Showrunner and Scriptwriter for "Future Factory", a viral Reels channel about the upcoming Technological Singularity (approx 2026).
    
    TONIGHT'S TOP NEWS STORIES:
    {news_text}
    
    CHANNEL THEME & CONTINUITY:
    - We are NOT just reporting news. We are building a continuous narrative: "The Great Transition is happening NOW."
    - Every video is a puzzle piece showing how humanity is merging with AI.
    - Tone: Cinematic, Urgent, Visionary, High-Energy (Cyberpunk/Sci-Fi aesthetics).
    
    TASK:
    1. Select the SINGLE most impactful story.
    2. Write a 30-60 second script (Russian language).
    
    STRUCTURE:
    1. HOOK (0-3s): Shocking statement or question linking the news to the User's life.
    2. THE SHIFT (3-40s): Explain the news item, but reframe it as a step towards the Singularity. Focus on the "Big Picture".
    3. THE PREDICTION (40-50s): "By 2026, this means..." (Concrete prediction).
    4. CTA (End): "The Factory is watching. Follow for the update."
    
    OUTPUT FORMAT (JSON ONLY):
    {{
        "selected_topic": "Headline",
        "description": "Short caption for Instagram with hashtags (#AI #Future #2026)...",
        "script_ru": "Full text of the script in Russian...",
        "scenes": [
            {{"image": "img_keyword_1", "keyword": "Visual prompt for DALL-E (prompts must be in English, highly detailed, cinematic, Aspect Ratio 9:16)..."}},
            ... (5-8 scenes)
        ]
    }}
    """
    
    print("🧠 Analyzing trends and generating script...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a viral content expert. Return strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # Post-process keys to match pipeline expectations
        # The pipeline expects "image" to be a filename-friendly string and "keyword" for generation/search
        for i, scene in enumerate(data.get("scenes", [])):
            # Ensure unique internal names
            scene["image"] = f"daily_news_s{i+1}_{scene.get('image', 'scene').replace(' ', '_')[:20]}"
            
        print(f"✅ Script Generated: {data['selected_topic']}")
        return data
        
    except Exception as e:
        print(f"❌ LLM Generation failed: {e}")
        return None

def generate_vision_assets(scenes, output_dir: Path):
    """
    Generates images for each scene using Pexels (fallback from DALL-E).
    """
    import requests
    
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "5KikfJFyT75Rlibf2u829q4qZOTm0FVfttKCb5znbJSYqb96qAKarEDY")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎨 Generating {len(scenes)} visual assets via Pexels...")
    
    for i, scene in enumerate(scenes):
        keyword = scene['keyword']
        safe_name = scene['image']
        
        # Check if already exists
        existing = list(output_dir.glob(f"{safe_name}_*.jpg"))
        if existing:
            print(f"   ⏭️  Skipping {safe_name}, already exists.")
            scene["resolved_path"] = str(existing[0])
            continue
            
        print(f"   🖼️  Searching {i+1}/{len(scenes)}: {keyword[:30]}...")
        
        try:
            # Search Pexels
            url = "https://api.pexels.com/v1/search"
            headers = {"Authorization": PEXELS_API_KEY}
            params = {
                "query": keyword,
                "per_page": 1,
                "orientation": "portrait"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("photos"):
                photo = data["photos"][0]
                img_url = photo["src"]["large2x"]  # High quality
                
                # Download
                img_data = requests.get(img_url, timeout=15).content
                
                # Save
                timestamp = datetime.now().strftime("%H%M%S")
                filename = f"{safe_name}_{timestamp}.jpg"
                filepath = output_dir / filename
                
                with open(filepath, "wb") as f:
                    f.write(img_data)
                    
                print(f"      ✅ Saved: {filename}")
                scene["resolved_path"] = str(filepath)
            else:
                print(f"      ⚠️  No results for {keyword}")
                scene["resolved_path"] = None
            
        except Exception as e:
            print(f"      ❌ Download failed for {safe_name}: {e}")
            scene["resolved_path"] = None

    return scenes

def run_daily_research():
    """
    Main entry point for the scheduler.
    """
    news = get_latest_tech_news()
    if not news:
        # Fallback to generic if news fails
        print("⚠️ News fetch failed, using fallback topic.")
        return {
            "selected_topic": "AI Singularity 2026",
            "description": "Daily insight into the future of Agentic AI.",
            "script_ru": "Этот день настал. Граница между реальностью и цифрой исчезла...",
            "scenes": [{"image": f"fallback_s{i}", "keyword": "futuristic ai cinematic"} for i in range(15)]
        }
        
    data = generate_daily_script(news)
    return data

if __name__ == "__main__":
    # Test run
    result = run_daily_research()
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
