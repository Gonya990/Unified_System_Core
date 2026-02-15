import asyncio
import json
import logging
import os
import subprocess
import time

import aiohttp

# ==========================================
# CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_CHAT_ID = (
    os.getenv("ADMIN_CHAT_ID")
    or os.getenv("TELEGRAM_ADMIN_CHAT_ID")
    or ""
)
CHECK_INTERVAL = 60  # seconds

# Critical processes to monitor
MONITORED_PROCESSES = ["bot-v2", "crypto-bot", "dashboard", "landing-page"]

# Critical HTTP endpoints
HEALTH_ENDPOINTS = {
    "bot-v2": "http://localhost:8095/health",
    "dashboard": "http://localhost:8096/",
    "landing-page": "http://localhost:3000/",
}

# Logging Setup
LOG_FILE = "system_watchdog.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger("WatchdogV2")

# Internal State tracker
app_states = {}  # name -> {status, restarts, last_alive}


async def send_telegram_alert(message: str):
    """Sends a markdown message to the admin chat."""
    if not TELEGRAM_BOT_TOKEN or not ADMIN_CHAT_ID:
        logger.warning("Telegram alert skipped: missing TELEGRAM_BOT_TOKEN or ADMIN_CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": ADMIN_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10) as resp:
                if resp.status != 200:
                    logger.error(f"Failed to send telegram alert: {await resp.text()}")
    except Exception as e:
        logger.error(f"Error sending telegram alert: {e}")


async def get_pm2_status():
    """Gets list of all PM2 managed processes."""
    try:
        output = subprocess.check_output(["pm2", "jlist"], stderr=subprocess.STDOUT).decode()
        return json.loads(output)
    except Exception as e:
        logger.error(f"Failed to get PM2 jlist: {e}")
        return []


async def check_pm2():
    """Check PM2 process statuses and restart counts."""
    processes = await get_pm2_status()
    alerts = []

    current_found = set()
    for proc in processes:
        name = proc.get("name")
        if name not in MONITORED_PROCESSES:
            continue

        current_found.add(name)
        status = proc.get("pm2_env", {}).get("status")
        restarts = proc.get("pm2_env", {}).get("restart_time", 0)

        prev = app_states.get(name)
        if prev:
            # Status Transition
            if status != "online" and prev.get("status") == "online":
                alerts.append(f"🔴 **CRITICAL: Process Down!**\nName: `{name}`\nStatus: `{status}`")
            elif status == "online" and prev.get("status") != "online":
                alerts.append(f"✅ **RECOVERED: Process Online**\nName: `{name}`")

            # Restart Anomaly
            if restarts > prev.get("restarts", 0):
                diff = restarts - prev.get("restarts", 0)
                alerts.append(
                    f"⚠️ **WARNING: Process Restarted!**\nName: `{name}`\nRecent Restarts: `+{diff}`\nTotal: `{restarts}`"
                )

        # Update State
        app_states[name] = {"status": status, "restarts": restarts, "last_check": time.time()}

    # Check for missing processes
    for name in MONITORED_PROCESSES:
        if name not in current_found:
            prev = app_states.get(name)
            if not prev or prev.get("exists", True):
                alerts.append(f"❓ **UNKNOWN: Process Missing!**\nName: `{name}`\nIt's not in PM2 list anymore.")
                app_states[name] = {"status": "missing", "restarts": 0, "exists": False}
        else:
            app_states[name]["exists"] = True

    for alert in alerts:
        await send_telegram_alert(alert)


async def check_http():
    """Perform heartbeat checks on defined HTTP endpoints."""
    for name, url in HEALTH_ENDPOINTS.items():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as resp:
                    # Dashboard redirects to login if no cookie, which is 307 or 200 depending on templates
                    if resp.status >= 500:
                        await send_telegram_alert(
                            f"🚨 **ALERT: Server Error!**\nName: `{name}`\nURL: {url}\nStatus: `{resp.status}`"
                        )
                    elif resp.status == 404:
                        await send_telegram_alert(f"🚨 **ALERT: 404 Not Found!**\nName: `{name}`\nURL: {url}")
        except Exception as e:
            # For critical services like bot-v2, alert on failure
            if name == "bot-v2":
                logger.error(f"Bot-V2 heartbeat failed: {e}")
                # To avoid spamming, we can put a cooldown
                await send_telegram_alert(
                    f"🚨 **CRITICAL: Bot-V2 unresponsive!**\nEndpoint: `{url}`\nError: `{str(e)[:100]}`"
                )


async def main_loop():
    logger.info("Watchdog V2 initializing...")
    await send_telegram_alert(
        "👁 **SYSTEM WATCHDOG V2 (Unified Home)**\nМониторинг активирован. Слежу за всеми процессами 24/7."
    )

    # Initial state capture
    processes = await get_pm2_status()
    for proc in processes:
        name = proc.get("name")
        if name in MONITORED_PROCESSES:
            app_states[name] = {
                "status": proc.get("pm2_env", {}).get("status"),
                "restarts": proc.get("pm2_env", {}).get("restart_time", 0),
                "last_check": time.time(),
                "exists": True,
            }

    while True:
        try:
            await check_pm2()
            await check_http()
        except Exception as e:
            logger.error(f"Error in main loop: {e}")

        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("Watchdog stopped by user.")
    except Exception as e:
        logger.critical(f"Watchdog crashed: {e}")
