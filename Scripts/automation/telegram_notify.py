
import os
import requests
import logging

# Ensure logging is configured if run standalone
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("TelegramNotify")

def send_telegram_message(message, token=None, chat_id=None):
    """
    Send a message to Telegram.
    Uses provided arguments or falls back to environment variables.
    """
    # Load from env if not provided
    if not token:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not chat_id:
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.warning("Telegram token or chat_id not set. Skipping notification.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Simple truncation to avoid 400 errors (Telegram limit is 4096)
    if len(message) > 4000:
        message = message[:4000] + "\n...(truncated)"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        # Remove parse_mode="Markdown" to avoid 400 Bad Request on raw log data
        # or use "Markdown" only if we are sure it's safe. For logs, text is safer.
        # "parse_mode": "Markdown" 
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Telegram notification sent successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        # Try sending without payload text if it failed (maybe invalid chars)
        if "Bad Request" in str(e):
             try:
                 payload["text"] = "⚠️ Notification failed to render. Check server logs."
                 requests.post(url, json=payload, timeout=10)
             except:
                 pass
        return False

if __name__ == "__main__":
    # Test run
    from dotenv import load_dotenv, find_dotenv
    # Try to find .env in parent or specific locations
    load_dotenv(find_dotenv(usecwd=True)) 
    # Also look in Projects/AI_Core for dev setup
    load_dotenv("/Users/macbook/Documents/Unified_System/Projects/AI_Core/.env")
    
    send_telegram_message("🔔 Test notification from Job Hunter Agent")
