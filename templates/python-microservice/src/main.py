import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from google.cloud import logging as cloud_logging
from pydantic import BaseModel


# --- UNIFIED LOGGER ---
def setup_unified_logging():
    log_client = cloud_logging.Client()
    log_client.setup_logging()

    # Configure root logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(os.getenv("SERVICE_NAME", "unknown-service"))
    return logger


logger = setup_unified_logging()

# --- APP SETUP ---
app = FastAPI(title=os.getenv("SERVICE_NAME", "Microservice"), version=os.getenv("VERSION", "0.1.0"))


# --- MODELS ---
class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


# --- ROUTES ---
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Liveness/Readiness probe endpoint."""
    return {"status": "ok", "service": os.getenv("SERVICE_NAME", "unknown"), "version": os.getenv("VERSION", "0.1.0")}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log incoming requests."""
    logger.info(f"Requests: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


# --- ENTRYPOINT ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    # In production, use uvicorn CLI or Gunicorn manager
    uvicorn.run(app, host="0.0.0.0", port=port)
