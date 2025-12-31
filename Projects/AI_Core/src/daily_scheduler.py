import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from telegram.ext import Application
from user_context_db import UserContextDB
from calendar_client import CalendarClient
import json

logger = logging.getLogger(__name__)

class DailyScheduler:
    def __init__(self, application: Application, db: UserContextDB):
        self.application = application
        self.db = db
        self.running = False

    async def start(self):
        self.running = True
        logger.info("Daily Scheduler/Nudger started.")
        while self.running:
            try:
                await self.check_and_nudge()
                await self.check_upcoming_events()
                # Check every hour
                await asyncio.sleep(3600)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(60)

    async def stop(self):
        self.running = False

    async def check_and_nudge(self):
        """Find users who haven't talked in 3 days and send a nudge."""
        inactive_users = self.db.get_inactive_users(hours=72)
        for user in inactive_users:
            try:
                user_id = user['user_id']
                # Don't nudge if we nudged recently (store nudge state in KV or another table)
                # For now, just a simple nudge
                nudge_text = (
                    f"Hi {user['full_name']}! 👋 We haven't spoken in a few days. "
                    "Ready to resume our work or check your calendar?"
                )
                await self.application.bot.send_message(chat_id=user_id, text=nudge_text)
                # Update last interaction so we don't spam
                self.db.update_last_interaction(user_id)
                logger.info(f"Sent nudge to user {user_id}")
            except Exception as e:
                logger.error(f"Failed to nudge user {user['user_id']}: {e}")

    async def check_upcoming_events(self):
        """Logic to remind about upcoming events (e.g., in 15 mins)."""
        # This implementation requires scanning all connected users' calendars.
        # In a real system, we'd have a more efficient way to track this.
        # For small scale, we can iterate.
        pass
