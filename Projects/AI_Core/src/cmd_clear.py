"""
/clear command handler - clears conversation history
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


@require_auth  # noqa: F821
async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command - clear conversation history."""
    user_id = update.effective_user.id

    if conv_manager.clear_history(user_id):  # noqa: F821
        await update.message.reply_text("🧹 История диалогов очищена!\n\nСледующее сообщение начнёт новый контекст.")
        logger.info(f"Cleared conversation history for user {user_id}")
    else:
        await update.message.reply_text("ℹ️ История диалогов уже пуста.")
