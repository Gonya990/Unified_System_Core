# Observability Integration Guide

Development guidelines for integrating logging, tracing, and metrics into Unified System services.

---

## Quick Start (30 seconds)

```python
# At the top of your service's entry point
from unified_observability import setup_observability, get_logger

# Initialize once at startup
setup_observability(service_name="my-service")

# Get a logger
logger = get_logger(__name__)

# Log with context
logger.info("Request processed", user_id=123, duration_ms=45)
```

That's it. Your service now has:
- Structured JSON logs to stdout
- Trace correlation (if OTEL collector is running)
- Automatic export to Loki/Grafana (if configured)

---

## Table of Contents

1. [Logging Best Practices](#1-logging-best-practices)
2. [Structured Context](#2-structured-context)
3. [Log Levels](#3-log-levels)
4. [Tracing](#4-tracing)
5. [Metrics](#5-metrics)
6. [Error Handling](#6-error-handling)
7. [Performance](#7-performance)
8. [Container Integration](#8-container-integration)
9. [Testing](#9-testing)
10. [Checklist](#10-checklist)

---

## 1. Logging Best Practices

### DO: Log with structured context

```python
# GOOD: Structured, searchable, context-rich
logger.info(
    "Order completed",
    order_id="ORD-123",
    user_id=456,
    total=99.99,
    items_count=3,
)

# BAD: String interpolation, hard to search
logger.info(f"Order ORD-123 completed for user 456, total $99.99, 3 items")
```

### DO: Log at service boundaries

```python
async def handle_request(request):
    logger.info("Request received", endpoint=request.path, method=request.method)

    try:
        result = await process(request)
        logger.info("Request completed", status="success", duration_ms=elapsed)
        return result
    except Exception as e:
        logger.error("Request failed", error=str(e), exc_info=True)
        raise
```

### DO: Include correlation context

```python
from unified_observability import LogContext, set_correlation_id

async def handle_request(request):
    # Set correlation ID from header or generate new one
    correlation_id = request.headers.get("X-Correlation-ID") or set_correlation_id()

    with LogContext(correlation_id=correlation_id, user_id=request.user_id):
        # All logs in this block include correlation_id and user_id
        logger.info("Processing started")
        await do_work()
        logger.info("Processing completed")
```

### DON'T: Log sensitive data

```python
# BAD: Logs passwords, tokens, PII
logger.info("User login", password=password, token=api_token)

# GOOD: Redact or omit sensitive fields
logger.info("User login", user_id=user.id, ip=request.ip)
```

### DON'T: Log in tight loops

```python
# BAD: Floods logs, kills performance
for item in items:  # 10,000 items
    logger.debug(f"Processing item {item.id}")
    process(item)

# GOOD: Log summary or sample
logger.info("Processing batch", count=len(items))
for item in items:
    process(item)
logger.info("Batch complete", count=len(items), duration_ms=elapsed)
```

---

## 2. Structured Context

### Request-scoped context with LogContext

```python
from unified_observability import LogContext

async def api_handler(request):
    with LogContext(
        request_id=request.id,
        user_id=request.user.id,
        tenant_id=request.tenant_id,
    ):
        # All logs automatically include these fields
        await validate(request)      # logs include request_id, user_id, tenant_id
        await process(request)       # logs include request_id, user_id, tenant_id
        await notify(request)        # logs include request_id, user_id, tenant_id
```

### Per-logger context

```python
# Create a logger with permanent context
logger = get_logger(__name__, component="payment", version="2.1")

# All logs from this logger include component and version
logger.info("Payment initiated", amount=100)
# Output: {..., "component": "payment", "version": "2.1", "amount": 100}
```

### Combining contexts

```python
logger = get_logger(__name__, service="checkout")

with LogContext(user_id=123):
    logger.info("Cart loaded", items=5)
    # Output: {..., "service": "checkout", "user_id": 123, "items": 5}
```

---

## 3. Log Levels

| Level | When to Use | Examples |
|-------|-------------|----------|
| **DEBUG** | Development diagnostics, verbose details | Variable values, loop iterations, internal state |
| **INFO** | Normal operations, business events | Request received, order completed, user login |
| **WARNING** | Unexpected but handled situations | Retry attempted, cache miss, deprecated API used |
| **ERROR** | Failures requiring attention | Request failed, database error, external API down |
| **CRITICAL** | System-wide failures | Out of memory, cannot connect to database, data corruption |

### Examples

```python
# DEBUG: Development only, very verbose
logger.debug("Cache lookup", key=cache_key, hit=bool(result))

# INFO: Normal business operations
logger.info("User registered", user_id=user.id, plan="free")

# WARNING: Something unexpected but handled
logger.warning("Rate limit approaching", current=95, limit=100, user_id=user.id)

# ERROR: Something failed, needs attention
logger.error("Payment failed", order_id=order.id, error=str(e), exc_info=True)

# CRITICAL: System is broken
logger.critical("Database connection pool exhausted", available=0, max=100)
```

### Environment-based levels

```bash
# Development: verbose logging
LOG_LEVEL=DEBUG python my_service.py

# Production: normal logging
LOG_LEVEL=INFO python my_service.py

# Debugging production issue: temporary verbose
LOG_LEVEL=DEBUG python my_service.py  # then revert
```

---

## 4. Tracing

### Automatic function tracing

```python
from unified_observability import trace_function, trace_async_function

@trace_function()
def process_payment(order_id: str, amount: float):
    # Automatically creates a span named "module.process_payment"
    validate_order(order_id)
    charge_card(amount)
    return receipt

@trace_async_function()
async def fetch_user(user_id: int):
    # Async functions work too
    return await db.get_user(user_id)
```

### Manual spans for complex operations

```python
from unified_observability import get_tracer

tracer = get_tracer(__name__)

async def complex_operation(data):
    with tracer.start_as_current_span("complex_operation") as span:
        span.set_attribute("data.size", len(data))

        # Child span for sub-operation
        with tracer.start_as_current_span("validate"):
            validate(data)

        # Another child span
        with tracer.start_as_current_span("transform"):
            result = transform(data)
            span.set_attribute("result.size", len(result))

        return result
```

### Propagating context across services

```python
from unified_observability import inject_context, extract_context

# When making outbound HTTP requests
async def call_external_service(data):
    headers = {}
    inject_context(headers)  # Adds traceparent header

    async with aiohttp.ClientSession() as session:
        response = await session.post(url, json=data, headers=headers)
        return response

# When receiving requests (in your framework middleware)
def trace_middleware(request, handler):
    context = extract_context(dict(request.headers))
    with tracer.start_as_current_span("handle_request", context=context):
        return handler(request)
```

---

## 5. Metrics

### Counter: Track occurrences

```python
from unified_observability import create_counter

request_counter = create_counter(
    "http_requests_total",
    description="Total HTTP requests",
)

async def handle_request(request):
    request_counter.add(1, {
        "method": request.method,
        "endpoint": request.path,
        "status": "success",
    })
```

### Histogram: Track distributions

```python
from unified_observability import create_histogram, timed_operation

latency_histogram = create_histogram(
    "request_duration_ms",
    description="Request latency in milliseconds",
    unit="ms",
)

async def handle_request(request):
    with timed_operation(latency_histogram, {"endpoint": request.path}):
        return await process(request)
```

### Gauge: Track current values

```python
from unified_observability import create_gauge

# Gauge with callback - called periodically
def get_queue_size():
    return len(work_queue)

queue_gauge = create_gauge(
    "work_queue_depth",
    callback=get_queue_size,
    description="Current items in work queue",
)
```

### Pre-built service metrics

```python
from unified_observability import ServiceMetrics

metrics = ServiceMetrics("my-service")

async def handle_request(request):
    metrics.request_count.add(1, {"endpoint": request.path})

    start = time.perf_counter()
    try:
        result = await process(request)
        duration = (time.perf_counter() - start) * 1000
        metrics.request_latency.record(duration, {"endpoint": request.path})
        return result
    except Exception as e:
        metrics.error_count.add(1, {"error_type": type(e).__name__})
        raise
```

---

## 6. Error Handling

### Always include exc_info for exceptions

```python
try:
    result = risky_operation()
except ValueError as e:
    # GOOD: Includes full traceback
    logger.error("Validation failed", error=str(e), exc_info=True)
    raise

except Exception as e:
    # GOOD: Logs and re-raises with context
    logger.error(
        "Unexpected error",
        operation="risky_operation",
        error=str(e),
        exc_info=True,
    )
    raise
```

### Structured error context

```python
try:
    order = await process_order(order_id, user_id)
except PaymentError as e:
    logger.error(
        "Payment processing failed",
        order_id=order_id,
        user_id=user_id,
        payment_method=e.method,
        error_code=e.code,
        error_message=str(e),
        exc_info=True,
    )
    # Now you can search: error_code="CARD_DECLINED" in Grafana
```

### Error boundaries in async code

```python
async def worker(task_queue):
    while True:
        task = await task_queue.get()
        try:
            with LogContext(task_id=task.id):
                await process_task(task)
                logger.info("Task completed")
        except Exception as e:
            logger.error("Task failed", error=str(e), exc_info=True)
            # Don't crash the worker, continue processing
        finally:
            task_queue.task_done()
```

---

## 7. Performance

### Lazy evaluation for expensive operations

```python
# BAD: expensive_serialize() runs even if DEBUG is disabled
logger.debug(f"Full state: {expensive_serialize(state)}")

# GOOD: Only evaluates if DEBUG is enabled
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("Full state", state=expensive_serialize(state))
```

### Batch logging for high-throughput

```python
# BAD: Log every item
for item in million_items:
    logger.info("Processed", item_id=item.id)

# GOOD: Log batches
batch_size = 1000
for i, item in enumerate(million_items):
    process(item)
    if i % batch_size == 0:
        logger.info("Progress", processed=i, total=len(million_items))

logger.info("Complete", total=len(million_items))
```

### Sampling for very high volume

```python
import random

SAMPLE_RATE = 0.01  # Log 1% of requests

async def handle_request(request):
    should_log = random.random() < SAMPLE_RATE

    if should_log:
        logger.info("Request received", endpoint=request.path)

    result = await process(request)

    if should_log:
        logger.info("Request completed", endpoint=request.path)

    return result
```

---

## 8. Container Integration

### Dockerfile setup

```dockerfile
# Copy and install observability package
COPY infra/observability /tmp/observability
RUN pip install /tmp/observability && rm -rf /tmp/observability

# Set environment defaults
ENV LOG_LEVEL=INFO
ENV PYTHONUNBUFFERED=1
```

### Docker Compose environment

```yaml
services:
  my-service:
    environment:
      - LOG_LEVEL=INFO
      - OTEL_SERVICE_NAME=my-service
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
```

### Health check logging

```python
@app.get("/health")
async def health():
    # DON'T log health checks - they're too frequent
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    # DO log readiness issues
    if not db.is_connected():
        logger.warning("Readiness check failed: database not connected")
        raise HTTPException(503, "Not ready")
    return {"status": "ready"}
```

---

## 9. Testing

### Test logging output

```python
import logging

def test_logs_on_error(caplog):
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            process_invalid_data()

    assert "Validation failed" in caplog.text
    assert "error_code" in caplog.text
```

### Mock observability in tests

```python
from unittest.mock import patch

def test_without_otel():
    with patch("unified_observability.OTEL_AVAILABLE", False):
        # Test runs without OpenTelemetry
        result = my_function()
        assert result is not None
```

### Verify structured fields

```python
import json

def test_structured_logging(caplog):
    with caplog.at_level(logging.INFO):
        logger.info("Test event", user_id=123, action="test")

    # Parse JSON log output
    log_record = json.loads(caplog.records[0].message)
    assert log_record["user_id"] == 123
    assert log_record["action"] == "test"
```

---

## 10. Checklist

### New Service Checklist

- [ ] Add `unified-observability` to dependencies
- [ ] Call `setup_observability()` at startup
- [ ] Use `get_logger(__name__)` instead of `logging.getLogger()`
- [ ] Add structured context to all log calls
- [ ] Include `exc_info=True` for all error logs
- [ ] Set `OTEL_SERVICE_NAME` in container config
- [ ] Add health/ready endpoints (without logging)
- [ ] Test logging output in unit tests

### Pre-Production Checklist

- [ ] Verify logs appear in Grafana/Loki
- [ ] Check log volume is reasonable (not flooding)
- [ ] Confirm sensitive data is not logged
- [ ] Test error scenarios produce searchable logs
- [ ] Verify traces connect across service calls
- [ ] Set up alerts for ERROR/CRITICAL logs

### Log Review Checklist

- [ ] Can I find all requests for a specific user?
- [ ] Can I trace a request across all services?
- [ ] Can I find all errors in the last hour?
- [ ] Can I see why a specific request failed?
- [ ] Are log messages actionable (not just "error occurred")?

---

## Quick Reference

```python
# Import
from unified_observability import (
    setup_observability,
    get_logger,
    LogContext,
    trace_function,
    trace_async_function,
    create_counter,
    create_histogram,
    ServiceMetrics,
)

# Initialize
setup_observability(service_name="my-service")

# Logger
logger = get_logger(__name__)
logger.info("Event", key="value")
logger.error("Failed", exc_info=True)

# Context
with LogContext(user_id=123):
    logger.info("Scoped log")

# Tracing
@trace_async_function()
async def my_func():
    pass

# Metrics
counter = create_counter("events_total")
counter.add(1, {"type": "click"})
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `OTEL_SERVICE_NAME` | Required | Service name in telemetry |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | None | OTLP collector endpoint (enables export) |
| `ENVIRONMENT` | `development` | Deployment environment tag |
