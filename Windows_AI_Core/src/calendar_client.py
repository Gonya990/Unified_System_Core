import os
import logging
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

# Scopes required for calendar access
SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarClient:
    """Client for Google Calendar API with OAuth support."""
    
    def __init__(self):
        self.creds = None
        self.service = None
        self.calendar_id = 'primary'
        
        self.credentials_path = "credentials.json"
        self.token_path = "token.pickle"
        
        self.authenticate()

    def authenticate(self):
        """Authenticate with Google Calendar API."""
        try:
            # Load existing token
            if os.path.exists(self.token_path):
                with open(self.token_path, 'rb') as token:
                    self.creds = pickle.load(token)
            
            # Refresh or create new token
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if os.path.exists(self.credentials_path):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_path, SCOPES)
                        # This might require a browser flow, which is tricky on a headless server
                        # Ideally, this runs once locally to generate token.pickle
                        logger.warning("Need to authenticate via browser. Credentials found but no valid token.")
                        # self.creds = flow.run_local_server(port=0)
                    else:
                        logger.warning("No credentials.json found.")
                        return

                # Save the credentials for the next run
                if self.creds:
                    with open(self.token_path, 'wb') as token:
                        pickle.dump(self.creds, token)

            # Build service
            if self.creds:
                self.service = build('calendar', 'v3', credentials=self.creds)
                logger.info("Calendar service initialized successfully with OAuth")
        except Exception as e:
            logger.error(f"Failed to authenticate Calendar: {e}")

    def get_today_events(self) -> List[Dict]:
        """Get today's events."""
        if not self.service:
            return []
        
        try:
            now = datetime.utcnow()
            # Start of day
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=0)
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start.isoformat() + 'Z',
                timeMax=end.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except Exception as e:
            logger.error(f"Failed to fetch today events: {e}")
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
        
        try:
            # Helper to parse ISO format
            if 'T' in start:
                dt = datetime.fromisoformat(str(start).replace('Z', '+00:00'))
                # Localize if needed, for simplicity show time
                time_str = dt.strftime('%H:%M')
            else:
                time_str = "Весь день"
        except:
            time_str = "?"
            
        return f"{time_str} - {summary}"

    def create_event(self, summary: str, start_time: datetime, duration_minutes: int = 60) -> Optional[Dict]:
        """Create a new calendar event."""
        if not self.service:
            logger.error("Service not initialized")
            return None
            
        try:
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            event = {
                'summary': summary,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC', # Consider using user's timezone
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event
            ).execute()
            
            logger.info(f"Created event: {created_event.get('htmlLink')}")
            return created_event
        except Exception as e:
            logger.error(f"Failed to create event: {e}")
            return None
