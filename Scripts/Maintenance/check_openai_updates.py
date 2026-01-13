#!/usr/bin/env python3
"""
OpenAI Feature Tracker
Checks OpenAI help pages for new features (specifically Google Drive integration).
Run this periodically (e.g., every 5 days via cron).
"""

import logging
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from Scripts.Utilities.telegram_notifier import TelegramNotifier

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("OpenAITracker")

# Config
TARGET_URL = "https://help.openai.com/en/collections/8471418-data-controls"
KEYWORDS = ["Google Drive", "Drive Integration", "Cloud Export", "Direct Export"]
STATE_FILE = Path(__file__).parent / "openai_tracker_state.txt"


def check_for_updates():
    """
    Checks the OpenAI help page for specific keywords.
    Note: Since Cloudflare protection is active, we might need to use the nodriver daemon or a browser.
    For this implementation, we will assume we can use the 'ndc' tool if available, or just log a reminder to check manually if automation fails.
    """
    logger.info("🔍 Checking OpenAI features...")

    # We will try to read the last known state
    last_state = ""
    if STATE_FILE.exists():
        last_state = STATE_FILE.read_text().strip()

    # Construct command to fetch page via nodriver (most reliable way given 403s on curl)
    import subprocess

    ndc_path = Path(__file__).resolve().parent.parent.parent / "External_Tools/nodriver/ndc"

    cmd = f'{ndc_path} goto "{TARGET_URL}" && sleep 5 && {ndc_path} js "return document.body.innerText"'

    try:
        # Run ndc command
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"Failed to fetch page: {result.stderr}")
            return

        content = result.stdout

        found_keywords = []
        for kw in KEYWORDS:
            if kw.lower() in content.lower():
                found_keywords.append(kw)

        if found_keywords:
            msg = f"🚀 **OpenAI Update Detected!**\nFound keywords: {', '.join(found_keywords)}\nCheck: {TARGET_URL}"
            logger.info(msg)

            # Send Telegram Alert
            TelegramNotifier.send_message(msg)

        else:
            logger.info("No target keywords found.")

        # Update state
        STATE_FILE.write_text(str(time.time()))

    except Exception as e:
        logger.error(f"Error during check: {e}")


if __name__ == "__main__":
    check_for_updates()
