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
    def __init__(self, application: Application, db: UserContextDB, inference=None):
        self.application = application
        self.db = db
        self.inference = inference
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
                
                # Get some context for a better nudge
                memories = self.db.get_memories(user_id, limit=3)
                mem_text = "\n".join([f"- {m['fact_full']}" for m in memories])
                
                if self.inference and mem_text:
                    prompt = (
                        f"The user {user['full_name']} hasn't interacted for 3 days. "
                        f"Here is what we know about them:\n{mem_text}\n\n"
                        "Generate a short, friendly nudge (1-2 sentences) to re-engage them, "
                        "referencing one of the facts if possible. Be professional yet warm."
                    )
                    nudge_text, _ = await self.inference.chat([{"role": "user", "content": prompt}], system_prompt="You are a helpful assistant.")
                else:
                    nudge_text = (
                        f"Hi {user['full_name']}! 👋 We haven't spoken in a few days. "
                        "Ready to resume our work or check your calendar?"
                    )

                await self.application.bot.send_message(chat_id=user_id, text=nudge_text)
                # Update last interaction so we don't spam
                self.db.update_last_interaction(user_id)
                logger.info(f"Sent contextual nudge to user {user_id}")
            except Exception as e:
                logger.error(f"Failed to nudge user {user['user_id']}: {e}")

    async def check_upcoming_events(self):
        """Logic to remind about upcoming events (e.g., in 15 mins)."""
        # This implementation requires scanning all connected users' calendars.
        # In a real system, we'd have a more efficient way to track this.
        # For small scale, we can iterate.
        pass
