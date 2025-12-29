"""
Gmail Integration Client
Provides read access to Gmail for the AI Bot.
"""
import os
import pickle
import logging
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Gmail dependencies not installed: {e}")
    GMAIL_AVAILABLE = False

# If modifying these scopes, delete the token.pickle file
# If modifying these scopes, delete the token.pickle file
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'openid']

class GmailClient:
    """Client for reading Gmail messages."""
    
    def __init__(self, credentials_path: str = None, token_path: str = None):
        self.service = None
        self.authenticated = False
        
        if not GMAIL_AVAILABLE:
            logger.warning("Gmail client not available - missing dependencies")
            return
            
        # Default paths
        config_dir = Path(__file__).parent.parent / "config"
        self.credentials_path = credentials_path or str(config_dir / "gmail_credentials.json")
        self.token_path = token_path or str(config_dir / "gmail_token_v2.pickle") # Force re-auth for new scopes
        
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API."""
        if not os.path.exists(self.credentials_path):
            logger.warning(f"Gmail credentials not found at {self.credentials_path}")
            return
            
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                try:
                    creds = pickle.load(token)
                except Exception:
                    logger.warning("Failed to load existing token, will re-auth")
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Failed to refresh token: {e}")
                    creds = None
            
            if not creds:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    # Security Bundle: Request auth_time in ID Token
                    creds = flow.run_local_server(
                        port=0,
                        claims='{"id_token":{"auth_time":{"essential":true}}}'
                    )
                except Exception as e:
                    logger.error(f"Gmail authentication failed: {e}")
                    return
            
            # Save the credentials for next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            self.authenticated = True
            logger.info("Gmail client authenticated successfully")
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
    
    def get_unread_count(self) -> int:
        """Get count of unread emails."""
        if not self.authenticated:
            return -1
            
        try:
            results = self.service.users().messages().list(
                userId='me', 
                labelIds=['INBOX', 'UNREAD'],
                maxResults=1
            ).execute()
            return results.get('resultSizeEstimate', 0)
        except Exception as e:
            logger.error(f"Failed to get unread count: {e}")
            return -1
    
    def get_recent_emails(self, max_results: int = 10, unread_only: bool = False) -> List[Dict]:
        """Get recent emails from inbox."""
        if not self.authenticated:
            return []
            
        try:
            labels = ['INBOX']
            if unread_only:
                labels.append('UNREAD')
                
            results = self.service.users().messages().list(
                userId='me',
                labelIds=labels,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for msg in messages:
                msg_data = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()
                
                headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
                
                emails.append({
                    'id': msg['id'],
                    'from': headers.get('From', 'Unknown'),
                    'subject': headers.get('Subject', 'No Subject'),
                    'date': headers.get('Date', ''),
                    'snippet': msg_data.get('snippet', '')[:100],
                    'unread': 'UNREAD' in msg_data.get('labelIds', [])
                })
            
            return emails
            
        except Exception as e:
            logger.error(f"Failed to get emails: {e}")
            return []
    
    def get_email_summary(self) -> str:
        """Get a formatted summary of recent emails."""
        if not self.authenticated:
            return "❌ Gmail не подключен. Требуется авторизация."
        
        unread = self.get_unread_count()
        emails = self.get_recent_emails(max_results=5, unread_only=True)
        
        if unread == 0:
            return "📭 Нет непрочитанных писем."
        
        summary = f"📧 **Непрочитанных писем: {unread}**\n\n"
        
        for email in emails:
            # Parse sender name
            sender = email['from']
            if '<' in sender:
                sender = sender.split('<')[0].strip().strip('"')
            
            status = "🔵" if email['unread'] else "⚪"
            summary += f"{status} **{sender}**\n"
            summary += f"   {email['subject'][:50]}...\n\n"
        
        return summary
    
    def search_emails(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search emails with Gmail query syntax."""
        if not self.authenticated:
            return []
            
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for msg in messages:
                msg_data = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()
                
                headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
                
                emails.append({
                    'id': msg['id'],
                    'from': headers.get('From', 'Unknown'),
                    'subject': headers.get('Subject', 'No Subject'),
                    'date': headers.get('Date', ''),
                    'snippet': msg_data.get('snippet', '')[:100]
                })
            
            return emails
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
