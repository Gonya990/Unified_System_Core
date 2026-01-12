#!/usr/bin/env python3
"""
Scheduled token rotation for TokenBroker.
Runs as a standalone service or integrates with APScheduler.
"""

import logging
import os
import sys
import time
from pathlib import Path

import schedule

sys.path.insert(0, str(Path(__file__).parent))
from token_broker import TokenBroker

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ROTATION_INTERVAL_HOURS = int(os.getenv("TOKEN_ROTATION_HOURS", "24"))
RELOAD_INTERVAL_HOURS = int(os.getenv("TOKEN_RELOAD_HOURS", "6"))


def rotate_job():
    """Clear blacklist and reset rotation indices."""
    broker = TokenBroker()
    result = broker.rotate_keys()
    logger.info(f"Rotation complete: {result}")


def reload_job():
    """Reload keys from disk for hot-updates."""
    broker = TokenBroker()
    success = broker.reload_keys()
    logger.info(f"Reload {'succeeded' if success else 'failed'}")


def health_job():
    """Log health status."""
    broker = TokenBroker()
    health = broker.health_check()
    status = health.get("status", "unknown")
    active = health.get("active_keys", 0)
    blacklisted = health.get("blacklisted_keys", 0)
    logger.info(f"Health: {status} | Active: {active} | Blacklisted: {blacklisted}")


def run_scheduler():
    """Run the rotation scheduler as a standalone service."""
    logger.info("Starting TokenBroker rotation scheduler")
    logger.info(f"  Rotation interval: {ROTATION_INTERVAL_HOURS}h")
    logger.info(f"  Reload interval: {RELOAD_INTERVAL_HOURS}h")

    schedule.every(ROTATION_INTERVAL_HOURS).hours.do(rotate_job)
    schedule.every(RELOAD_INTERVAL_HOURS).hours.do(reload_job)
    schedule.every(1).hours.do(health_job)

    health_job()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run_scheduler()
