import os
import threading
import time

from google.cloud import monitoring_v3


class UnifiedMonitoring:
    def __init__(self, service_name):
        self.project_id = os.getenv("GCP_PROJECT_ID", "my-home-435112")
        self.service_name = service_name
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{self.project_id}"

    def send_metric(self, metric_name, value, unit="1"):
        """
        Sends a custom metric to Google Cloud Monitoring.
        metric_name: e.g., "active_users", "trades_count"
        value: numeric value
        """
        try:
            series = monitoring_v3.TimeSeries()
            series.metric.type = f"custom.googleapis.com/{self.service_name}/{metric_name}"
            series.resource.type = "global"
            series.resource.labels["project_id"] = self.project_id

            now = time.time()
            seconds = int(now)
            nanos = int((now - seconds) * 10**9)

            interval = monitoring_v3.TimeInterval(
                {"end_time": {"seconds": seconds, "nanos": nanos}}
            )

            point = monitoring_v3.Point(
                {"value": {"double_value": float(value)}, "interval": interval}
            )

            series.points = [point]
            self.client.create_time_series(name=self.project_name, time_series=[series])
            return True
        except Exception as e:
            # Silently fail or log to unified logger if possible, but avoid recursion
            print(f"⚠️ Monitoring Error: {e}")
            return False

    def start_heartbeat(self, interval=60):
        """Starts a background thread to send heartbeat everywhere minute."""

        def _loop():
            while True:
                self.send_metric("heartbeat", 1)
                time.sleep(interval)

        t = threading.Thread(target=_loop, daemon=True)
        t.start()


# Global instance pattern
_monitor = None


def get_monitor(service_name=None):
    global _monitor
    if not _monitor:
        if not service_name:
            service_name = os.getenv("SERVICE_NAME", "unknown-service")
        _monitor = UnifiedMonitoring(service_name)
    return _monitor
