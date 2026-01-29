"""
Logging Configuration for AI Telegram Bot.
Provides structured JSON logging with OpenTelemetry integration for observability.

This module wraps the unified observability library and provides backward-compatible
logging setup for the AI Telegram Bot service.
"""
import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Optional

# Try to import unified observability module (installed package or path-based)
try:
    from unified_observability import setup_observability, get_logger, LogContext
    UNIFIED_OBSERVABILITY_AVAILABLE = True
except ImportError:
    try:
        # Fallback for local development without installed package
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        from infra.observability import setup_observability, get_logger, LogContext
        UNIFIED_OBSERVABILITY_AVAILABLE = True
    except ImportError:
        UNIFIED_OBSERVABILITY_AVAILABLE = False


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": os.environ.get("OTEL_SERVICE_NAME", "ai-telegram-bot"),
        }

        # Add extra fields
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id
        if hasattr(record, "chat_id"):
            log_entry["chat_id"] = record.chat_id

        # Add trace context if available
        if hasattr(record, "trace_id"):
            log_entry["trace_id"] = record.trace_id
        if hasattr(record, "span_id"):
            log_entry["span_id"] = record.span_id
        if hasattr(record, "correlation_id"):
            log_entry["correlation_id"] = record.correlation_id

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def setup_logging(
    service_name: Optional[str] = None,
    service_version: str = "1.0.0",
) -> None:
    """
    Configure logging based on environment with OpenTelemetry support.

    Args:
        service_name: Service name for telemetry (default: from env or 'ai-telegram-bot')
        service_version: Service version for telemetry
    """
    service_name = service_name or os.environ.get("OTEL_SERVICE_NAME", "ai-telegram-bot")
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

    # Use unified observability if available
    if UNIFIED_OBSERVABILITY_AVAILABLE:
        setup_observability(
            service_name=service_name,
            service_version=service_version,
            log_level=log_level,
        )
        logging.getLogger("logging_config").info(
            "Using unified observability module",
            extra={"otel_enabled": True}
        )
        return

    # Fallback to local logging configuration
    handler = logging.StreamHandler(sys.stdout)

    # Use JSON format in production, readable format in debug
    if log_level == "DEBUG":
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
    else:
        formatter = JSONFormatter()

    handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Reduce noise from libraries
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
