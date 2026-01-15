#!/usr/bin/env python3
"""
Entry point for the AI Telegram Bot (Unified System).
Redirects to the latest version of the bot implementation.
"""

import sys
import os
from dotenv import load_dotenv

# Ensure we can import modules from src
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Explicitly load .env from project root to ensure we get the right config
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, ".env")
print(f"[BOOT] Loading environment from {env_path}")
load_dotenv(env_path, override=True)

# Debug print (masked)
token = os.environ.get("TELEGRAM_BOT_TOKEN", "NOT_SET")
print(f"[BOOT] Token loaded: {token[:5]}...{token[-5:] if len(token) > 10 else ''}")

from ai_telegram_bot_v2 import main

if __name__ == "__main__":
    main()
