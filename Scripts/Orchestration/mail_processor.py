#!/usr/bin/env python3
"""
MCP Mail Processor - Background Intelligence Service
Automatically processes incoming Agent Mail messages and generates alerts.

Features:
- Polls inbox for new messages at configurable intervals
- Detects high-priority keywords and sends alerts to Admin Telegram
- Special handling for Council agents (FuchsiaCat, VioletCastle, PinkLake)
- Logs all processing activity for debugging
"""

import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

# Add parent directories to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pathlib import Path

    from dotenv import load_dotenv

    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass

from agent_mail_client import AgentMailClient

# =============================================================================
# Configuration
# =============================================================================


@dataclass
class ProcessorConfig:
    """Configuration for Mail Processor"""

    # Polling
    poll_interval_seconds: int = 60

    # High Priority Alert Keywords (case-insensitive)
    alert_keywords: list[str] = field(
        default_factory=lambda: [
            "urgent",
            "critical",
            "emergency",
            "alert",
            "error",
            "failure",
            "security",
            "breach",
            "down",
            "offline",
            "blocked",
            "help",
            "immediate",
            "asap",
            "priority",
            "warning",
            "incident",
            "auth",
            "unauthorized",
            "permission",
            "token",
            "secret",
            "key",
            "database",
            "db",
            "production",
            "deploy",
            "exception",
            "traceback",
        ]
    )

    # Council Agents - their messages get special processing
    council_agents: list[str] = field(
        default_factory=lambda: [
            "FuchsiaCat",
            "VioletCastle",
            "PinkLake",
            "Kostya",
            "WhiteMill",
            "IvoryOtter",
            "CalmSnow",
            "BlueLake",
            "GreenCastle",
            "RedStone",
        ]
    )

    # Admin Telegram Chat ID for alerts
    telegram_chat_id: str = field(default_factory=lambda: os.getenv("TELEGRAM_ADMIN_CHAT_ID", ""))
    telegram_bot_token: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))

    # Persistence
    processed_ids_file: str = field(
        default_factory=lambda: os.path.join(os.path.dirname(__file__), ".mail_processor_state.json")
    )


# =============================================================================
# Mail Processor Service
# =============================================================================


class MailProcessor:
    """Background service for processing Agent Mail messages"""

    def __init__(self, config: Optional[ProcessorConfig] = None):
        self.config = config or ProcessorConfig()
        self.client = AgentMailClient()
        self.processed_ids: set[int] = set()
        self.logger = self._setup_logging()
        self._load_state()

    def _setup_logging(self) -> logging.Logger:
        """Configure logging"""
        logger = logging.getLogger("MailProcessor")
        logger.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File handler
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)
        fh = logging.FileHandler(os.path.join(log_dir, f"mail_processor_{datetime.now():%Y%m%d}.log"))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger

    def _load_state(self):
        """Load persisted state (processed message IDs)"""
        try:
            if os.path.exists(self.config.processed_ids_file):
                with open(self.config.processed_ids_file) as f:
                    state = json.load(f)
                    self.processed_ids = set(state.get("processed_ids", []))
                self.logger.info(f"Loaded {len(self.processed_ids)} processed message IDs")
        except Exception as e:
            self.logger.warning(f"Could not load state: {e}")

    def _save_state(self):
        """Persist state and heartbeat"""
        try:
            state = {
                "processed_ids": list(self.processed_ids),
                "last_updated": datetime.now().isoformat(),
                "status": "running",
                "pid": os.getpid(),
            }
            with open(self.config.processed_ids_file, "w") as f:
                json.dump(state, f)

            # Update a general status file for the Admin Panel
            status_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "service_status.json"
            )
            try:
                current_status = {}
                if os.path.exists(status_file):
                    with open(status_file) as f:
                        current_status = json.load(f)

                current_status["mail_processor"] = {
                    "status": "🟢 Running",
                    "last_poll": datetime.now().isoformat(),
                    "processed_count": len(self.processed_ids),
                }

                with open(status_file, "w") as f:
                    json.dump(current_status, f, indent=2)
            except Exception as e:
                self.logger.warning(f"Could not update service_status.json: {e}")

        except Exception as e:
            self.logger.error(f"Could not save state: {e}")

    def _detect_priority(self, message: dict[str, Any]) -> str:
        """Detect message priority based on keywords and sender"""
        subject = (message.get("subject") or "").lower()
        body = (message.get("body_md") or message.get("body") or "").lower()
        sender = message.get("from", "")
        importance = message.get("importance", "normal")

        # Explicit high importance
        if importance == "high":
            return "high"

        # Council agent messages are always medium+ priority
        if sender in self.config.council_agents:
            # Check for alert keywords to bump to high
            text = f"{subject} {body}"
            if any(kw in text for kw in self.config.alert_keywords):
                return "high"
            return "medium"

        # Check for alert keywords
        text = f"{subject} {body}"
        if any(kw in text for kw in self.config.alert_keywords):
            return "high"

        return "normal"

    def _send_telegram_alert(self, message: dict[str, Any], priority: str):
        """Send high-priority alert to Admin Telegram"""
        if not self.config.telegram_bot_token or not self.config.telegram_chat_id:
            self.logger.warning("Telegram not configured, skipping alert")
            return

        try:
            import requests

            # Format alert message
            priority_emoji = "🚨" if priority == "high" else "📧"
            alert_text = f"""
{priority_emoji} **MCP Mail Alert** {priority_emoji}

**From:** {message.get("from", "Unknown")}
**Subject:** {message.get("subject", "No Subject")}
**Priority:** {priority.upper()}
**Time:** {message.get("created_ts", "Unknown")}

---
{(message.get("body_md") or message.get("body") or "No content")[:500]}
"""

            url = f"https://api.telegram.org/bot{self.config.telegram_bot_token}/sendMessage"
            response = requests.post(
                url,
                json={
                    "chat_id": self.config.telegram_chat_id,
                    "text": alert_text,
                    "parse_mode": "Markdown",
                },
                timeout=10,
            )

            if response.status_code == 200:
                self.logger.info(f"Sent Telegram alert for message #{message.get('id')}")
            else:
                self.logger.error(f"Telegram API error: {response.text}")

        except Exception as e:
            self.logger.error(f"Failed to send Telegram alert: {e}")

    def _process_council_message(self, message: dict[str, Any]):
        """Special processing for Council agent messages"""
        sender = message.get("from", "Unknown")
        subject = message.get("subject", "")
        body = message.get("body_md") or message.get("body") or ""

        self.logger.info(f"📋 Council message from {sender}: {subject}")

        # CIRCUIT BREAKER: Avoid infinite ack loops
        # 1. Ignore if body contains auto-ack signature
        if "Auto-Acknowledged by MailProcessor" in body or "Auto-Acknowledged" in body:
            self.logger.info(f"Skipping auto-response to auto-ack from {sender}")
            return

        # 2. Ignore replies to our own threads if no new content (dumb heuristic)
        if subject.startswith("Re:") and "Concilium" in subject:
            # Check if this is just a ping-pong.
            # For now, let's just Log it but NOT reply to avoid the storm.
            self.logger.warning(f"⚠️ POTENTIAL LOOP DETECTED from {sender}. Skipping Auto-Ack.")
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "from": sender,
            "subject": subject,
            "body": body[:1000],  # Truncate for log
            "message_id": message.get("id"),
        }

        # Append to council log
        council_log = os.path.join(os.path.dirname(__file__), "logs", "council_messages.jsonl")
        os.makedirs(os.path.dirname(council_log), exist_ok=True)
        with open(council_log, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        # Auto-acknowledge if marked as needing acknowledgement
        if message.get("ack_required"):
            message_id = message.get("id")
            if isinstance(message_id, int):
                try:
                    # Translate auto-acknowledgment to Russian as requested
                    ack_body = f"✅ **Автоматическое подтверждение (MailProcessor)**\n\nСообщение получено в {datetime.now():%Y-%m-%d %H:%M:%S Z}"
                    self.client.reply(
                        message_id=message_id,
                        body_md=ack_body,
                    )
                    self.logger.info(f"Auto-acknowledged message #{message_id}")
                except Exception as e:
                    self.logger.error(f"Failed to auto-acknowledge: {e}")
            else:
                self.logger.warning("Cannot auto-acknowledge message without int id")

        # Parse for specific instructions/approvals
        self._parse_council_instructions(message)

    def _parse_council_instructions(self, message: dict[str, Any]):
        """Parse council messages for specific commands or approvals"""
        sender = message.get("from", "Unknown")
        body = (message.get("body_md") or message.get("body") or "").lower()
        subject = (message.get("subject") or "").lower()

        # Keywords for approval/actions
        approvals = ["approved", "одобрено", "подтверждаю", "confirm", "approve"]
        rejections = ["rejected", "отклонено", "отмена", "deny", "reject"]

        instruction_found = False
        action = None

        if any(kw in body or kw in subject for kw in approvals):
            action = "APPROVED"
            instruction_found = True
        elif any(kw in body or kw in subject for kw in rejections):
            action = "REJECTED"
            instruction_found = True

        if instruction_found:
            instruction_entry = {
                "timestamp": datetime.now().isoformat(),
                "from": sender,
                "action": action,
                "subject": message.get("subject"),
                "message_id": message.get("id"),
                "content": body[:500],
            }

            # Save to instructions log
            instr_log = os.path.join(os.path.dirname(__file__), "logs", "council_instructions.jsonl")
            with open(instr_log, "a") as f:
                f.write(json.dumps(instruction_entry) + "\n")

            self.logger.info(f"🎯 Council Instruction Detected: {action} from {sender}")

            # If it's an approval for the pending Spec 502, we could potentially update NOTEBOOK.md
            if "502" in body or "502" in subject:
                self.logger.info("🚀 Approval for Spec 502 detected! Triggering notebook update...")
                # Note: Actual notebook update logic can be added here or handled by another script watching this log

    def process_message(self, message: dict[str, Any]) -> bool:
        """Process a single message. Returns True if processed successfully."""
        message_id = message.get("id")
        if not isinstance(message_id, int):
            self.logger.warning("Skipping message without int id")
            return False

        if message_id in self.processed_ids:
            return True  # Already processed

        try:
            sender = message.get("from", "Unknown")
            subject = message.get("subject", "No Subject")

            self.logger.info(f"Processing message #{message_id} from {sender}: {subject}")

            # Detect priority
            priority = self._detect_priority(message)

            # High priority -> Telegram alert
            if priority == "high":
                self._send_telegram_alert(message, priority)

            # Council agent -> special processing
            if sender in self.config.council_agents:
                self._process_council_message(message)

            # Mark as read
            try:
                self.client.mark_read(message_id)
            except Exception as e:
                self.logger.warning(f"Could not mark message #{message_id} as read: {e}")

            # Add to processed set
            self.processed_ids.add(message_id)

            return True

        except Exception as e:
            self.logger.error(f"Error processing message #{message_id}: {e}")
            return False

    def poll_and_process(self):
        """Poll inbox and process new messages"""
        try:
            # Health check
            if not self.client.health_check():
                self.logger.warning("Mail server not available, skipping poll")
                return

            # Fetch inbox
            messages = self.client.fetch_inbox(limit=50)

            if not messages:
                self.logger.debug("No messages in inbox")
                return

            new_count = 0
            for msg in messages:
                msg_id = msg.get("id")
                if isinstance(msg_id, int) and msg_id not in self.processed_ids:
                    if self.process_message(msg):
                        new_count += 1

            if new_count > 0:
                self.logger.info(f"Processed {new_count} new messages")

            self._save_state()

        except Exception as e:
            self.logger.error(f"Error during poll: {e}")

    def run(self):
        """Run the processor loop"""
        self.logger.info("🚀 Mail Processor starting...")

        # Ensure agent is registered
        try:
            self.client.ensure_project()
            reg = self.client.register(task_description="Monitoring inbox for alerts")
            self.logger.info(f"✅ Registered as agent: {reg.get('name')} (ID: {reg.get('id')})")
        except Exception as e:
            self.logger.warning(f"⚠️ Registration failed: {e}")

        self.logger.info(f"   Poll interval: {self.config.poll_interval_seconds}s")
        self.logger.info(f"   Council agents: {', '.join(self.config.council_agents)}")
        self.logger.info(f"   Alert keywords: {len(self.config.alert_keywords)} configured")

        try:
            while True:
                self.poll_and_process()
                time.sleep(self.config.poll_interval_seconds)
        except KeyboardInterrupt:
            self.logger.info("Shutting down...")
            self._save_state()
        except Exception as e:
            self.logger.error(f"Fatal error: {e}")
            self._save_state()
            raise


# =============================================================================
# CLI Interface
# =============================================================================


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="MCP Mail Processor Service")
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Poll interval in seconds (default: 60)",
    )
    parser.add_argument("--once", action="store_true", help="Process once and exit (no loop)")
    parser.add_argument("--test-alert", action="store_true", help="Send a test alert to Telegram")

    args = parser.parse_args()

    config = ProcessorConfig(poll_interval_seconds=args.interval)
    processor = MailProcessor(config)

    if args.test_alert:
        print("Sending test alert...")
        test_msg = {
            "id": 0,
            "from": "MailProcessor",
            "subject": "Test Alert",
            "body_md": "This is a test alert from MailProcessor.",
            "created_ts": datetime.now().isoformat(),
        }
        processor._send_telegram_alert(test_msg, "high")
        print("Done!")
    elif args.once:
        processor.poll_and_process()
    else:
        processor.run()


if __name__ == "__main__":
    main()
