#!/usr/bin/env python3
"""
Watchdog Service for AI Telegram Bot.
Monitors bot health and GCP budget alerts.
"""

import os
import sys
import time
import logging
import subprocess
import requests

# Setup logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("watchdog")

# Configuration
HEALTH_URL = os.environ.get("HEALTH_URL", "http://localhost:8080/health")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "60"))  # seconds
FAIL_THRESHOLD = int(os.environ.get("FAIL_THRESHOLD", "3"))  # consecutive failures before alert
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_IDS = os.environ.get("TELEGRAM_CHAT_IDS", "").split(",")


def send_alert(message: str):
    """Send alert to Telegram."""
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not set, skipping alert")
        return

    for chat_id in TELEGRAM_CHAT_IDS:
        if not chat_id.strip():
            continue
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, json={
                "chat_id": chat_id.strip(),
                "text": message,
                "parse_mode": "Markdown"
            }, timeout=10)
            logger.debug(f"Alert sent to chat {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")


def check_health() -> bool:
    """Check if the bot is healthy."""
    try:
        response = requests.get(HEALTH_URL, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.debug(f"Health check failed: {e}")
        return False


class BudgetMonitor:
    """Monitors GCP budget alerts via Gmail."""

    def __init__(self):
        self.last_check = 0
        self.check_interval = 3600 * 4  # Check every 4 hours
        self.alert_sent = False

    def check_budget_alerts(self):
        """Scan Gmail for budget alerts > 90%."""
        if time.time() - self.last_check < self.check_interval:
            return

        try:
            # Lazy import to avoid circular dependency issues at module level
            from src.gmail_client import GmailClient
            client = GmailClient()
            if not client.authenticated:
                logger.debug("Gmail client not authenticated, skipping budget check")
                return

            # Search specifically for budget alerts from Google
            query = "from:CloudPlatform-noreply@google.com subject:budget"
            messages = client.search_emails(query, max_results=3)

            for msg in messages:
                snippet = msg.get('snippet', '')
                subject = msg.get('subject', '')

                # Check for high percentages
                if "100%" in subject or "150%" in subject or "90%" in subject:
                    logger.warning(f"Budget Alert Found: {subject}")

                    if not self.alert_sent:
                        send_alert(f"💰 *БЮДЖЕТ ПРЕВЫШЕН!*\nНайдено уведомление: {subject}\n\n⚡ *ПЕРЕКЛЮЧАЮ НА OLLAMA*")
                        self.enforce_ollama()
                        self.alert_sent = True

        except ImportError:
            logger.debug("Gmail client not available, skipping budget check")
        except Exception as e:
            logger.error(f"Budget check failed: {e}")
        finally:
            self.last_check = time.time()

    def enforce_ollama(self):
        """Force switch to Ollama in .env and restart bot."""
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        try:
            # Read current env
            if not os.path.exists(env_path):
                logger.warning(f".env file not found at {env_path}")
                return

            with open(env_path, 'r') as f:
                lines = f.readlines()

            new_lines = []
            changed = False
            for line in lines:
                if line.startswith("INFERENCE_PROVIDER="):
                    if "ollama" not in line.lower():
                        new_lines.append("INFERENCE_PROVIDER=ollama\n")
                        changed = True
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)

            if changed:
                with open(env_path, 'w') as f:
                    f.writelines(new_lines)
                logger.info("Switched INFERENCE_PROVIDER to ollama.")

                # Restart service (works in systemd environment)
                result = subprocess.run(
                    ["sudo", "systemctl", "restart", "ai-bot"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    logger.info("Restarted ai-bot service.")
                else:
                    logger.warning(f"Failed to restart service: {result.stderr}")
            else:
                logger.info("Already on Ollama.")

        except Exception as e:
            logger.error(f"Failed to enforce Ollama: {e}")
            send_alert(f"❌ Не удалось переключить на Ollama автоматически: {e}")


def main():
    """Main watchdog loop."""
    logger.info("=" * 50)
    logger.info("Watchdog Service Starting")
    logger.info(f"Health URL: {HEALTH_URL}")
    logger.info(f"Check Interval: {CHECK_INTERVAL}s")
    logger.info(f"Fail Threshold: {FAIL_THRESHOLD}")
    logger.info(f"Log Level: {LOG_LEVEL}")
    logger.info("=" * 50)

    fail_count = 0
    budget_monitor = BudgetMonitor()

    # Wait for bot to start initially
    logger.info("Waiting 10s for bot to initialize...")
    time.sleep(10)

    while True:
        try:
            # 1. Health Check
            if check_health():
                if fail_count > 0:
                    logger.info("Bot recovered.")
                    if fail_count >= FAIL_THRESHOLD:
                        send_alert("✅ Бот восстановился и снова онлайн.")
                fail_count = 0
                logger.debug("Health check passed")
            else:
                fail_count += 1
                logger.warning(f"Health check failed ({fail_count}/{FAIL_THRESHOLD})")

                if fail_count == FAIL_THRESHOLD:
                    send_alert(f"⚠️ Бот не отвечает уже {FAIL_THRESHOLD} минут!\nВозможно, он завис или упал.")
                    # Auto-restart attempt
                    logger.info("Attempting to restart ai-bot service...")
                    subprocess.run(["sudo", "systemctl", "restart", "ai-bot"], capture_output=True)

            # 2. Budget Check
            budget_monitor.check_budget_alerts()

        except Exception as e:
            logger.error(f"Watchdog error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
