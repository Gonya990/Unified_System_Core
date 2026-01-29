"""
Metrics collection with OpenTelemetry.

Provides utilities for creating and recording metrics (counters, histograms, gauges)
that can be exported to Prometheus or other metrics backends.
"""

import os
import time
import functools
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional, TypeVar, ParamSpec

# Type hints
P = ParamSpec("P")
R = TypeVar("R")

# OpenTelemetry imports (graceful fallback)
try:
    from opentelemetry import metrics
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    OTEL_METRICS_AVAILABLE = True
except ImportError:
    OTEL_METRICS_AVAILABLE = False
    metrics = None

# Global state
_meter_provider_initialized = False


def setup_metrics(
    service_name: str,
    otlp_endpoint: Optional[str] = None,
    export_interval_millis: int = 60000,
) -> None:
    """
    Initialize the metrics provider.

    This is typically called by setup_observability(), but can be called
    separately if only metrics are needed.

    Args:
        service_name: Name of the service
        otlp_endpoint: OTLP collector endpoint for metric export
        export_interval_millis: How often to export metrics (default: 60s)
    """
    global _meter_provider_initialized

    if _meter_provider_initialized or not OTEL_METRICS_AVAILABLE:
        return

    otlp_endpoint = otlp_endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

    resource = Resource.create({SERVICE_NAME: service_name})

    readers = []

    if otlp_endpoint:
        otlp_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
        readers.append(PeriodicExportingMetricReader(
            otlp_exporter,
            export_interval_millis=export_interval_millis,
        ))

    # Optionally add console exporter for debugging
    if os.environ.get("OTEL_METRICS_CONSOLE", "").lower() == "true":
        readers.append(PeriodicExportingMetricReader(
            ConsoleMetricExporter(),
            export_interval_millis=export_interval_millis,
        ))

    if readers:
        meter_provider = MeterProvider(resource=resource, metric_readers=readers)
        metrics.set_meter_provider(meter_provider)

    _meter_provider_initialized = True


def get_meter(name: str, version: str = "1.0.0") -> Any:
    """
    Get an OpenTelemetry meter for the given instrumentation scope.

    Args:
        name: Meter name (typically __name__ or service name)
        version: Version of the instrumentation

    Returns:
        Meter instance (or NoopMeter if OTEL not available)
    """
    if OTEL_METRICS_AVAILABLE and metrics:
        return metrics.get_meter(name, version)
    return NoopMeter()


class NoopMeter:
    """No-operation meter for when OpenTelemetry metrics are not available."""

    def create_counter(self, name: str, **kwargs):
        return NoopCounter()

    def create_up_down_counter(self, name: str, **kwargs):
        return NoopCounter()

    def create_histogram(self, name: str, **kwargs):
        return NoopHistogram()

    def create_observable_gauge(self, name: str, callbacks, **kwargs):
        return NoopGauge()


class NoopCounter:
    """No-operation counter."""

    def add(self, amount: int, attributes: Optional[dict] = None) -> None:
        pass


class NoopHistogram:
    """No-operation histogram."""

    def record(self, amount: float, attributes: Optional[dict] = None) -> None:
        pass


class NoopGauge:
    """No-operation gauge."""
    pass


# Convenience functions for creating metrics
def create_counter(
    name: str,
    description: str = "",
    unit: str = "1",
    meter_name: str = "default",
) -> Any:
    """
    Create a counter metric.

    Counters are monotonically increasing values (e.g., request count, errors).

    Args:
        name: Metric name (e.g., "http_requests_total")
        description: Human-readable description
        unit: Unit of measurement
        meter_name: Meter to use

    Returns:
        Counter instrument

    Usage:
        request_counter = create_counter("http_requests_total", "Total HTTP requests")
        request_counter.add(1, {"method": "GET", "status": "200"})
    """
    meter = get_meter(meter_name)
    return meter.create_counter(name, description=description, unit=unit)


def create_histogram(
    name: str,
    description: str = "",
    unit: str = "ms",
    meter_name: str = "default",
) -> Any:
    """
    Create a histogram metric.

    Histograms record distributions of values (e.g., request latency).

    Args:
        name: Metric name (e.g., "http_request_duration_ms")
        description: Human-readable description
        unit: Unit of measurement
        meter_name: Meter to use

    Returns:
        Histogram instrument

    Usage:
        latency_histogram = create_histogram("http_request_duration_ms", "Request latency")
        latency_histogram.record(150.5, {"endpoint": "/api/users"})
    """
    meter = get_meter(meter_name)
    return meter.create_histogram(name, description=description, unit=unit)


def create_gauge(
    name: str,
    callback: Callable[[], float],
    description: str = "",
    unit: str = "1",
    meter_name: str = "default",
) -> Any:
    """
    Create a gauge metric (observable).

    Gauges represent point-in-time values (e.g., queue depth, memory usage).

    Args:
        name: Metric name (e.g., "queue_depth")
        callback: Function that returns the current value
        description: Human-readable description
        unit: Unit of measurement
        meter_name: Meter to use

    Returns:
        Observable gauge instrument

    Usage:
        def get_queue_size():
            return len(my_queue)
        queue_gauge = create_gauge("queue_depth", get_queue_size, "Current queue depth")
    """
    meter = get_meter(meter_name)

    def wrapped_callback(options):
        try:
            value = callback()
            options.observe(value)
        except Exception:
            pass  # Gauge callbacks should not raise

    return meter.create_observable_gauge(
        name,
        callbacks=[wrapped_callback],
        description=description,
        unit=unit,
    )


@contextmanager
def timed_operation(histogram: Any, attributes: Optional[dict] = None):
    """
    Context manager to time an operation and record it to a histogram.

    Usage:
        latency = create_histogram("operation_duration_ms")
        with timed_operation(latency, {"operation": "fetch_data"}):
            fetch_data()
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        duration_ms = (time.perf_counter() - start_time) * 1000
        histogram.record(duration_ms, attributes or {})


def timed(
    histogram: Any,
    attributes: Optional[dict] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to time a function and record duration to a histogram.

    Usage:
        latency = create_histogram("function_duration_ms")

        @timed(latency, {"function": "process_data"})
        def process_data():
            pass
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with timed_operation(histogram, attributes):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# Common metrics for services
class ServiceMetrics:
    """
    Pre-defined metrics commonly used by services.

    Usage:
        metrics = ServiceMetrics("my-service")
        metrics.request_count.add(1, {"endpoint": "/api/users", "method": "GET"})
        metrics.request_latency.record(150, {"endpoint": "/api/users"})
        metrics.error_count.add(1, {"error_type": "validation"})
    """

    def __init__(self, service_name: str):
        self.service_name = service_name
        meter = get_meter(service_name)

        self.request_count = meter.create_counter(
            f"{service_name}_requests_total",
            description="Total number of requests",
            unit="1",
        )

        self.request_latency = meter.create_histogram(
            f"{service_name}_request_duration_ms",
            description="Request latency in milliseconds",
            unit="ms",
        )

        self.error_count = meter.create_counter(
            f"{service_name}_errors_total",
            description="Total number of errors",
            unit="1",
        )

        self.active_connections = meter.create_up_down_counter(
            f"{service_name}_active_connections",
            description="Number of active connections",
            unit="1",
        )
