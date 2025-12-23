"""
Health Check Server for AI Telegram Bot.
Provides /health endpoint for container orchestration.
"""
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class HealthHandler(BaseHTTPRequestHandler):
    """HTTP handler for health checks."""
    
    # Class-level callback for dynamic health status
    health_callback: Optional[Callable[[], dict]] = None
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/health":
            self._handle_health()
        elif self.path == "/ready":
            self._handle_ready()
        else:
            self.send_error(404)
    
    def _handle_health(self):
        """Return health status."""
        status = {"status": "healthy"}
        if self.health_callback:
            try:
                status.update(self.health_callback())
            except Exception as e:
                status["error"] = str(e)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(status).encode())
    
    def _handle_ready(self):
        """Return readiness status."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ready": true}')


def start_health_server(port: int = 8080, health_callback: Optional[Callable[[], dict]] = None) -> HTTPServer:
    """
    Start the health check HTTP server in a background thread.
    
    Args:
        port: Port to listen on
        health_callback: Optional callback that returns additional health info
    
    Returns:
        The HTTPServer instance
    """
    HealthHandler.health_callback = health_callback
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    
    logger.info(f"Health server started on port {port}")
    return server
