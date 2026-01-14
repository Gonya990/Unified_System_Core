import os
import json
import time
import hashlib
import requests
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load Environment
load_dotenv()

logger = logging.getLogger("MetaCAPI")
logging.basicConfig(level=logging.INFO)


class MetaCAPIService:
    """
    Secure Server-Side Tracking for AI Documentary Factory.
    Implements 'Digital Sovereignty' by filtering PII before sending events.
    """

    API_VERSION = "v19.0"
    BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

    def __init__(self):
        self.pixel_id = os.getenv("META_PIXEL_ID")
        self.access_token = os.getenv("META_ACCESS_TOKEN")

        if not self.pixel_id or not self.access_token:
            logger.warning("⚠️ Meta Pixel ID or Access Token missing in .env. CAPI tracking disabled.")
            self.enabled = False
        else:
            self.enabled = True
            logger.info(f"✅ Meta CAPI initialized for Pixel ID: {self.pixel_id}")

    def _hash_data(self, data: str) -> str:
        """SHA-256 hashing for user data normalization (email, phone)."""
        if not data:
            return None
        return hashlib.sha256(data.strip().lower().encode("utf-8")).hexdigest()

    def send_event(self, event_name: str, user_data: Dict[str, Any], custom_data: Optional[Dict] = None):
        """
        Sends a filtered server-side event to Meta.

        Args:
            event_name: 'ViewContent', 'Lead', 'Purchase', etc.
            user_data: Dict containing 'email', 'phone', 'ip_address', 'user_agent'.
                       SENSITIVE DATA IS HASHED LOCALLY.
            custom_data: Additional event parameters (value, currency).
        """
        if not self.enabled:
            return

        # 1. FILTER & HASH PII (Privacy First)
        # We never send raw emails or phones. Only hashes.
        formatted_user_data = {
            "client_ip_address": user_data.get("ip_address"),
            "client_user_agent": user_data.get("user_agent"),
            "em": [self._hash_data(user_data.get("email"))] if user_data.get("email") else None,
            "ph": [self._hash_data(user_data.get("phone"))] if user_data.get("phone") else None,
        }

        # Remove None values
        formatted_user_data = {k: v for k, v in formatted_user_data.items() if v is not None}

        payload = {
            "data": [
                {
                    "event_name": event_name,
                    "event_time": int(time.time()),
                    "action_source": "website",
                    "user_data": formatted_user_data,
                    "custom_data": custom_data or {},
                }
            ],
            "access_token": self.access_token,
        }

        try:
            url = f"{self.BASE_URL}/{self.pixel_id}/events"
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                logger.info(f"🚀 Event '{event_name}' sent successfully to Meta.")
            else:
                logger.error(f"❌ Failed to send event: {response.text}")

        except Exception as e:
            logger.error(f"❌ CAPI Exception: {e}")


if __name__ == "__main__":
    # Test Run
    service = MetaCAPIService()
    if service.enabled:
        service.send_event(
            event_name="TestEvent",
            user_data={"ip_address": "127.0.0.1", "user_agent": "TestAgent/1.0"},
            custom_data={"status": "sovereign_check_passed"},
        )
    else:
        print("Please set META_PIXEL_ID and META_ACCESS_TOKEN in .env to test.")
