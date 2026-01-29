"""
Distributed tracing with OpenTelemetry.

Provides decorators and utilities for adding tracing to functions
and propagating trace context across service boundaries.
"""

import functools
import asyncio
from typing import Any, Callable, Optional, TypeVar, ParamSpec

# Type hints
P = ParamSpec("P")
R = TypeVar("R")

# OpenTelemetry imports (graceful fallback)
try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode, SpanKind
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
    from opentelemetry.propagate import inject, extract
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None


def get_tracer(name: str) -> Any:
    """
    Get an OpenTelemetry tracer for the given instrumentation scope.

    Args:
        name: Tracer name (typically __name__)

    Returns:
        Tracer instance (or NoopTracer if OTEL not available)
    """
    if OTEL_AVAILABLE and trace:
        return trace.get_tracer(name)

    # Return a noop tracer if OTEL not available
    return NoopTracer()


class NoopSpan:
    """No-operation span for when OpenTelemetry is not available."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def set_attribute(self, key: str, value: Any) -> None:
        pass

    def set_status(self, status: Any) -> None:
        pass

    def record_exception(self, exception: Exception) -> None:
        pass

    def add_event(self, name: str, attributes: Optional[dict] = None) -> None:
        pass

    def is_recording(self) -> bool:
        return False


class NoopTracer:
    """No-operation tracer for when OpenTelemetry is not available."""

    def start_as_current_span(
        self,
        name: str,
        kind: Any = None,
        attributes: Optional[dict] = None,
        **kwargs,
    ):
        return NoopSpan()

    def start_span(self, name: str, **kwargs):
        return NoopSpan()


def trace_function(
    name: Optional[str] = None,
    attributes: Optional[dict] = None,
    record_exception: bool = True,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to trace a synchronous function.

    Args:
        name: Span name (defaults to function name)
        attributes: Additional span attributes
        record_exception: Whether to record exceptions in the span

    Usage:
        @trace_function()
        def my_function(arg1, arg2):
            return result

        @trace_function(name="custom.span.name", attributes={"key": "value"})
        def my_function():
            pass
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        span_name = name or f"{func.__module__}.{func.__qualname__}"
        tracer = get_tracer(func.__module__)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with tracer.start_as_current_span(
                span_name,
                attributes=attributes,
            ) as span:
                try:
                    result = func(*args, **kwargs)
                    if OTEL_AVAILABLE:
                        span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    if OTEL_AVAILABLE and record_exception:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise

        return wrapper
    return decorator


def trace_async_function(
    name: Optional[str] = None,
    attributes: Optional[dict] = None,
    record_exception: bool = True,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to trace an async function.

    Args:
        name: Span name (defaults to function name)
        attributes: Additional span attributes
        record_exception: Whether to record exceptions in the span

    Usage:
        @trace_async_function()
        async def my_async_function(arg1, arg2):
            return await something()
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        span_name = name or f"{func.__module__}.{func.__qualname__}"
        tracer = get_tracer(func.__module__)

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with tracer.start_as_current_span(
                span_name,
                attributes=attributes,
            ) as span:
                try:
                    result = await func(*args, **kwargs)
                    if OTEL_AVAILABLE:
                        span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    if OTEL_AVAILABLE and record_exception:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise

        return wrapper
    return decorator


def inject_context(carrier: dict) -> dict:
    """
    Inject the current trace context into a carrier (e.g., HTTP headers).

    Args:
        carrier: Dictionary to inject context into

    Returns:
        The carrier with trace context injected

    Usage:
        headers = {}
        inject_context(headers)
        # headers now contains traceparent, tracestate, etc.
        response = requests.get(url, headers=headers)
    """
    if OTEL_AVAILABLE:
        inject(carrier)
    return carrier


def extract_context(carrier: dict) -> Any:
    """
    Extract trace context from a carrier (e.g., incoming HTTP headers).

    Args:
        carrier: Dictionary containing trace context

    Returns:
        Context object that can be used with trace.set_span_in_context()

    Usage:
        # In a web framework request handler
        ctx = extract_context(request.headers)
        with tracer.start_as_current_span("handle_request", context=ctx):
            process_request()
    """
    if OTEL_AVAILABLE:
        return extract(carrier)
    return None


class SpanContext:
    """
    Context manager for creating a span with automatic error handling.

    Usage:
        with SpanContext("operation_name", attributes={"key": "value"}) as span:
            span.add_event("processing_started")
            result = do_something()
            span.set_attribute("result_count", len(result))
    """

    def __init__(
        self,
        name: str,
        tracer_name: str = __name__,
        kind: Optional[Any] = None,
        attributes: Optional[dict] = None,
    ):
        self.name = name
        self.tracer = get_tracer(tracer_name)
        self.kind = kind
        self.attributes = attributes
        self._span = None

    def __enter__(self):
        kwargs = {}
        if self.attributes:
            kwargs["attributes"] = self.attributes
        if self.kind and OTEL_AVAILABLE:
            kwargs["kind"] = self.kind

        self._span = self.tracer.start_as_current_span(self.name, **kwargs)
        return self._span.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and OTEL_AVAILABLE and self._span:
            # Record the exception
            span = self._span.__enter__()
            span.record_exception(exc_val)
            span.set_status(Status(StatusCode.ERROR, str(exc_val)))

        if self._span:
            return self._span.__exit__(exc_type, exc_val, exc_tb)
        return False


# HTTP client instrumentation helpers
def traced_request(
    method: str,
    url: str,
    tracer_name: str = __name__,
    **kwargs,
) -> dict:
    """
    Create span attributes for an HTTP request.

    Usage:
        with SpanContext("http.request", attributes=traced_request("GET", url)):
            response = requests.get(url)
    """
    return {
        "http.method": method,
        "http.url": url,
        "http.scheme": url.split("://")[0] if "://" in url else "http",
    }
