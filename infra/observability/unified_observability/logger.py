"""
Structured logging with OpenTelemetry integration.

Provides JSON-formatted logs with trace correlation, context propagation,
and automatic enrichment of log records with service metadata.
"""

import json
import logging
import os
import sys
import threading
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Optional

# OpenTelemetry imports (graceful fallback if not installed)
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry._logs import set_logger_provider
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
    from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None

# Context variables for request-scoped data
_correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)
_request_context: ContextVar[dict] = ContextVar("request_context", default={})

# Global state
_observability_initialized = False
_service_name = "unknown-service"
_service_version = "0.0.0"


class LogContext:
    """
    Context manager for adding contextual information to logs.

    Usage:
        with LogContext(user_id=123, request_id="abc"):
            logger.info("Processing request")  # Will include user_id and request_id
    """

    def __init__(self, **kwargs):
        self.context = kwargs
        self._token = None

    def __enter__(self):
        current = _request_context.get().copy()
        current.update(self.context)
        self._token = _request_context.set(current)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._token:
            _request_context.reset(self._token)
        return False


def set_correlation_id(correlation_id: Optional[str] = None) -> str:
    """Set or generate a correlation ID for the current context."""
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())[:8]
    _correlation_id.set(correlation_id)
    return correlation_id


def get_correlation_id() -> Optional[str]:
    """Get the current correlation ID."""
    return _correlation_id.get()


class JSONFormatter(logging.Formatter):
    """
    Format log records as JSON with OpenTelemetry trace context.

    Output format:
    {
        "timestamp": "2026-01-29T12:00:00.000Z",
        "level": "INFO",
        "logger": "my.module",
        "message": "Something happened",
        "service": "my-service",
        "trace_id": "abc123...",
        "span_id": "def456...",
        "correlation_id": "xyz789",
        ...extra_fields
    }
    """

    RESERVED_ATTRS = {
        "name", "msg", "args", "created", "filename", "funcName",
        "levelname", "levelno", "lineno", "module", "msecs",
        "pathname", "process", "processName", "relativeCreated",
        "stack_info", "exc_info", "exc_text", "thread", "threadName",
        "taskName", "message"
    }

    def __init__(self, service_name: str = "unknown", service_version: str = "0.0.0"):
        super().__init__()
        self.service_name = service_name
        self.service_version = service_version

    def format(self, record: logging.LogRecord) -> str:
        # Base log entry
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service_name,
            "version": self.service_version,
        }

        # Add source location for errors
        if record.levelno >= logging.ERROR:
            log_entry["location"] = {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            }

        # Add OpenTelemetry trace context if available
        if OTEL_AVAILABLE and trace:
            span = trace.get_current_span()
            if span and span.is_recording():
                ctx = span.get_span_context()
                log_entry["trace_id"] = format(ctx.trace_id, "032x")
                log_entry["span_id"] = format(ctx.span_id, "016x")

        # Add correlation ID
        correlation_id = get_correlation_id()
        if correlation_id:
            log_entry["correlation_id"] = correlation_id

        # Add request context
        request_ctx = _request_context.get()
        if request_ctx:
            log_entry.update(request_ctx)

        # Add extra fields from the record
        for key, value in record.__dict__.items():
            if key not in self.RESERVED_ATTRS and not key.startswith("_"):
                try:
                    # Ensure value is JSON serializable
                    json.dumps(value)
                    log_entry[key] = value
                except (TypeError, ValueError):
                    log_entry[key] = str(value)

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info),
            }

        return json.dumps(log_entry, default=str)


class ReadableFormatter(logging.Formatter):
    """Human-readable formatter for development/debug mode."""

    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def __init__(self, use_colors: bool = True):
        super().__init__()
        self.use_colors = use_colors and sys.stdout.isatty()

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        level = record.levelname
        if self.use_colors:
            color = self.COLORS.get(level, "")
            level = f"{color}{level:8}{self.RESET}"
        else:
            level = f"{level:8}"

        # Build message
        msg = f"{timestamp} | {level} | {record.name} | {record.getMessage()}"

        # Add correlation ID if present
        correlation_id = get_correlation_id()
        if correlation_id:
            msg = f"{timestamp} | {level} | [{correlation_id}] {record.name} | {record.getMessage()}"

        # Add exception if present
        if record.exc_info:
            msg += f"\n{self.formatException(record.exc_info)}"

        return msg


class StructuredLogger(logging.LoggerAdapter):
    """
    Logger adapter that adds structured context to all log messages.

    Usage:
        logger = StructuredLogger(logging.getLogger(__name__), {"component": "auth"})
        logger.info("User logged in", user_id=123)
    """

    def __init__(self, logger: logging.Logger, extra: Optional[dict] = None):
        super().__init__(logger, extra or {})

    def process(self, msg: str, kwargs: dict) -> tuple:
        # Merge extra context
        extra = {**self.extra, **kwargs.get("extra", {})}

        # Support keyword arguments as extra fields
        for key in list(kwargs.keys()):
            if key not in ("exc_info", "stack_info", "stacklevel", "extra"):
                extra[key] = kwargs.pop(key)

        kwargs["extra"] = extra
        return msg, kwargs


def setup_observability(
    service_name: str,
    service_version: str = "1.0.0",
    log_level: Optional[str] = None,
    otlp_endpoint: Optional[str] = None,
    json_logs: Optional[bool] = None,
    enable_console_export: bool = False,
) -> None:
    """
    Initialize the observability stack for a service.

    Args:
        service_name: Name of the service (used in logs and traces)
        service_version: Version of the service
        log_level: Log level (DEBUG, INFO, WARNING, ERROR). Default from LOG_LEVEL env var.
        otlp_endpoint: OpenTelemetry collector endpoint. Default from OTEL_EXPORTER_OTLP_ENDPOINT env var.
        json_logs: Use JSON format for logs. Default: True in production, False if LOG_LEVEL=DEBUG.
        enable_console_export: Also export traces/logs to console (for debugging).
    """
    global _observability_initialized, _service_name, _service_version

    if _observability_initialized:
        return

    _service_name = service_name
    _service_version = service_version

    # Determine settings from environment
    log_level = log_level or os.environ.get("LOG_LEVEL", "INFO").upper()
    otlp_endpoint = otlp_endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

    if json_logs is None:
        json_logs = log_level != "DEBUG"

    # Configure Python logging
    _configure_logging(service_name, service_version, log_level, json_logs)

    # Configure OpenTelemetry if available
    if OTEL_AVAILABLE:
        _configure_opentelemetry(
            service_name,
            service_version,
            otlp_endpoint,
            enable_console_export
        )

    _observability_initialized = True

    # Log initialization
    logger = get_logger("observability")
    logger.info(
        "Observability initialized",
        service=service_name,
        version=service_version,
        log_level=log_level,
        json_logs=json_logs,
        otel_enabled=OTEL_AVAILABLE,
        otlp_endpoint=otlp_endpoint or "none",
    )


def _configure_logging(
    service_name: str,
    service_version: str,
    log_level: str,
    json_logs: bool,
) -> None:
    """Configure Python logging with appropriate formatter."""

    # Clear existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    # Choose formatter
    if json_logs:
        formatter = JSONFormatter(service_name, service_version)
    else:
        formatter = ReadableFormatter()

    handler.setFormatter(formatter)

    # Configure root logger
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Reduce noise from third-party libraries
    noisy_loggers = [
        "aiohttp", "telegram", "httpx", "httpcore", "urllib3",
        "asyncio", "concurrent", "grpc", "opentelemetry",
    ]
    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def _configure_opentelemetry(
    service_name: str,
    service_version: str,
    otlp_endpoint: Optional[str],
    enable_console_export: bool,
) -> None:
    """Configure OpenTelemetry tracing and logging."""

    # Create resource with service info
    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
        "deployment.environment": os.environ.get("ENVIRONMENT", "development"),
    })

    # Configure tracing
    tracer_provider = TracerProvider(resource=resource)

    if otlp_endpoint:
        # Export to OTLP collector
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    if enable_console_export:
        # Also export to console for debugging
        console_exporter = ConsoleSpanExporter()
        tracer_provider.add_span_processor(BatchSpanProcessor(console_exporter))

    trace.set_tracer_provider(tracer_provider)

    # Configure log export to OTLP if available
    if otlp_endpoint:
        try:
            logger_provider = LoggerProvider(resource=resource)
            log_exporter = OTLPLogExporter(endpoint=otlp_endpoint, insecure=True)
            logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
            set_logger_provider(logger_provider)

            # Add OTEL handler to root logger
            otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
            logging.getLogger().addHandler(otel_handler)
        except Exception as e:
            logging.getLogger("observability").warning(f"Failed to configure OTLP log export: {e}")


def get_logger(name: str, **extra_context) -> StructuredLogger:
    """
    Get a structured logger for the given module/component.

    Args:
        name: Logger name (typically __name__)
        **extra_context: Additional context fields to include in all log messages

    Returns:
        StructuredLogger instance
    """
    base_logger = logging.getLogger(name)
    return StructuredLogger(base_logger, extra_context)
