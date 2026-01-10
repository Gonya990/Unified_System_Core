
import os
import sys
import requests
import datetime
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env")

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MorningBrief")

def get_weather(lat=32.08, lon=34.78): # Tel Aviv Default
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        r = requests.get(url, timeout=5)
        data = r.json()
        current = data.get("current_weather", {})
        temp = current.get("temperature")
        code = current.get("weathercode")
        return f"{temp}°C (Code: {code})"
    except Exception as e:
        logger.error(f"Weather fetch failed: {e}")
        return "Weather unavailable"

def get_calendar_events():
    # TODO: Integrate with IdentityOrchestrator for real events
    return [
        {"time": "08:00", "title": "School Start"},
        {"time": "14:00", "title": "Football Practice"}
    ]

def generate_brief():
    logger.info("Generating Morning Brief...")
    
    weather = get_weather()
    events = get_calendar_events()
    
    # Get Homework (Import Sentinel)
    try:
        from Scripts.Family.homework_sentinel import scan_mailbox, summarize_tasks
        # Mock user
        homework_summary = summarize_tasks([]) 
    except ImportError:
        homework_summary = "Homework Scan Failed."
        
    brief = f"""
🌅 **Good Morning, Artur!**
    
🌤️ **Weather:** {weather}
    
📅 **Schedule:**
"""
    for e in events:
        brief += f"- {e['time']}: {e['title']}\n"
        
    brief += f"\n📚 **Homework:**\n{homework_summary}\n"
    
    brief += "\n🚀 *\"The expert in anything was once a beginner.\"* - Helen Hayes"
    
    return brief

if __name__ == "__main__":
    report = generate_brief()
    print(report)
    
    # TODO: Send to Telegram
