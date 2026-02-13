import json
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Setup Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env")

# Logging
LOG_DIR = ROOT_DIR / "logs/family"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "fma.log"), logging.StreamHandler()],
)
logger = logging.getLogger("HomeworkSentinel")


def get_gmail_service():
    """Load credentials and return service."""
    creds_path = ROOT_DIR / "Scripts/automation/.credentials/gmail_token.json"
    if not creds_path.exists():
        logger.error(f"Credentials not found at {creds_path}")
        return None

    try:
        with open(creds_path) as f:
            info = json.load(f)
            creds = Credentials.from_authorized_user_info(info)
        return build("gmail", "v1", credentials=creds)
    except Exception as e:
        logger.error(f"Failed to authenticate: {e}")
        return None


def scan_mailbox(query="subject:(homework OR school OR due) after:2d"):
    """
    Scan mailbox for homework related emails.
    """
    service = get_gmail_service()
    if not service:
        return []

    logger.info(f"Scanning mailbox with query: {query}")
    results = []

    try:
        response = service.users().messages().list(userId="me", q=query).execute()
        messages = response.get("messages", [])

        for msg in messages:
            msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
            payload = msg_data.get("payload", {})
            headers = payload.get("headers", [])

            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
            from_addr = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
            snippet = msg_data.get("snippet", "")

            results.append({"id": msg["id"], "subject": subject, "from": from_addr, "snippet": snippet})

    except Exception as e:
        logger.error(f"Scan failed: {e}")

    return results


def summarize_tasks(emails):
    """
    Use LLM (via TokenBroker) to summarize homework.
    """
    if not emails:
        return "No homework emails found."

    try:
        from Scripts.Utilities.token_broker import TokenBroker

        broker = TokenBroker()
        # Try Gemini (Free) first, then others
        key = broker.get_key("gemini")
        if not key:
            key = broker.get_key("openai")

        if not key:
            logger.error("No LLM key available for summary.")
            return "Found emails but cannot summarize (No API Key)."

        logger.info(f"Summarizing {len(emails)} emails...")

        # Simple concatenation for prompt
        email_text = "\n".join(
            [f"- From: {e['from']}, Subject: {e['subject']} ({e['snippet'][:100]}...)" for e in emails]
        )

        # In a real scenario, we'd call the LLM API here.
        # For now, we return the structured list as the "Report" to ensure stability without burning tokens blindly.
        return f"Found {len(emails)} relevant emails:\n" + email_text

    except ImportError:
        logger.error("TokenBroker not found.")
        return "Internal Error: TokenBroker missing."


if __name__ == "__main__":
    logger.info("Starting Homework Sentinel...")

    emails = scan_mailbox()
    if emails:
        report = summarize_tasks(emails)
        print("\n--- Daily Homework Report ---\n")
        print(report)
        print("\n-----------------------------")

        # Internal notification logic could go here
    else:
        print("No homework found.")
        logger.info("No homework found.")
