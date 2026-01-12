#!/usr/bin/env python3
"""
GCP Custom Metrics Collector for igor-gaming-1
Collects CPU, RAM, GPU metrics and pushes to Google Cloud Monitoring
"""

import logging
import os
import subprocess
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import psutil
    from google.cloud import monitoring_v3
    from google.protobuf import timestamp_pb2
except ImportError as e:
    logger.error(f"Missing dependency: {e}")
    logger.info("Install with: pip install google-cloud-monitoring psutil")
    exit(1)

# Configuration
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "my-home-435112")
INSTANCE_ID = os.environ.get("INSTANCE_ID", "igor-gaming-1")
COLLECTION_INTERVAL = int(os.environ.get("COLLECTION_INTERVAL", "60"))

# Metric type prefix
METRIC_PREFIX = "custom.googleapis.com/igor_gaming"


def get_gpu_metrics() -> dict:
    """Get NVIDIA GPU metrics using nvidia-smi"""
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total",
                "--format=csv,noheader,nounits"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split(", ")
            if len(parts) >= 4:
                gpu_temp = float(parts[0])
                gpu_util = float(parts[1])
                mem_used = float(parts[2])
                mem_total = float(parts[3])
                return {
                    "gpu_temperature": gpu_temp,
                    "gpu_utilization": gpu_util,
                    "gpu_memory_used_mb": mem_used,
                    "gpu_memory_total_mb": mem_total,
                    "gpu_memory_percent": (mem_used / mem_total) * 100 if mem_total > 0 else 0
                }
    except Exception as e:
        logger.warning(f"Failed to get GPU metrics: {e}")
    return {}


def get_system_metrics() -> dict:
    """Get CPU and RAM metrics using psutil"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "memory_used_gb": psutil.virtual_memory().used / (1024**3),
        "disk_percent": psutil.disk_usage('/').percent,
        "load_average_1m": os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
    }


def create_time_series(client, project_name: str, metric_type: str, value: float, labels: dict):
    """Create a time series data point using dict initialization"""
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    # Use dict-style initialization compatible with proto-plus
    series = {
        "metric": {
            "type": metric_type,
            "labels": labels
        },
        "resource": {
            "type": "generic_node",
            "labels": {
                "project_id": PROJECT_ID,
                "location": "global",
                "namespace": "igor-home",
                "node_id": INSTANCE_ID
            }
        },
        "points": [
            {
                "interval": {
                    "end_time": {"seconds": seconds, "nanos": nanos}
                },
                "value": {"double_value": value}
            }
        ]
    }
    return series


def push_metrics(metrics: dict):
    """Push metrics to GCP Monitoring"""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{PROJECT_ID}"

    time_series_list = []
    labels = {"instance": INSTANCE_ID}

    for metric_name, value in metrics.items():
        if value is not None:
            metric_type = f"{METRIC_PREFIX}/{metric_name}"
            series = create_time_series(client, project_name, metric_type, float(value), labels)
            time_series_list.append(series)

    if time_series_list:
        try:
            client.create_time_series(
                name=project_name,
                time_series=time_series_list
            )
            logger.info(f"Pushed {len(time_series_list)} metrics to GCP Monitoring")
        except Exception as e:
            logger.error(f"Failed to push metrics: {e}")


def main():
    """Main collection loop"""
    logger.info(f"Starting GCP metrics collector for {INSTANCE_ID}")
    logger.info(f"Project: {PROJECT_ID}, Interval: {COLLECTION_INTERVAL}s")

    while True:
        try:
            # Collect all metrics
            metrics = {}
            metrics.update(get_system_metrics())
            metrics.update(get_gpu_metrics())

            logger.info(f"Collected metrics: CPU={metrics.get('cpu_percent', 'N/A')}%, "
                       f"RAM={metrics.get('memory_percent', 'N/A')}%, "
                       f"GPU={metrics.get('gpu_utilization', 'N/A')}%, "
                       f"GPU Temp={metrics.get('gpu_temperature', 'N/A')}°C")

            # Push to GCP
            push_metrics(metrics)

        except Exception as e:
            logger.error(f"Error in collection loop: {e}")

        time.sleep(COLLECTION_INTERVAL)


if __name__ == "__main__":
    main()
