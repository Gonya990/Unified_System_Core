import asyncio
import json
import logging
from pathlib import Path
import nodriver as uc
from datetime import datetime

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

async def load_config():
    if not CONFIG_PATH.exists():
        logger.error(f"Config not found at {CONFIG_PATH}")
        return None
    
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

async def check_linkedin(browser, profile):
    logger.info(f"Checking LinkedIn for {profile['name']}...")
    # Placeholder for actual LinkedIn scraping logic
    # Real implementation needs login handling/cookies
    
    page = await browser.get("https://www.linkedin.com/jobs")
    await asyncio.sleep(5)
    
    # Example logic (to be expanded)
    for keyword in profile['keywords']:
         logger.info(f"Searching for '{keyword}' in {profile['locations']}")
         # await page.type ...
         
    return []

async def main():
    config = await load_config()
    if not config:
        return

    logger.info("Starting Job Hunter...")
    
    # Initialize browser with config args
    browser_args = config.get('settings', {}).get('browser_args', ['--no-sandbox'])
    headless = config.get('settings', {}).get('headless', True) # Default to True for server
    
    if headless:
        browser_args.append("--headless=new")
    
    # Try to find browser path from config or common Linux paths
    browser_path = config.get('settings', {}).get('browser_path')
    if not browser_path:
        # Fallback for server
        possible_paths = ["/usr/bin/google-chrome-stable", "/usr/bin/google-chrome"]
        for p in possible_paths:
            if Path(p).exists():
                browser_path = p
                break

    logger.info(f"Using browser binary: {browser_path}")

    browser = await uc.start(
        browser_args=browser_args,
        headless=headless,
        browser_executable_path=browser_path
    )
    
    try:
        for profile in config['profiles']:
            if not profile.get('enabled', True):
                continue
                
            logger.info(f"Processing profile: {profile['name']}")
            
            if "linkedin" in profile['platforms']:
                jobs = await check_linkedin(browser, profile)
                # Process found jobs (send email etc)
                
    except Exception as e:
        logger.error(f"Error in execution: {e}")
    finally:
        # browser.stop() # close browser if needed, or keep open for debugging
        logger.info("Job Hunter finished cycle.")

if __name__ == "__main__":
    asyncio.run(main())
