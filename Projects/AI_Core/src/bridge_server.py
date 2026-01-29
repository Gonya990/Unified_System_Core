import logging
import os
import sys
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
import uvicorn

# Import local modules
try:
    from config_manager import ConfigManager
    from inference_client import InferenceClient
    from agent_orchestrator import AgentOrchestrator
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from config_manager import ConfigManager
    from inference_client import InferenceClient
    from agent_orchestrator import AgentOrchestrator

# Try to import unified observability
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from infra.observability import setup_observability, get_logger
    OBSERVABILITY_AVAILABLE = True
except ImportError:
    OBSERVABILITY_AVAILABLE = False

# Setup logging with OpenTelemetry support
if OBSERVABILITY_AVAILABLE:
    setup_observability(
        service_name="bridge-server",
        service_version="1.0.0",
    )
    logger = get_logger("BridgeServer")
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
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
    payload: Dict[str, Any] = {}

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
    return {
        "status": "received",
        "analysis": analysis,
        "message_id": lead.message_id
    }

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
