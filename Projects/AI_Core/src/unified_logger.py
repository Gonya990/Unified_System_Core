import datetime
import json
import logging
import os


class UnifiedJSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings compatible with Google Cloud Logging.
    """
    def format(self, record):
        # Base log record
        log_entry = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "logger": record.name,
            "location": f"{record.pathname}:{record.lineno}",
            "serviceContext": {
                "service": os.getenv("SERVICE_NAME", "ai-core"),
                "version": os.getenv("SERVICE_VERSION", "unknown")
            }
        }

        # Add Google Cloud Trace ID if available in record attributes
        if hasattr(record, "trace_id"):
            project_id = os.getenv("GCP_PROJECT_ID", "my-home-435112")
            trace_id = record.trace_id
            log_entry["logging.googleapis.com/trace"] = (
                f"projects/{project_id}/traces/{trace_id}"
            )

        # Add span ID if available
        if hasattr(record, "span_id"):
            log_entry["logging.googleapis.com/spanId"] = record.span_id

        # Handle exceptions
        if record.exc_info:
            log_entry["stack_trace"] = self.formatException(record.exc_info)
            # Find the actual error message if message is empty
            if not log_entry["message"]:
                log_entry["message"] = str(record.exc_info[1])

        return json.dumps(log_entry)

def setup_unified_logging(level=logging.INFO):
    """
    Configures the root logger to output structured JSON to stdout.
    This is the preferred method for GKE/Cloud Run.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(UnifiedJSONFormatter())

    root = logging.getLogger()
    # Remove existing handlers to avoid duplicates
    for h in root.handlers[:]:
        root.removeHandler(h)

    root.addHandler(handler)
    root.setLevel(level)

    # Silence noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("googleapiclient").setLevel(logging.WARNING)

    # Test log
    logging.info(
        f"✅ Unified JSON Logging Initialized for {os.getenv('SERVICE_NAME', 'ai-core')}"
    )
