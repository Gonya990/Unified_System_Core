import logging
import os
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

# Import local modules
try:
    from agent_orchestrator import AgentOrchestrator
    from config_manager import ConfigManager
    from inference_client import InferenceClient
except ImportError:
    import sys

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from agent_orchestrator import AgentOrchestrator
    from config_manager import ConfigManager
    from inference_client import InferenceClient

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BridgeServer")

app = FastAPI(title="Unified Core Bridge", version="1.0.0")
config = ConfigManager()
inference = InferenceClient(config)
orchestrator = AgentOrchestrator(inference)

# Security: Simple token-based auth for Make.com
BRIDGE_TOKEN = os.getenv("BRIDGE_TOKEN", "unified-secret-2026")


class LeadData(BaseModel):
    name: str
    phone: str
    message: Optional[str] = None
    timestamp: Optional[str] = None
    message_id: Optional[str] = None
    source: str = "WhatsApp"


class CommandRequest(BaseModel):
    command: str
    payload: dict[str, Any] = {}


async def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization or authorization != f"Bearer {BRIDGE_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/health")
async def health():
    return {"status": "online", "system": "Unified Core Bridge"}


@app.post("/webhook/lead")
async def handle_lead(lead: LeadData, authorization: Optional[str] = Header(None)):
    await verify_token(authorization)
    logger.info(f"Received lead from {lead.phone} ({lead.name})")

    # Brain processing: Analyze lead importance
    prompt = (
        f"Analyze this business lead and suggest priority (High, Medium, Low):\n"
        f"Source: {lead.source}\n"
        f"Name: {lead.name}\n"
        f"Phone: {lead.phone}\n"
        f"Message: {lead.message}"
    )
    analysis = await inference.complete(prompt)

    # Here we could record to Google Sheets or notify Telegram
    return {"status": "received", "analysis": analysis, "message_id": lead.message_id}


@app.post("/command")
async def execute_command(req: CommandRequest, authorization: Optional[str] = Header(None)):
    await verify_token(authorization)
    logger.info(f"Executing external command: {req.command}")

    if req.command == "sync":
        # Placeholder for triggering vibranium-sync.sh
        return {"status": "sync_triggered"}

    return {"status": "unknown_command"}


if __name__ == "__main__":
    port = int(config.get("BRIDGE_PORT", "8090"))
    logger.info(f"Starting Bridge Server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
