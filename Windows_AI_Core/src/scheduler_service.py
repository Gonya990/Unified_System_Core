"""
Scheduler Service for AI Telegram Bot.
Handles scheduled tasks and reminders using APScheduler.
"""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
from telegram.ext import Application
import asyncio

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, db_path: str = "sqlite:///jobs.db"):
        self.jobstores = {
            'default': SQLAlchemyJobStore(url=db_path)
        }
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
            await self.application.bot.send_message(chat_id=chat_id, text=f"⏰ **Напоминание!**\n\n{text}", parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Failed to send reminder to {chat_id}: {e}")

    def add_reminder(self, chat_id: int, text: str, run_date: datetime):
        """Schedule a one-time reminder."""
        try:
            self.scheduler.add_job(
                self.send_reminder,
                'date',
                run_date=run_date,
                args=[chat_id, text],
                misfire_grace_time=3600
            )
            return True
        except Exception as e:
            logger.error(f"Failed to add reminder: {e}")
            return False
