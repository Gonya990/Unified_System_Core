#!/usr/bin/env python3
"""
Entry point for the AI Telegram Bot (Unified System).
Redirects to the latest version of the bot implementation.
"""

import sys
import os

# Ensure we can import modules from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_telegram_bot_v2 import main

if __name__ == "__main__":
    main()
