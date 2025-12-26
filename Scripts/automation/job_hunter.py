import asyncio
import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Browser Use & LangChain
try:
    from browser_use import Agent
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    # Fallback for local dev without libs
    Agent = None

from telegram_notify import send_telegram_message

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("job_hunter.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("JobHunter")

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "profiles.json"
ENV_PATH = BASE_DIR / ".env"

# Load Env
load_dotenv(ENV_PATH)
# Also try to load from Windows_AI_Core locations if on server
load_dotenv(BASE_DIR.parent.parent / "Windows_AI_Core" / ".env")


async def load_config():
    if not CONFIG_PATH.exists():
        logger.error(f"Config not found at {CONFIG_PATH}")
        return None
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def get_llm():
    """Configure LLM based on environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return ChatOpenAI(model="gpt-4o", api_key=api_key)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        real_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=gemini_key)
        
        class GeminiAdapter:
            def __init__(self, llm):
                self._llm = llm
                self.provider = "google"
                self.model_name = llm.model
            
            def __getattr__(self, name):
                return getattr(self._llm, name)
            
            async def ainvoke(self, *args, **kwargs):
                return await self._llm.ainvoke(*args, **kwargs)
                
            def invoke(self, *args, **kwargs):
                return self._llm.invoke(*args, **kwargs)
                
        return GeminiAdapter(real_llm)
        
    logger.error("No valid API Key found (OPENAI_API_KEY or GEMINI_API_KEY)")
    return None

async def process_profile(profile, llm):
    if not Agent:
        logger.error("browser-use library not installed!")
        return

    logger.info(f"Processing profile: {profile['name']}...")
    
    # Simplified prompt for initial E2E test (LinkedIn often requires login)
    task_desc = (
        f"Go to google.com. "
        f"Search for '{profile['keywords'][0]} jobs in {profile['locations'][0]}'. "
        f"Identify 2 interesting job titles from the results. "
        f"Return them as a simple string summary."
    )
            
    logger.info(f"Starting Agent Task: {task_desc}")
    
    try:
        agent = Agent(task=task_desc, llm=llm)
        result = await agent.run()
        
        logger.info(f"Task Result: {result}")
        
        # Notify
        msg = f"🔍 **Job Hunt Report for {profile['name']}**\n\n{result}"
        send_telegram_message(msg)
        
    except Exception as e:
        logger.error(f"Agent failed: {e}")
        send_telegram_message(f"⚠️ Job Hunter Error for {profile['name']}: {e}")

async def main():
    config = await load_config()
    if not config:
        return
    
    llm = get_llm()
    if not llm:
        logger.error("LLM not configured. Exiting.")
        send_telegram_message("⚠️ Job Hunter failed: No LLM API Key found.")
        return

    logger.info("Starting Job Hunter (Browser Use)...")
    send_telegram_message("🚀 Job Hunter Agent Started")

    try:
        for profile in config['profiles']:
            if not profile.get('enabled', True):
                continue
            await process_profile(profile, llm)
                
    except Exception as e:
        logger.error(f"Critical Error: {e}")
    finally:
        logger.info("Job Hunter finished cycle.")

if __name__ == "__main__":
    asyncio.run(main())
