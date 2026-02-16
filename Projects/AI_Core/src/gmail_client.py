"""
Gmail Integration Client
Provides read and compose access to Gmail for the AI Bot.
Uses unified OAuth credentials from Firestore (same as Calendar).
"""

import base64
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

logger = logging.getLogger(__name__)

# Gmail API imports
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    GMAIL_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Gmail dependencies not installed: {e}")
    GMAIL_AVAILABLE = False


class GmailClient:
    """Client for Gmail API - read and compose emails."""

    def __init__(self, credentials_dict: dict = None):
        """
        Initialize with OAuth credentials (same format as CalendarClient).
        :param credentials_dict: Dictionary of OAuth credentials from Firestore
        """
        self.service = None
        self.authenticated = False
        self.user_email = None

        if not GMAIL_AVAILABLE:
            logger.warning("Gmail client not available - missing dependencies")
            return

        try:
            if credentials_dict:
                self.creds = Credentials.from_authorized_user_info(credentials_dict)
                self.service = build("gmail", "v1", credentials=self.creds)

                # Verify and get user's email address
                profile = self.service.users().getProfile(userId="me").execute()
                self.user_email = profile.get("emailAddress")
                self.authenticated = True
                logger.debug(f"Gmail service initialized for {self.user_email}")
            else:
                logger.warning("No credentials provided to GmailClient")
        except Exception as e:
            self.authenticated = False
            logger.error(f"Failed to initialize Gmail service: {e}")

    def is_valid(self) -> bool:
        return self.service is not None and self.authenticated

    def get_unread_count(self) -> int:
        """Get count of unread emails."""
        if not self.authenticated:
            return 0

        try:
            results = (
                self.service.users().messages().list(userId="me", labelIds=["UNREAD"], maxResults=1).execute()
            )
            # resultSizeEstimate is often an estimate, totalEstimate is more reliable in newer API
            return results.get("resultSizeEstimate", 0)
        except Exception as e:
            logger.error(f"Failed to get unread count for {self.user_email}: {e}")
            if "deleted_client" in str(e):
                self.authenticated = False # Force re-auth
            return 0

    def get_recent_emails(self, max_results: int = 10, unread_only: bool = False) -> list[dict]:
        """Get recent emails from inbox."""
        if not self.authenticated:
            return []

        try:
            labels = ["INBOX"]
            if unread_only:
                labels.append("UNREAD")

            results = (
                self.service.users().messages().list(userId="me", labelIds=labels, maxResults=max_results).execute()
            )

            messages = results.get("messages", [])
            emails = []

            for msg in messages:
                msg_data = (
                    self.service.users()
                    .messages()
                    .get(
                        userId="me", id=msg["id"], format="metadata", metadataHeaders=["From", "Subject", "Date", "To"]
                    )
                    .execute()
                )

                headers = {h["name"]: h["value"] for h in msg_data.get("payload", {}).get("headers", [])}

                emails.append(
                    {
                        "id": msg["id"],
                        "thread_id": msg_data.get("threadId"),
                        "from": headers.get("From", "Unknown"),
                        "to": headers.get("To", ""),
                        "subject": headers.get("Subject", "No Subject"),
                        "date": headers.get("Date", ""),
                        "snippet": msg_data.get("snippet", "")[:100],
                        "unread": "UNREAD" in msg_data.get("labelIds", []),
                    }
                )

            return emails

        except Exception as e:
            logger.error(f"Failed to get emails: {e}")
            return []

    def get_email_body(self, message_id: str) -> Optional[str]:
        """Get full email body by message ID."""
        if not self.authenticated:
            return None

        try:
            msg = self.service.users().messages().get(userId="me", id=message_id, format="full").execute()

            payload = msg.get("payload", {})
            body = self._extract_body(payload)
            return body
        except Exception as e:
            logger.error(f"Failed to get email body: {e}")
            return None

    def _extract_body(self, payload: dict) -> str:
        """Extract text body from email payload."""
        body = ""

        if "body" in payload and payload["body"].get("data"):
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")

        if "parts" in payload:
            for part in payload["parts"]:
                mime_type = part.get("mimeType", "")
                if mime_type == "text/plain":
                    if part["body"].get("data"):
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                        break
                elif mime_type.startswith("multipart/"):
                    body = self._extract_body(part)
                    if body:
                        break

        return body

    def get_email_summary(self) -> str:
        """Get a formatted summary of recent emails."""
        if not self.authenticated:
            return "❌ Gmail не подключен. Используйте /start для подключения Google."

        unread = self.get_unread_count()

        if unread == 0 and not self.authenticated:
            return "❌ Gmail не подключен. Используйте /start для подключения Google."

        if unread == 0:
            # Check if it was really 0 or an error that returned 0
            if not self.authenticated:
                return "❌ Ошибка авторизации Gmail. Пожалуйста, переподключите аккаунт через /start."
            return "📭 Нет непрочитанных писем."

        summary = f"📧 **Непрочитанных писем: {unread}**\n\n"

        for email in self.get_recent_emails(unread_only=True):
            # Parse sender name
            sender = email["from"]
            if "<" in sender:
                sender = sender.split("<")[0].strip().strip('"')

            status = "🔵" if email["unread"] else "⚪"
            subject = email["subject"][:50]
            if len(email["subject"]) > 50:
                subject += "..."
            summary += f"{status} **{sender}**\n"
            summary += f"   {subject}\n\n"

        return summary

    def search_emails(self, query: str, max_results: int = 10) -> list[dict]:
        """Search emails with Gmail query syntax."""
        if not self.authenticated:
            return []

        try:
            results = self.service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()

            messages = results.get("messages", [])
            emails = []

            for msg in messages:
                msg_data = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=msg["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"])
                    .execute()
                )

                headers = {h["name"]: h["value"] for h in msg_data.get("payload", {}).get("headers", [])}

                emails.append(
                    {
                        "id": msg["id"],
                        "from": headers.get("From", "Unknown"),
                        "subject": headers.get("Subject", "No Subject"),
                        "date": headers.get("Date", ""),
                        "snippet": msg_data.get("snippet", "")[:100],
                    }
                )

            return emails

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> Optional[dict]:
        """
        Send an email.
        :param to: Recipient email address
        :param subject: Email subject
        :param body: Email body (plain text or HTML)
        :param html: If True, body is treated as HTML
        :return: Sent message info or None on error
        """
        if not self.authenticated:
            logger.error("Cannot send email - not authenticated")
            return None

        try:
            if html:
                message = MIMEMultipart("alternative")
                message.attach(MIMEText(body, "html"))
            else:
                message = MIMEText(body)

            message["to"] = to
            message["subject"] = subject

            # Encode the message
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

            sent = self.service.users().messages().send(userId="me", body={"raw": raw}).execute()

            logger.info(f"Email sent to {to}, message ID: {sent.get('id')}")
            return sent
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return None

    def reply_to_email(self, message_id: str, body: str, html: bool = False) -> Optional[dict]:
        """
        Reply to an existing email.
        :param message_id: Original message ID to reply to
        :param body: Reply body
        :param html: If True, body is treated as HTML
        :return: Sent message info or None on error
        """
        if not self.authenticated:
            return None

        try:
            # Get original message for headers
            original = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="metadata", metadataHeaders=["From", "Subject", "Message-ID"])
                .execute()
            )

            headers = {h["name"]: h["value"] for h in original.get("payload", {}).get("headers", [])}

            # Build reply
            if html:
                message = MIMEMultipart("alternative")
                message.attach(MIMEText(body, "html"))
            else:
                message = MIMEText(body)

            # Extract email from "Name <email>" format
            from_header = headers.get("From", "")
            if "<" in from_header and ">" in from_header:
                to_email = from_header[from_header.find("<") + 1 : from_header.find(">")]
            else:
                to_email = from_header

            message["to"] = to_email
            subject = headers.get("Subject", "")
            if not subject.lower().startswith("re:"):
                subject = f"Re: {subject}"
            message["subject"] = subject
            message["In-Reply-To"] = headers.get("Message-ID", "")
            message["References"] = headers.get("Message-ID", "")

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

            sent = (
                self.service.users()
                .messages()
                .send(userId="me", body={"raw": raw, "threadId": original.get("threadId")})
                .execute()
            )

            logger.info(f"Reply sent to {to_email}, message ID: {sent.get('id')}")
            return sent
        except Exception as e:
            logger.error(f"Failed to reply to email: {e}")
            return None

    def mark_as_read(self, message_id: str) -> bool:
        """Mark email as read."""
        if not self.authenticated:
            return False

        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to mark as read: {e}")
            return False

    def mark_as_unread(self, message_id: str) -> bool:
        """Mark email as unread."""
        if not self.authenticated:
            return False

        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"addLabelIds": ["UNREAD"]}
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to mark as unread: {e}")
            return False

    def archive_email(self, message_id: str) -> bool:
        """Archive email (remove from INBOX)."""
        if not self.authenticated:
            return False

        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"removeLabelIds": ["INBOX"]}
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to archive email: {e}")
            return False

    def trash_email(self, message_id: str) -> bool:
        """Move email to trash."""
        if not self.authenticated:
            return False

        try:
            self.service.users().messages().trash(userId="me", id=message_id).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to trash email: {e}")
            return False

    def get_labels(self) -> list[dict]:
        """Get all Gmail labels."""
        if not self.authenticated:
            return []

        try:
            results = self.service.users().labels().list(userId="me").execute()
            return results.get("labels", [])
        except Exception as e:
            logger.error(f"Failed to get labels: {e}")
            return []
