#!/usr/bin/env python3
"""
Metrics Collector Service
Collects system metrics and sends them to GCP Cloud Monitoring.
Also sends alerts to Telegram when thresholds are exceeded.
"""

import os
import sys
import time
import logging
import psutil
import subprocess
import requests
from datetime import datetime, timezone

# Setup logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("metrics-collector")

# Configuration from environment
GCP_PROJECT = os.environ.get("GCP_PROJECT", "gen-lang-client-0982257437")
INSTANCE_NAME = os.environ.get("INSTANCE_NAME", "igor-gaming-1")
COLLECTION_INTERVAL = int(os.environ.get("COLLECTION_INTERVAL", "60"))
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_IDS = os.environ.get("TELEGRAM_CHAT_IDS", "").split(",")

# Thresholds for alerts (can be overridden via env)
THRESHOLDS = {
    "cpu_usage": int(os.environ.get("THRESHOLD_CPU", "90")),
    "memory_usage": int(os.environ.get("THRESHOLD_MEMORY", "85")),
    "disk_usage": int(os.environ.get("THRESHOLD_DISK", "90")),
    "gpu_temp": int(os.environ.get("THRESHOLD_GPU_TEMP", "80"))
}


def get_gpu_info():
    """Get GPU temperature and memory usage via nvidia-smi."""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu,memory.used,memory.total,utilization.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split(", ")
            return {
                "temp": int(parts[0]),
                "memory_used": int(parts[1]),
                "memory_total": int(parts[2]),
                "utilization": int(parts[3])
            }
    except FileNotFoundError:
        logger.debug("nvidia-smi not found, GPU monitoring disabled")
    except Exception as e:
        logger.debug(f"GPU info error: {e}")
    return None


def collect_metrics():
    """Collect all system metrics."""
    metrics = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
    }

    gpu = get_gpu_info()
    if gpu:
        metrics["gpu_temp"] = gpu["temp"]
        metrics["gpu_memory_percent"] = (gpu["memory_used"] / gpu["memory_total"]) * 100
        metrics["gpu_utilization"] = gpu["utilization"]

    return metrics


def send_telegram_alert(message: str):
    """Send alert to Telegram."""
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not set, skipping alert")
        return

    for chat_id in TELEGRAM_CHAT_IDS:
        if not chat_id.strip():
            continue
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            response = requests.post(url, json={
                "chat_id": chat_id.strip(),
                "text": f"🚨 *ALERT* от {INSTANCE_NAME}\n\n{message}",
                "parse_mode": "Markdown"
            }, timeout=10)
            if response.status_code == 200:
                logger.debug(f"Alert sent to chat {chat_id}")
            else:
                logger.warning(f"Telegram API error: {response.status_code}")
        except Exception as e:
            logger.error(f"Telegram error: {e}")


def check_thresholds(metrics: dict):
    """Check if any metrics exceed thresholds and send alerts."""
    alerts = []
    for metric, threshold in THRESHOLDS.items():
        if metric in metrics and metrics[metric] > threshold:
            alerts.append(f"• {metric}: {metrics[metric]:.1f}% (порог: {threshold}%)")
            logger.warning(f"Threshold exceeded: {metric}={metrics[metric]:.1f}% > {threshold}%")

    if alerts:
        send_telegram_alert("\n".join(alerts))
        return True
    return False


def send_to_gcp(metrics: dict):
    """Send metrics to GCP Cloud Monitoring."""
    try:
        from google.cloud import monitoring_v3

        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{GCP_PROJECT}"

        now = time.time()

        for metric_name, value in metrics.items():
            if metric_name == "timestamp" or value is None:
                continue

            series = monitoring_v3.TimeSeries()
            series.metric.type = f"custom.googleapis.com/{INSTANCE_NAME}/{metric_name}"
            series.resource.type = "global"
            series.resource.labels["project_id"] = GCP_PROJECT

            point = monitoring_v3.Point()
            point.value.double_value = float(value)
            point.interval.end_time.seconds = int(now)
            series.points = [point]

            client.create_time_series(name=project_name, time_series=[series])

        logger.debug("Metrics sent to GCP")
        return True
    except ImportError:
        logger.debug("google-cloud-monitoring not installed, skipping GCP export")
        return False
    except Exception as e:
        logger.error(f"GCP error: {e}")
        return False


def main():
    """Main metrics collection loop."""
    logger.info("=" * 50)
    logger.info("Metrics Collector Service Starting")
    logger.info(f"Instance: {INSTANCE_NAME}")
    logger.info(f"GCP Project: {GCP_PROJECT}")
    logger.info(f"Collection Interval: {COLLECTION_INTERVAL}s")
    logger.info(f"Log Level: {LOG_LEVEL}")
    logger.info(f"Thresholds: {THRESHOLDS}")
    logger.info("=" * 50)

    while True:
        try:
            metrics = collect_metrics()

            # Log metrics at appropriate level
            log_msg = f"CPU: {metrics['cpu_usage']}%, RAM: {metrics['memory_usage']}%, Disk: {metrics['disk_usage']}%"
            if "gpu_temp" in metrics:
                log_msg += f", GPU: {metrics['gpu_temp']}°C ({metrics['gpu_utilization']}%)"

            logger.info(log_msg)

            # Check thresholds and send alerts
            check_thresholds(metrics)

            # Send to GCP
            send_to_gcp(metrics)

        except Exception as e:
            logger.error(f"Collection error: {e}")

        time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
    main()
