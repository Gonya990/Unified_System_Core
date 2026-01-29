"""
Unified Observability Module - OpenTelemetry-based logging, tracing, and metrics.

This module provides a consistent observability interface for all services in the
Unified System Core, enabling:
- Structured JSON logging with correlation IDs
- Distributed tracing with OpenTelemetry
- Metrics collection and export
- Easy integration with existing Python services

Usage:
    from infra.observability import setup_observability, get_logger

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
)
from .tracing import (
    get_tracer,
    trace_function,
    trace_async_function,
    inject_context,
    extract_context,
)
from .metrics import (
    get_meter,
    create_counter,
    create_histogram,
    create_gauge,
)

__all__ = [
    # Logger
    "setup_observability",
    "get_logger",
    "StructuredLogger",
    "LogContext",
    # Tracing
    "get_tracer",
    "trace_function",
    "trace_async_function",
    "inject_context",
    "extract_context",
    # Metrics
    "get_meter",
    "create_counter",
    "create_histogram",
    "create_gauge",
]

__version__ = "1.0.0"
