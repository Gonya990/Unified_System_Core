#!/usr/bin/env python3
"""
Entry point for the AI Telegram Bot (Unified System).
Redirects to the latest version of the bot implementation.
"""

import os
import sys

from dotenv import load_dotenv

# Ensure we can import modules from src
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Determine which .env file to load
env_file = os.environ.get("ENV_FILE", ".env")

# Check command line for --env override
for i, arg in enumerate(sys.argv):
    if arg == "--env" and i + 1 < len(sys.argv):
        env_file = sys.argv[i + 1]
        break

project_root = os.path.dirname(current_dir)
if os.path.isabs(env_file):
    env_path = env_file
else:
    env_path = os.path.join(project_root, env_file)

print(f"[BOOT] Loading environment from {env_path}")
load_dotenv(env_path, override=True)

# Debug print (masked)
token = os.environ.get("TELEGRAM_BOT_TOKEN", "NOT_SET")
print(f"[BOOT] Token loaded: {token[:5]}...{token[-5:] if len(token) > 10 else ''}")

from ai_telegram_bot_v2 import main

if __name__ == "__main__":
    main()
