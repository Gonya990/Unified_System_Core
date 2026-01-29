# Unified System Observability

OpenTelemetry-based logging, tracing, and metrics for all Unified System services.

## Quick Start

### 1. Start the Observability Stack

```bash
cd infra/observability
docker compose up -d
```

This starts:
- **OpenTelemetry Collector** (ports 4317/4318) - Receives telemetry from services
- **Loki** (port 3100) - Log aggregation
- **Tempo** (port 3200) - Distributed tracing
- **Prometheus** (port 9090) - Metrics storage
- **Grafana** (port 3000) - Dashboards (admin/admin)

### 2. Integrate with Your Service

```python
from infra.observability import setup_observability, get_logger

# Initialize at startup
setup_observability(
    service_name="my-service",
    service_version="1.0.0",
)

# Get a logger
logger = get_logger(__name__)

# Log with structured context
logger.info("User logged in", user_id=123, action="login")
logger.error("Failed to process request", request_id="abc", exc_info=True)
```

### 3. Add Tracing

```python
from infra.observability import trace_function, trace_async_function, get_tracer

# Decorator for sync functions
@trace_function()
def process_data(data):
    return transform(data)

# Decorator for async functions
@trace_async_function()
async def fetch_user(user_id: int):
    return await db.get_user(user_id)

# Manual spans
tracer = get_tracer(__name__)
with tracer.start_as_current_span("custom_operation") as span:
    span.set_attribute("key", "value")
    result = do_something()
```

### 4. Add Metrics

```python
from infra.observability import create_counter, create_histogram, ServiceMetrics

# Create individual metrics
request_counter = create_counter("http_requests_total", "Total HTTP requests")
latency_histogram = create_histogram("request_duration_ms", "Request latency")

# Record metrics
request_counter.add(1, {"method": "GET", "endpoint": "/api/users"})
latency_histogram.record(150.5, {"endpoint": "/api/users"})

# Or use pre-defined service metrics
metrics = ServiceMetrics("my-service")
metrics.request_count.add(1, {"endpoint": "/api/health"})
metrics.error_count.add(1, {"error_type": "validation"})
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | None (disabled) |
| `OTEL_SERVICE_NAME` | Service name in telemetry | From setup_observability() |
| `LOG_LEVEL` | Log level (DEBUG, INFO, WARNING, ERROR) | INFO |
| `ENVIRONMENT` | Deployment environment | development |

## Log Context

Add contextual information to all logs within a scope:

```python
from infra.observability import LogContext, get_logger

logger = get_logger(__name__)

# Context manager adds fields to all logs in scope
with LogContext(user_id=123, request_id="abc-123"):
    logger.info("Processing started")  # Includes user_id and request_id
    process_request()
    logger.info("Processing complete")  # Also includes context
```

## JSON Log Format

In production (LOG_LEVEL != DEBUG), logs are JSON formatted:

```json
{
  "timestamp": "2026-01-29T12:00:00.000Z",
  "level": "INFO",
  "logger": "my.module",
  "message": "User logged in",
  "service": "my-service",
  "version": "1.0.0",
  "trace_id": "abc123...",
  "span_id": "def456...",
  "correlation_id": "xyz789",
  "user_id": 123,
  "action": "login"
}
```

## Grafana Dashboards

Access Grafana at http://localhost:3000 (admin/admin).

Pre-configured dashboards:
- **Service Overview**: Health status, error logs, request metrics
- **Explore**: Query logs, traces, and metrics

### Query Examples

**Loki (Logs)**:
```logql
{service_namespace="unified-system"} |= "ERROR"
{service_name="ai-telegram-bot"} | json | level="ERROR"
```

**Prometheus (Metrics)**:
```promql
sum(rate(unified_system_requests_total[5m])) by (service)
histogram_quantile(0.95, rate(unified_system_request_duration_ms_bucket[5m]))
```

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  AI Telegram    │     │  Bridge Server  │     │  Mail Processor │
│     Bot         │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │    OTLP (gRPC/HTTP)   │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  OpenTelemetry         │
                    │  Collector             │
                    │  (port 4317/4318)      │
                    └───────────┬────────────┘
                                │
           ┌────────────────────┼────────────────────┐
           │                    │                    │
           ▼                    ▼                    ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │    Loki     │     │   Tempo     │     │ Prometheus  │
    │   (Logs)    │     │  (Traces)   │     │  (Metrics)  │
    │  port 3100  │     │  port 3200  │     │  port 9090  │
    └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                               ▼
                    ┌────────────────────────┐
                    │       Grafana          │
                    │     (port 3000)        │
                    │   Dashboards & Alerts  │
                    └────────────────────────┘
```

## Troubleshooting

### Logs not appearing in Loki

1. Check OTEL collector is running: `docker compose ps`
2. Verify endpoint: `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`
3. Check collector logs: `docker compose logs otel-collector`

### Traces not appearing in Tempo

1. Ensure tracing is enabled (OTEL_AVAILABLE = True in logs)
2. Check Tempo is healthy: `curl http://localhost:3200/ready`

### High memory usage

Adjust limits in `otel-collector-config.yaml`:
```yaml
processors:
  memory_limiter:
    limit_mib: 256  # Reduce from 512
```

## Dependencies

Install with pip:
```bash
pip install -r infra/observability/requirements.txt
```

Or add to your service's pyproject.toml:
```toml
[project.optional-dependencies]
observability = [
    "opentelemetry-api>=1.22.0",
    "opentelemetry-sdk>=1.22.0",
    "opentelemetry-exporter-otlp-proto-grpc>=1.22.0",
]
```
