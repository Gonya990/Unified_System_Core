#!/usr/bin/env python3
"""
Igor Gaming Metrics Collector
Collects system metrics and sends them to GCP Cloud Monitoring.
Also sends alerts to Telegram when thresholds are exceeded.
"""

import subprocess
import time
from datetime import datetime, timezone

import psutil
import requests

# Configuration
GCP_PROJECT = "gen-lang-client-0982257437"
INSTANCE_NAME = "igor-gaming-1"
COLLECTION_INTERVAL = 60  # seconds

# Thresholds for alerts
THRESHOLDS = {"cpu_usage": 90, "memory_usage": 85, "disk_usage": 90, "gpu_temp": 80}

# Telegram config
TELEGRAM_BOT_TOKEN = "8518131338:AAFzuwI6PJ7ftiZVe3u8cWtjYz1pSU_QIqQ"
TELEGRAM_CHAT_IDS = [708531393, 1881720235]


def get_gpu_info():
    """Get GPU temperature and memory usage via nvidia-smi."""
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=temperature.gpu,memory.used,memory.total,utilization.gpu",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split(", ")
            return {
                "temp": int(parts[0]),
                "memory_used": int(parts[1]),
                "memory_total": int(parts[2]),
                "utilization": int(parts[3]),
            }
    except Exception as e:
        print(f"GPU info error: {e}")
    return None


def collect_metrics():
    """Collect all system metrics."""
    metrics = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
    }

    gpu = get_gpu_info()
    if gpu:
        metrics["gpu_temp"] = gpu["temp"]
        metrics["gpu_memory_percent"] = (gpu["memory_used"] / gpu["memory_total"]) * 100
        metrics["gpu_utilization"] = gpu["utilization"]

    return metrics


def send_telegram_alert(message: str):
    """Send alert to Telegram."""
    for chat_id in TELEGRAM_CHAT_IDS:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": f"🚨 *ALERT* от {INSTANCE_NAME}\n\n{message}",
                    "parse_mode": "Markdown",
                },
                timeout=10,
            )
        except Exception as e:
            print(f"Telegram error: {e}")


def check_thresholds(metrics: dict):
    """Check if any metrics exceed thresholds and send alerts."""
    alerts = []
    for metric, threshold in THRESHOLDS.items():
        if metric in metrics and metrics[metric] > threshold:
            alerts.append(f"• {metric}: {metrics[metric]:.1f}% (порог: {threshold}%)")

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

        print(f"[{datetime.now()}] Metrics sent to GCP")
        return True
    except Exception as e:
        print(f"GCP error: {e}")
        return False


def main():
    print(f"Starting metrics collector for {INSTANCE_NAME}")
    print(f"Collection interval: {COLLECTION_INTERVAL}s")
    print(f"GCP Project: {GCP_PROJECT}")

    while True:
        try:
            metrics = collect_metrics()
            print(f"[{metrics['timestamp']}] CPU: {metrics['cpu_usage']}%, RAM: {metrics['memory_usage']}%", end="")

            if "gpu_temp" in metrics:
                print(f", GPU: {metrics['gpu_temp']}°C")
            else:
                print()

            # Check thresholds and send alerts
            check_thresholds(metrics)

            # Send to GCP
            send_to_gcp(metrics)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
    main()
