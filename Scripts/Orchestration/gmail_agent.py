#!/usr/bin/env python3
"""
Gmail Intelligence Agent - Background Service
Monitors Gmail for important notifications and dispatches tasks to agents.
Replaces noisy email notifications with smart Telegram alerts.
"""

import asyncio
import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta

import requests

# Add context for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, os.path.join(root_dir, "Projects", "AI_Core", "src"))

try:
    from agent_orchestrator import AgentOrchestrator
    from config_manager import ConfigManager
    from firestore_db import FirestoreDB
    from gmail_client import GmailClient
    from inference_client import InferenceClient
except ImportError as e:
    print(f"Failed to import dependencies: {e}")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("GmailAgent")


class GmailIntelligenceAgent:
    def __init__(self):
        self.config = ConfigManager()
        self.db = FirestoreDB()
        self.inference = InferenceClient(self.config)
        self.orchestrator = AgentOrchestrator(self.inference)
        self.gmail = None
        self.last_check_time = datetime.utcnow() - timedelta(minutes=10)
        self.poll_interval = 300  # 5 minutes

        # User ID to notify (Admin)
        # Default to Igor's ID if found
        self.admin_id = int(os.getenv("ADMIN_ID", "113113645"))

    async def initialize(self):
        """Initialize Gmail client using Admin's credentials."""
        admin_user = self.db.get_user(self.admin_id)
        if not admin_user or not admin_user.get("google_creds"):
            logger.error(
                f"Admin user {self.admin_id} " "not found or has no Google credentials."
            )
            return False

        creds_dict = json.loads(admin_user["google_creds"])
        self.gmail = GmailClient(creds_dict)

        if not self.gmail.is_valid():
            logger.error("GmailClient failed to initialize with credentials.")
            return False

        logger.info(f"GmailAgent initialized for {self.gmail.user_email}")
        return True

    def send_telegram(self, text):
        """Send a message via Telegram Bot API."""
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            logger.error("TELEGRAM_BOT_TOKEN not set")
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            resp = requests.post(
                url,
                json={"chat_id": self.admin_id, "text": text, "parse_mode": "Markdown"},
                timeout=10,
            )
            if resp.status_code != 200:
                logger.error(f"Telegram API error: {resp.text}")
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")

    async def process_email(self, email):
        """Analyze email and decide action."""
        subject = email.get("subject", "No Subject")
        sender = email.get("from", "Unknown")
        snippet = email.get("snippet", "")

        logger.info(f"Processing email: {subject} from {sender}")

        # Skip bot-generated "Bug" notifications that we've already handled
        if (
            "[BOT ERROR] Conflict" in subject
            or "terminated by other getUpdates" in snippet
        ):
            logger.info("Skipping known bot conflict notification.")
            return

        # 1. Use LLM to analyze the email
        prompt = f"""
Analyze the following email and determine if it requires immediate action
or can be handled by an AI agent.
Sender: {sender}
Subject: {subject}
Snippet: {snippet}

Available Agent Categories: {list(self.orchestrator.CATEGORIES.keys())}

Response format (JSON):
{{
  "priority": "low|medium|high",
  "category": "category_name_or_null",
  "summary": "one_sentence_summary",
  "action_required": true|false,
  "agent_instruction": "detailed_instruction_for_agent_or_null"
}}
"""
        try:
            response_text, _ = await self.inference.chat(
                [{"role": "user", "content": prompt}],
                system_prompt=(
                    "You are a Mail Intelligence Agent. Analyze and categorize."
                ),
            )

            # Extract JSON from response
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group(0))
            else:
                logger.warning(f"Failed to parse LLM response: {response_text}")
                analysis = {
                    "priority": "medium",
                    "action_required": True,
                    "summary": subject,
                }
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            analysis = {
                "priority": "medium",
                "action_required": True,
                "summary": subject,
            }

        if not analysis.get("action_required", True):
            logger.info(f"No action required for email: {subject}")
            return

        # 2. Execute Action
        if (
            analysis.get("category")
            and analysis["category"] in self.orchestrator.CATEGORIES
        ):
            # Dispatch to agent
            instruction = analysis.get("agent_instruction") or subject
            agent_name = self.orchestrator.find_agent_for_task(instruction)
            logger.info(f"Dispatching to agent {agent_name}: {analysis.get('summary')}")

            result = await self.orchestrator.run(
                agent_name, analysis.get("agent_instruction") or subject
            )

            # Notify user of agent action
            msg = (
                f"📧 **New Mail Intelligence**\n"
                f"From: `{sender}`\n"
                f"Subject: {subject}\n\n"
                f"🤖 **Agent {agent_name}** is handling this:\n"
                f"{result[:500]}..."
            )
            self.send_telegram(msg)
        else:
            # No specific agent, notify user
            msg = (
                f"📧 **New Email Alert** "
                f"({analysis.get('priority', 'medium')})\n"
                f"From: `{sender}`\n"
                f"Subject: {subject}\n\n"
                f"📝 **Summary:** {analysis.get('summary')}\n\n"
                f"Snippet: _{snippet}_"
            )
            self.send_telegram(msg)

    async def run(self):
        """Fetch and process loop."""
        if not await self.initialize():
            logger.error("Initialization failed. Exiting.")
            return

        logger.info("Gmail Monitor loop started.")
        while True:
            try:
                emails = self.gmail.get_recent_emails(max_results=10, unread_only=True)

                for email in emails:
                    await self.process_email(email)
                    # Mark as read to avoid re-processing
                    self.gmail.mark_as_read(email["id"])

                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                await asyncio.sleep(60)


if __name__ == "__main__":
    agent = GmailIntelligenceAgent()
    asyncio.run(agent.run())
