#!/usr/bin/env python3
"""
Daily Researcher
Fetches trending topics from RSS feeds and uses the LLM Council to select the most viral one.
"""

import os
import sys
import json
import logging
import feedparser
from datetime import datetime
from pathlib import Path

# Add LLM Council to path
current_dir = Path(__file__).parent.resolve()
council_dir = current_dir.parent.parent / "LLM_Council"
sys.path.append(str(council_dir))

try:
    from council.council import LLMCouncil
except ImportError:
    print("Error: Could not import LLMCouncil. Make sure the path is correct.")
    sys.exit(1)

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
    topics_list = "\n".join([f"{i+1}. {t['title']} ({t['link']})" for i, t in enumerate(topics[:15])]) # Limit to 15 to save context
    
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
        council = LLMCouncil.from_env()
        session = await council.deliberate(prompt, verbose=True)
        final_answer = session.stage3_consensus
        await council.close()
        
        # Cleanup markdown formatting if present
        clean_json = final_answer.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        return data
        
    except Exception as e:
        logger.error(f"Council deliberation failed: {e}")
        logger.info("Falling back to Heuristic Selection (Mock Council)...")
        # Fallback: Pick the first valid topic and format it
        if topics:
            best = topics[0]
            logger.info(f"Fallback selected: {best['title']}")
            return {
                "title": best['title'],
                "angle": "Breaking News (Fallback)",
                "reason": "Top trending item selected by heuristic fallback due to AI service unavailability.",
                "source_link": best['link']
            }
        return None

def main():
    import asyncio
    
    logger.info("Starting Daily Research...")
    
    # 1. Research
    topics = fetch_rss_trends()
    if not topics:
        logger.error("No topics found from RSS feeds.")
        return

    # 2. Deliberate
    best_topic = asyncio.run(deliberate_on_trends(topics))
    
    if best_topic:
        logger.info(f"Selected Topic: {best_topic['title']}")
        
        output_data = {
            "date": datetime.now().isoformat(),
            "topic": best_topic,
            "raw_candidates_count": len(topics)
        }
        
        # 3. Save
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved to {OUTPUT_FILE}")
    else:
        logger.error("Failed to select a topic.")

if __name__ == "__main__":
    main()
