"""
Google Calendar Client
Simplified integration for viewing and creating calendar events.
"""
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class CalendarClient:
    """Client for Google Calendar API."""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_CALENDAR_API_KEY")
        self.calendar_id = os.getenv("GOOGLE_CALENDAR_ID", "primary")
        self.service = None
        
        # Try to initialize service
        try:
            from googleapiclient.discovery import build
            
            if self.api_key:
                # API Key method (read-only, public calendars)
                self.service = build('calendar', 'v3', developerKey=self.api_key)
                logger.info("Calendar service initialized with API key")
            else:
                logger.warning("Google Calendar API key not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Calendar service: {e}")
    
    def get_today_events(self) -> List[Dict]:
        """Get today's events."""
        if not self.service:
            return []
        
        try:
            # Get events for today
            now = datetime.utcnow()
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
            end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_of_day,
                timeMax=end_of_day,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return events
        except Exception as e:
            logger.error(f"Failed to fetch calendar events: {e}")
            return []
    
    def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Get upcoming events for next N days."""
        if not self.service:
            return []
        
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            end = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=now,
                timeMax=end,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except Exception as e:
            logger.error(f"Failed to fetch upcoming events: {e}")
            return []
    
    def format_event(self, event: Dict) -> str:
        """Format event for display."""
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'No Title')
        
        # Parse time
        try:
            if 'T' in start:  # DateTime
                dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                time_str = dt.strftime('%H:%M')
            else:  # All-day event
                time_str = "Весь день"
        except:
            time_str = "?"
        
        return f"{time_str} - {summary}"
    
    def create_event(self, summary: str, start_time: datetime, duration_minutes: int = 60) -> Optional[Dict]:
        """
        Create a new calendar event.
        Note: Requires OAuth, not API key.
        """
        if not self.service:
            logger.error("Calendar service not initialized")
            return None
        
        try:
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            event = {
                'summary': summary,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Europe/Kiev',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Europe/Kiev',
                },
            }
            
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            
            return created_event
        except Exception as e:
            logger.error(f"Failed to create event: {e}")
            return None
