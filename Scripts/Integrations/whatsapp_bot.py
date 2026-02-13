#!/usr/bin/env python3
"""
WhatsApp Cloud API Integration
Business messaging bot using Meta's WhatsApp Cloud API
https://developers.facebook.com/docs/whatsapp/cloud-api

Setup:
1. Create Meta Developer account: https://developers.facebook.com
2. Create Business App and add WhatsApp product
3. Get Phone Number ID and Access Token
4. Set environment variables: WHATSAPP_TOKEN, WHATSAPP_PHONE_ID
"""

import json
import logging
import os

import requests
from flask import Flask, jsonify, request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WhatsAppBot")

# Configuration
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "unified_system_verify")
WHATSAPP_API_VERSION = "v21.0"
WHATSAPP_API_URL = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_ID}/messages"


class WhatsAppClient:
    """
    WhatsApp Cloud API Client

    Usage:
        client = WhatsAppClient()
        client.send_text("972501234567", "Hello from Unified System!")
    """

    def __init__(self, token: str = None, phone_id: str = None):
        self.token = token or WHATSAPP_TOKEN
        self.phone_id = phone_id or WHATSAPP_PHONE_ID
        self.api_url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{self.phone_id}/messages"

        if not self.token or not self.phone_id:
            logger.warning("WhatsApp credentials not configured!")

    def _make_request(self, payload: dict) -> dict:
        """Make API request to WhatsApp"""
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            data = response.json()

            if response.status_code != 200:
                logger.error(f"WhatsApp API error: {data}")
                return {"error": data.get("error", {}).get("message", "Unknown error")}

            return data
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return {"error": str(e)}

    def send_text(self, to: str, message: str, preview_url: bool = False) -> dict:
        """
        Send a text message

        Args:
            to: Recipient phone number (with country code, no +)
            message: Text message content
            preview_url: Whether to enable URL preview
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"preview_url": preview_url, "body": message},
        }
        return self._make_request(payload)

    def send_template(self, to: str, template_name: str, language: str = "en_US", components: list = None) -> dict:
        """
        Send a template message (required for first contact)

        Args:
            to: Recipient phone number
            template_name: Approved template name
            language: Template language code
            components: Template components (header, body, buttons)
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {"name": template_name, "language": {"code": language}},
        }

        if components:
            payload["template"]["components"] = components

        return self._make_request(payload)

    def send_image(self, to: str, image_url: str, caption: str = None) -> dict:
        """Send an image message"""
        payload = {"messaging_product": "whatsapp", "to": to, "type": "image", "image": {"link": image_url}}
        if caption:
            payload["image"]["caption"] = caption

        return self._make_request(payload)

    def send_document(self, to: str, document_url: str, filename: str, caption: str = None) -> dict:
        """Send a document"""
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "document",
            "document": {"link": document_url, "filename": filename},
        }
        if caption:
            payload["document"]["caption"] = caption

        return self._make_request(payload)

    def send_buttons(self, to: str, body: str, buttons: list, header: str = None, footer: str = None) -> dict:
        """
        Send interactive button message

        Args:
            to: Recipient phone
            body: Message body
            buttons: List of button dicts with 'id' and 'title'
            header: Optional header text
            footer: Optional footer text
        """
        interactive = {
            "type": "button",
            "body": {"text": body},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": b["id"], "title": b["title"]}}
                    for b in buttons[:3]  # Max 3 buttons
                ]
            },
        }

        if header:
            interactive["header"] = {"type": "text", "text": header}
        if footer:
            interactive["footer"] = {"text": footer}

        payload = {"messaging_product": "whatsapp", "to": to, "type": "interactive", "interactive": interactive}

        return self._make_request(payload)

    def mark_as_read(self, message_id: str) -> dict:
        """Mark a message as read"""
        payload = {"messaging_product": "whatsapp", "status": "read", "message_id": message_id}
        return self._make_request(payload)


# Flask webhook server
app = Flask(__name__)
client = WhatsAppClient()


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """Webhook verification for Meta"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified!")
        return challenge, 200

    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    """Handle incoming WhatsApp messages"""
    data = request.get_json()

    try:
        # Extract message data
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        for message in messages:
            msg_id = message.get("id")
            from_number = message.get("from")
            msg_type = message.get("type")
            message.get("timestamp")

            logger.info(f"Received {msg_type} from {from_number}")

            # Mark as read
            client.mark_as_read(msg_id)

            # Handle different message types
            if msg_type == "text":
                text = message.get("text", {}).get("body", "")
                handle_text_message(from_number, text)

            elif msg_type == "button":
                button_id = message.get("button", {}).get("payload", "")
                handle_button_click(from_number, button_id)

            elif msg_type == "interactive":
                button_reply = message.get("interactive", {}).get("button_reply", {})
                handle_button_click(from_number, button_reply.get("id", ""))

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return jsonify({"error": str(e)}), 500


def handle_text_message(from_number: str, text: str):
    """Process incoming text messages"""
    text_lower = text.lower().strip()

    # Simple command handling
    if text_lower in ["hi", "hello", "привет", "שלום"]:
        client.send_text(from_number, "👋 Hello! I'm the Unified System Bot. How can I help you today?")
        client.send_buttons(
            to=from_number,
            body="Choose an option:",
            buttons=[
                {"id": "status", "title": "📊 System Status"},
                {"id": "help", "title": "❓ Help"},
                {"id": "contact", "title": "📞 Contact"},
            ],
        )

    elif text_lower == "status":
        client.send_text(from_number, "✅ All systems operational!\n\n📡 Uptime: 99.9%\n🔋 Load: Normal")

    elif text_lower == "help":
        client.send_text(
            from_number,
            """
*Available Commands:*
• status - Check system status
• help - Show this message
• search <query> - Web search
• notify - Set up notifications

Type any question to get AI assistance!
""",
        )

    else:
        # Default: AI response (integrate with your AI system)
        client.send_text(from_number, f"🤖 Processing your request: '{text}'\n\nI'll get back to you shortly!")


def handle_button_click(from_number: str, button_id: str):
    """Handle button click responses"""
    if button_id == "status":
        handle_text_message(from_number, "status")
    elif button_id == "help":
        handle_text_message(from_number, "help")
    elif button_id == "contact":
        client.send_text(from_number, "📧 Email: support@example.com\n📱 Phone: +1234567890")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        # Run webhook server
        logger.info("Starting WhatsApp webhook server on port 5000...")
        app.run(host="0.0.0.0", port=5000, debug=True)

    elif len(sys.argv) > 2 and sys.argv[1] == "send":
        # Send a test message
        phone = sys.argv[2]
        message = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "Hello from Unified System!"

        result = client.send_text(phone, message)
        print(json.dumps(result, indent=2))

    else:
        print("""
WhatsApp Cloud API Bot

Usage:
    python whatsapp_bot.py serve              # Start webhook server
    python whatsapp_bot.py send <phone> <msg> # Send test message

Environment variables required:
    WHATSAPP_TOKEN     - Meta access token
    WHATSAPP_PHONE_ID  - Your phone number ID
    WHATSAPP_VERIFY_TOKEN - Webhook verification token (optional)

Setup:
    1. Create app at https://developers.facebook.com
    2. Add WhatsApp product
    3. Get credentials from WhatsApp settings
    4. Configure webhook URL pointing to /webhook
""")
