"""
Notification Manager for Smart Alerts
Handles quiet hours, priority levels, and user preferences.
"""
import logging
from datetime import datetime, time
from typing import Optional

from telegram import Bot
from telegram.constants import ParseMode

logger = logging.getLogger(__name__)

class NotificationManager:
    """Manages bot notifications with priority and quiet hours."""

    # Priority Levels
    CRITICAL = "critical"  # Always send (errors, security)
    HIGH = "high"         # Send except during quiet hours
    NORMAL = "normal"     # Send only during active hours
    LOW = "low"          # Batched, send once per day

    def __init__(self, quiet_start: time = time(23, 0), quiet_end: time = time(8, 0)):
        """
        Initialize notification manager.

        Args:
            quiet_start: Start of quiet hours (default 23:00)
            quiet_end: End of quiet hours (default 08:00)
        """
        self.quiet_start = quiet_start
        self.quiet_end = quiet_end
        self.low_priority_queue = []  # Queue for batched notifications

    def is_quiet_hours(self) -> bool:
        """Check if current time is within quiet hours."""
        now = datetime.now().time()

        # Handle overnight quiet hours (e.g., 23:00 - 08:00)
        if self.quiet_start > self.quiet_end:
            return now >= self.quiet_start or now < self.quiet_end
        else:
            return self.quiet_start <= now < self.quiet_end

    async def send(
        self,
        bot: Bot,
        chat_id: int,
        text: str,
        priority: str = NORMAL,
        parse_mode: Optional[str] = None,
        **kwargs
    ) -> bool:
        """
        Send notification respecting quiet hours and priority.

        Args:
            bot: Telegram Bot instance
            chat_id: Target chat ID
            text: Message text
            priority: Priority level (CRITICAL, HIGH, NORMAL, LOW)
            parse_mode: Telegram parse mode
            **kwargs: Additional arguments for send_message

        Returns:
            True if sent immediately, False if queued/skipped
        """
        quiet = self.is_quiet_hours()

        # CRITICAL: Always send
        if priority == self.CRITICAL:
            await bot.send_message(chat_id, f"🚨 {text}", parse_mode=parse_mode, **kwargs)
            return True

        # HIGH: Send if not quiet hours
        if priority == self.HIGH:
            if not quiet:
                await bot.send_message(chat_id, text, parse_mode=parse_mode, **kwargs)
                return True
            else:
                logger.info(f"HIGH priority message delayed due to quiet hours: {text[:50]}")
                return False

        # NORMAL: Send only during active hours
        if priority == self.NORMAL:
            if not quiet:
                await bot.send_message(chat_id, text, parse_mode=parse_mode, **kwargs)
                return True
            else:
                logger.info(f"NORMAL priority message skipped (quiet hours): {text[:50]}")
                return False

        # LOW: Queue for batch delivery
        if priority == self.LOW:
            self.low_priority_queue.append({
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "kwargs": kwargs
            })
            logger.info(f"LOW priority message queued: {text[:50]}")
            return False

        # Default: Send as NORMAL
        return await self.send(bot, chat_id, text, self.NORMAL, parse_mode, **kwargs)

    async def flush_low_priority(self, bot: Bot):
        """Send all queued low-priority notifications as a batch."""
        if not self.low_priority_queue:
            return

        # Group by chat_id
        batches = {}
        for msg in self.low_priority_queue:
            chat_id = msg["chat_id"]
            if chat_id not in batches:
                batches[chat_id] = []
            batches[chat_id].append(msg["text"])

        # Send batched messages
        for chat_id, messages in batches.items():
            batch_text = "📬 **Накопленные уведомления:**\n\n" + "\n\n".join(messages)
            await bot.send_message(chat_id, batch_text, parse_mode=ParseMode.MARKDOWN)

        # Clear queue
        self.low_priority_queue.clear()
        logger.info(f"Flushed {len(batches)} batched notifications")
