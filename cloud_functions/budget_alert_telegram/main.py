import base64
import json
import os
import urllib.request
import urllib.parse

def send_telegram_message(chat_id: int, text: str, bot_token: str) -> bool:
    """Send message to Telegram chat"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }).encode()
    
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except Exception as e:
        print(f"Failed to send to {chat_id}: {e}")
        return False


def budget_alert_to_telegram(event, context):
    """
    Cloud Function triggered by Pub/Sub budget alerts.
    
    DISABLED: Notifications turned off per user request
    """
    import logging
    logging.info("Budget alert received but notifications disabled per user request")
    logging.info(f"Event data: {event.get('data', 'N/A')}")
    return "Notifications disabled", 200

    """
    Cloud Function triggered by Pub/Sub budget alert.
    Forwards budget notifications to Telegram.
    """
    # Get config from environment
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_ids_str = os.environ.get("TELEGRAM_CHAT_IDS", "708531393,1881720235")
    chat_ids = [int(x.strip()) for x in chat_ids_str.split(",")]
    
    if not bot_token:
        print("ERROR: TELEGRAM_BOT_TOKEN not set")
        return "Missing bot token", 500
    
    # Decode Pub/Sub message
    try:
        pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
        alert_data = json.loads(pubsub_message)
    except Exception as e:
        print(f"Failed to parse message: {e}")
        return f"Parse error: {e}", 400
    
    # Extract budget info
    budget_name = alert_data.get("budgetDisplayName", "Unknown Budget")
    cost_amount = alert_data.get("costAmount", 0)
    budget_amount = alert_data.get("budgetAmount", 0)
    threshold = alert_data.get("alertThresholdExceeded", 0)
    currency = alert_data.get("currencyCode", "ILS")
    
    # Calculate percentage
    if budget_amount > 0:
        percentage = (cost_amount / budget_amount) * 100
    else:
        percentage = 0
    
    # Determine urgency emoji
    if percentage >= 100:
        emoji = "🚨"
        urgency = "ПРЕВЫШЕН"
    elif percentage >= 90:
        emoji = "⚠️"
        urgency = "КРИТИЧЕСКИЙ"
    elif percentage >= 50:
        emoji = "📊"
        urgency = "ВНИМАНИЕ"
    else:
        # Skip alert if 0% usage to avoid spam
        if percentage == 0:
            print("Budget is 0%, skipping notification")
            return "Skipped (0%)", 200
            
        emoji = "ℹ️"
        urgency = "ИНФОРМАЦИЯ"
    
    # Format message
    message = f"""
{emoji} <b>GCP Budget Alert - {urgency}</b>

<b>Бюджет:</b> {budget_name}
<b>Потрачено:</b> {currency} {cost_amount:.2f} / {budget_amount:.2f}
<b>Процент:</b> {percentage:.1f}%
<b>Порог:</b> {threshold * 100:.0f}%

{"⚡ <b>РЕКОМЕНДАЦИЯ:</b> Переключайтесь на локальные ресурсы (Ollama)!" if percentage >= 50 else ""}
"""
    
    # Send to all chat IDs
    success_count = 0
    for chat_id in chat_ids:
        if send_telegram_message(chat_id, message.strip(), bot_token):
            success_count += 1
            print(f"Sent alert to chat {chat_id}")
    
    return f"Sent to {success_count}/{len(chat_ids)} chats", 200
