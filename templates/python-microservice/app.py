#!/usr/bin/env python3
"""
Template Python microservice for Unified System Core.
"""

import os
import logging
from fastapi import FastAPI
from google.cloud import logging as cloud_logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Cloud Logging
client = cloud_logging.Client()
client.setup_logging()

app = FastAPI(title="Microservice Template")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Hello from microservice"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
