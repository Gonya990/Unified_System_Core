#!/usr/bin/env python3
"""
Daily Researcher
Fetches trending topics from RSS feeds and uses the LLM Council to select the most viral one.
Now exports API for factory_scheduler.py
"""

import os
import sys
import json
import logging
import feedparser
from datetime import datetime
from pathlib import Path

# Add paths
current_dir = Path(__file__).parent.resolve()
sys.path.append(str(current_dir))

# Import sibling modules
try:
    from viral_content_generator import generate_script
    from pexels_broll import semantic_search_broll
except ImportError:
    # If running standalone
    pass

# Add LLM Council to path
council_dir = current_dir.parent.parent / "LLM_Council"
sys.path.append(str(council_dir))

try:
    from council.council import LLMCouncil
except ImportError:
    pass

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# RSS Feeds for Tech/AI trends
RSS_FEEDS = [
    "http://feeds.feedburner.com/TechCrunch/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/category/science/latest/rss",
    "https://www.wired.com/feed/tag/ai/latest/rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
]

OUTPUT_FILE = current_dir / "current_daily_topic.json"

def fetch_rss_trends():
    """Fetch headlines from RSS feeds."""
    logger.info("Fetching RSS feeds...")
    topics = []
    
    for url in RSS_FEEDS:
        try:
            logger.info(f"Parsing {url}...")
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]: # Top 5 from each
                topics.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get("summary", "")[:200] + "..."
                })
        except Exception as e:
            logger.error(f"Failed to parse {url}: {e}")
            
    return topics

async def deliberate_on_trends(topics):
    """Use LLM Council to pick the best topic."""
    if not topics:
        logger.warning("No topics found.")
        return None

    logger.info(f"Collected {len(topics)} topics. asking Council...")
    
    # Format topics for the prompt
    topics_list = "\n".join([f"{i+1}. {t['title']} ({t['link']})" for i, t in enumerate(topics[:15])]) 
    
    prompt = f"""
    You are the Editor-in-Chief of a viral tech video channel (TikTok/Reels).
    Review these trending news items:
    
    {topics_list}
    
    Task: Select the ONE topic with the highest potential to go viral if we make a short video about it today.
    Criteria: Controversial, life-changing, or mind-blowing AI news.
    
    Return ONLY a valid JSON object with this format (no markdown, just raw JSON):
    {{
        "title": "The exact headline you chose",
        "angle": "The viral angle/hook we should take (e.g. 'Secret reveal', 'Warning', 'Hype')",
        "reason": "Why this will go viral",
        "source_link": "URL from the list"
    }}
    """
    
    try:
        # Use TokenBroker for keys
        from Scripts.Utilities.token_broker import TokenBroker
        broker = TokenBroker()
        
        # Initialize Council with Broker-managed keys
        try:
             # Use the clean factory method
             council = LLMCouncil.from_token_broker(broker, tier="paid")
        except (ValueError, AttributeError) as e:
             logger.warning(f"TokenBroker/Council init failed ({e}). Trying fallback/legacy env...")
             council = LLMCouncil.from_env()
            
        session = await council.deliberate(prompt, verbose=True)
        final_answer = session.stage3_consensus
        await council.close()
        
        # Cleanup markdown formatting
        clean_json = final_answer.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        return data
        
    except Exception as e:
        logger.error(f"Council deliberation failed: {e}")
        logger.info("Falling back to Heuristic Selection (Mock Council)...")
        if topics:
            best = topics[0]
            logger.info(f"Fallback selected: {best['title']}")
            return {
                "title": best['title'],
                "angle": "Breaking News (Fallback)",
                "reason": "Top trending item selected by heuristic fallback.",
                "source_link": best['link']
            }
        return None

def flatten_script(script_obj):
    """Convert script object to narrative string"""
    text_parts = []
    # Hook isn't always part of sections in viral_content_generator structure?
    # Actually viral_content_generator has sections.
    # We should use sections text.
    
    if "sections" in script_obj:
        for sec in script_obj["sections"]:
            text_parts.append(sec["text"])
    else:
        # Fallback if structure is different
        text_parts.append(script_obj.get("hook", ""))
    
    return " ".join(text_parts)

def extract_scenes(script_obj):
    """Extract visual instructions as scenes"""
    scenes = []
    if "sections" in script_obj:
        for sec in script_obj["sections"]:
            scenes.append({
                "image": sec.get("visual", "abstract tech"), # placeholder desc
                "keyword": sec.get("visual", "technology")   # keyword for search
            })
    return scenes

# --- API for Factory Scheduler ---

def run_daily_research(style="impact"):
    """
    Main entry point called by factory_scheduler.py
    Returns dict: {selected_topic, description, script_ru, scenes}
    """
    import asyncio
    
    logger.info(f"Running Daily Research (Style: {style})...")
    
    # 1. Research Topic
    topics = fetch_rss_trends()
    best_topic_data = asyncio.run(deliberate_on_trends(topics))
    
    if not best_topic_data:
        logger.error("No topic selected.")
        return None

    topic_title = best_topic_data["title"]
    logger.info(f"Selected Topic: {topic_title}")

    # 2. Generate Script
    # We use viral_content_generator logic
    # Try to import if not already
    try:
        from viral_content_generator import generate_script
    except ImportError:
        logger.error("Could not import viral_content_generator")
        return None

    script_obj = generate_script(topic_title, template_type="secret_reveal", lang="ru")
    
    # 3. Format for Scheduler
    script_text = flatten_script(script_obj)
    scenes = extract_scenes(script_obj)
    description = f"{script_obj.get('hook', '')}\n\n{script_obj.get('cta', '')}\n{' '.join(script_obj.get('hashtags', []))}"

    return {
        "selected_topic": topic_title,
        "description": description,
        "script_ru": script_text,
        "scenes": scenes,
        "raw_data": best_topic_data
    }

def generate_vision_assets(scenes, assets_dir: Path, style="impact"):
    """
    Generate or download assets for scenes. Using Style Presets + DALL-E 3.
    """
    logger.info(f"Generating assets for {len(scenes)} scenes in {assets_dir} (Style: {style})...")
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    # Import Presets
    try:
        from style_presets import get_style_prompt, STYLES
    except ImportError:
        # Fallback inline
        def get_style_prompt(s, subj): return f"{subj}, cinematic, 8k"
        STYLES = {"cartoon": {"model": "dalle-3"}, "impact": {"model": "dalle-3"}}

    # Setup Pexels
    try:
        from pexels_broll import semantic_search_broll
        use_pexels = True
    except ImportError:
        use_pexels = False
        
    # Setup OpenAI for DALL-E
    from openai import OpenAI
    client = None
    try:
        from Scripts.Utilities.token_broker import TokenBroker
        broker = TokenBroker()
        key = broker.get_key("openai", tier="paid") # Images are expensive
        if key:
            client = OpenAI(api_key=key)
    except:
        pass
        
    resolved_assets = []
    
    for i, scene in enumerate(scenes):
        keyword = scene.get("keyword", "technology")
        output_path = assets_dir / f"scene_{i}.png" # Default to PNG for images
        
        found_path = None
        
        # Strategy: Mix of Real B-Roll and AI Images
        # If 'impact' style, prefer B-Roll. If 'cartoon', prefer AI.
        
        prefer_ai = (style == "cartoon")
        
        if not prefer_ai and use_pexels:
            clips = semantic_search_broll(keyword, assets_dir, num_clips=1)
            if clips:
                found_path = clips[0]
                
        # If no B-Roll or AI preferred, generate Image
        if not found_path and client:
            try:
                full_prompt = get_style_prompt(style, keyword)
                logger.info(f"🎨 Generating Image: {full_prompt[:50]}...")
                
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=full_prompt,
                    size="1024x1792", # Vertical
                    quality="hd",
                    n=1
                )
                
                image_url = response.data[0].url
                
                # Download
                import requests
                img_data = requests.get(image_url).content
                with open(output_path, 'wb') as f:
                    f.write(img_data)
                
                found_path = str(output_path)
                logger.info(f"✅ Generated: {output_path.name}")
                
            except Exception as e:
                logger.error(f"❌ DALL-E Gen failed: {e}")
        
        resolved_assets.append({
            "keyword": keyword,
            "resolved_path": str(found_path) if found_path else None
        })
        
    return resolved_assets

def translate_to_hebrew(text):
    # Mock translation or use a service
    return f"[HEBREW TRANSLATION] {text}"

def translate_to_english(text):
    # Mock translation
    return f"[ENGLISH TRANSLATION] {text}"

# --- Main CLI ---

def main():
    # CLI Mode
    result = run_daily_research()
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Also save to json for ref
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
