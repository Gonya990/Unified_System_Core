import os
import random
from google.cloud import trace_v2
from google.protobuf.timestamp_pb2 import Timestamp

class UnifiedTracer:
    """
    Simple tracer wrapper for Google Cloud Trace.
    Uses basic implementation since OpenTelemetry can be heavy to set up initially.
    """
    def __init__(self, service_name):
        self.project_id = os.getenv("GCP_PROJECT_ID", "my-home-435112")
        self.client = trace_v2.TraceServiceClient()
        self.service_name = service_name

    def create_span(self, name, span_id=None, trace_id=None):
        if not trace_id:
            trace_id = format(random.getrandbits(128), '032x')
        if not span_id:
            span_id = format(random.getrandbits(64), '016x')

        span = trace_v2.Span(
            name=f"projects/{self.project_id}/traces/{trace_id}/spans/{span_id}",
            span_id=span_id,
            display_name=trace_v2.TruncatableString(value=name),
            start_time=Timestamp()
        )
        span.start_time.GetCurrentTime()
        return span, trace_id

    def end_span(self, span, trace_id):
        span.end_time = Timestamp()
        span.end_time.GetCurrentTime()
        
        try:
            self.client.batch_write_spans(
                name=f"projects/{self.project_id}",
                spans=[span]
            )
            return True
        except Exception:
            # Silent fail to not block main thread
            return False

_tracer = None

def get_tracer(service_name=None):
    global _tracer
    if not _tracer:
        if not service_name:
            service_name = os.getenv("SERVICE_NAME", "unknown-service")
        # Only initialize if explicitly requested or in K8s
        if os.getenv("ENABLE_TRACING", "false").lower() == "true":
             try:
                 _tracer = UnifiedTracer(service_name)
             except Exception:
                 _tracer = None
    return _tracer
