#!/usr/bin/env python3
"""
Morning Brief Scheduler
Runs morning_brief.py at scheduled time daily (default 7:00 AM).
Maintains a persistent loop checking for the scheduled time.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Setup paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
FAMILY_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from dotenv import load_dotenv  # noqa: E402

# Load environment configuration
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env")
load_dotenv(FAMILY_DIR / ".env")

# Setup logging
LOG_DIR = ROOT_DIR / "logs/family"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "morning_brief_scheduler.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("MorningBriefScheduler")

# Import the brief function
from Scripts.Family.morning_brief import send_brief  # noqa: E402

# Schedule settings from environment
SCHEDULE_HOUR = int(os.getenv("BRIEF_TIME_HOUR", "7"))
SCHEDULE_MINUTE = int(os.getenv("BRIEF_TIME_MINUTE", "0"))


async def run_at_scheduled_time():
    """
    Run brief at scheduled time every day.
    Sleeps until the next scheduled time, then executes the brief.
    """
    logger.info(f"Morning Brief Scheduler started. Brief will run at {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d} daily")

    while True:
        now = datetime.now()

        # Create target time for today
        target_time = now.replace(hour=SCHEDULE_HOUR, minute=SCHEDULE_MINUTE, second=0, microsecond=0)

        # If target time passed today, schedule for tomorrow
        if now > target_time:
            target_time += timedelta(days=1)

        # Calculate sleep time in seconds
        sleep_seconds = (target_time - now).total_seconds()
        hours_until = sleep_seconds / 3600
        logger.info(f"Next brief in {hours_until:.1f} hours at {target_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Sleep until target time
        await asyncio.sleep(sleep_seconds)

        # Execute the brief
        try:
            logger.info("Executing scheduled morning brief...")
            await send_brief()
            logger.info("Morning brief completed successfully")
        except Exception as e:
            logger.error(f"Brief execution failed: {e}", exc_info=True)

        # Sleep 65 seconds to avoid double-triggering if timing is exact
        await asyncio.sleep(65)


if __name__ == "__main__":
    try:
        asyncio.run(run_at_scheduled_time())
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}", exc_info=True)
