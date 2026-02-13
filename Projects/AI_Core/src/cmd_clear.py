"""
/clear command handler - clears conversation history
"""


@require_auth
async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command - clear conversation history."""
    user_id = update.effective_user.id

    if conv_manager.clear_history(user_id):
        await update.message.reply_text("🧹 История диалогов очищена!\n\nСледующее сообщение начнёт новый контекст.")
        logger.info(f"Cleared conversation history for user {user_id}")
    else:
        await update.message.reply_text("ℹ️ История диалогов уже пуста.")
