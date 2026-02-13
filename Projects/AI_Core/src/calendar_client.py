"""
Google Calendar Client
Integrates with Google Calendar API using OAuth 2.0 credentials.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class CalendarClient:
    """Client for Google Calendar API per user."""

    def __init__(self, credentials_json: str = None, credentials_dict: dict = None):
        """
        Initialize with user credentials.
        :param credentials_json: JSON string of credentials
        :param credentials_dict: Dictionary of credentials
        """
        self.service = None
        self.creds = None

        try:
            if credentials_dict:
                self.creds = Credentials.from_authorized_user_info(credentials_dict)
            elif credentials_json:
                # Assuming credentials_json is a JSON string compatible with from_authorized_user_info
                import json

                info = json.loads(credentials_json)
                self.creds = Credentials.from_authorized_user_info(info)

            if self.creds:
                self.service = build("calendar", "v3", credentials=self.creds)
                logger.debug("Calendar service initialized with OAuth credentials")
            else:
                logger.warning("No credentials provided to CalendarClient")

        except Exception as e:
            logger.error(f"Failed to initialize Calendar service: {e}")

    def is_valid(self) -> bool:
        return self.service is not None

    def get_upcoming_events(self, days: int = 7) -> list[dict]:
        """Get upcoming events for next N days."""
        if not self.service:
            return []

        try:
            now = datetime.utcnow().isoformat() + "Z"
            end = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"

            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    timeMax=end,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            return events_result.get("items", [])
        except Exception as e:
            logger.error(f"Failed to fetch upcoming events: {e}")
            return []

    def format_event(self, event: dict) -> str:
        """Format event for display."""
        start = event["start"].get("dateTime", event["start"].get("date"))
        summary = event.get("summary", "No Title")

        # Parse time
        try:
            if "T" in start:  # DateTime
                dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                time_str = dt.strftime("%H:%M")
            else:  # All-day event
                time_str = "All Day"
        except Exception:
            time_str = "?"

        return f"{time_str} - {summary}"

    def create_event(
        self, summary: str, start_time: datetime, duration_minutes: int = 60, description: str = ""
    ) -> Optional[dict]:
        """
        Create a new calendar event.
        """
        if not self.service:
            logger.error("Calendar service not initialized")
            return None

        try:
            duration_minutes = int(str(duration_minutes).split()[0])
        except (ValueError, TypeError, IndexError):
            logger.warning(f"Invalid duration_minutes: {duration_minutes}, defaulting to 60")
            duration_minutes = 60

        try:
            end_time = start_time + timedelta(minutes=duration_minutes)

            # Use Israel timezone (configurable via TZ env var)
            import os

            user_tz = os.environ.get("TZ", "Asia/Jerusalem")

            event = {
                "summary": summary,
                "description": description,
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": user_tz,
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": user_tz,
                },
            }

            created_event = self.service.events().insert(calendarId="primary", body=event).execute()

            logger.info(f"Created event: {created_event.get('htmlLink')}")
            return created_event
        except Exception as e:
            logger.error(f"Failed to create event: {e}")
            return None
