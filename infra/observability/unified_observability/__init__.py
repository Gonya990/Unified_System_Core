"""
Unified Observability Module - OpenTelemetry-based logging, tracing, and metrics.

Install in your service:
    pip install unified-observability  # or add to requirements.txt

Usage:
    from unified_observability import setup_observability, get_logger

    # Initialize at service startup
    setup_observability(service_name="my-service")

    # Get a logger
    logger = get_logger(__name__)
    logger.info("Service started", extra={"user_id": 123})
"""

from .logger import (
    setup_observability,
    get_logger,
    StructuredLogger,
    LogContext,
    set_correlation_id,
    get_correlation_id,
)
from .tracing import (
    get_tracer,
    trace_function,
    trace_async_function,
    inject_context,
    extract_context,
    SpanContext,
)
from .metrics import (
    get_meter,
    create_counter,
    create_histogram,
    create_gauge,
    timed_operation,
    timed,
    ServiceMetrics,
)

__all__ = [
    # Logger
    "setup_observability",
    "get_logger",
    "StructuredLogger",
    "LogContext",
    "set_correlation_id",
    "get_correlation_id",
    # Tracing
    "get_tracer",
    "trace_function",
    "trace_async_function",
    "inject_context",
    "extract_context",
    "SpanContext",
    # Metrics
    "get_meter",
    "create_counter",
    "create_histogram",
    "create_gauge",
    "timed_operation",
    "timed",
    "ServiceMetrics",
]

__version__ = "1.0.0"
