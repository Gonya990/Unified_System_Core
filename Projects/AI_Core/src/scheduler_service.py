"""
Scheduler Service for AI Telegram Bot.
Handles scheduled tasks and reminders using APScheduler.
"""

import logging
from datetime import datetime

from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self, db_path: str = "sqlite:///jobs.db"):
        self.jobstores = {"default": SQLAlchemyJobStore(url=db_path), "memory": MemoryJobStore()}
        self.scheduler = AsyncIOScheduler(jobstores=self.jobstores)
        self.application = None  # Will hold Telegram Application instance

    def set_application(self, application: Application):
        self.application = application

    def start(self):
        """Start the scheduler."""
        try:
            self.scheduler.start()
            logger.info("Scheduler started")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")

    async def send_reminder(self, chat_id: int, text: str):
        """Callback function to send reminder."""
        if not self.application:
            logger.error("Application not set for scheduler")
            return

        try:
            await self.application.bot.send_message(
                chat_id=chat_id, text=f"⏰ **Напоминание!**\n\n{text}", parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Failed to send reminder to {chat_id}: {e}")

    def add_reminder(self, chat_id: int, text: str, run_date: datetime):
        """Schedule a one-time reminder."""
        try:
            self.scheduler.add_job(
                self.send_reminder, "date", run_date=run_date, args=[chat_id, text], misfire_grace_time=3600
            )
            return True
        except Exception as e:
            logger.error(f"Failed to add reminder: {e}")
            return False

    def add_daily_digest_job(self, chat_id: int, digest_callback, user_id: int, username: str):
        """Schedule daily digest at 09:00."""
        try:
            job_id = f"digest_{chat_id}"

            # Wrapper to call the async digest generation and sending
            async def send_digest():
                if not self.application:
                    return
                try:
                    text = await digest_callback(user_id, username)
                    await self.application.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
                except Exception as e:
                    logger.error(f"Failed to send digest: {e}")

            self.scheduler.add_job(
                send_digest,
                "cron",
                hour=9,
                minute=0,
                id=job_id,
                replace_existing=True,
                misfire_grace_time=3600,
                jobstore="memory",
            )
            logger.info(f"Scheduled daily digest for {username} at 09:00")
            return True
        except Exception as e:
            logger.error(f"Failed to schedule digest: {e}")
            return False
