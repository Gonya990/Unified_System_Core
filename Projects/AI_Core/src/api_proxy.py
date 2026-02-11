import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

logger = logging.getLogger(__name__)

app = FastAPI(title="Vibranium Mobile Proxy")

# Global reference to the bot/orchestrator
_BOT_INSTANCE = None

class CommandRequest(BaseModel):
    user_id: int
    command: str
    audio_data: Optional[str] = None  # Future voice support

def set_bot_instance(bot):
    global _BOT_INSTANCE
    _BOT_INSTANCE = bot

@app.get("/v1/health")
async def health_check():
    return {"status": "ok", "bot_connected": _BOT_INSTANCE is not None}

@app.post("/v1/execute")
async def execute_command(request: CommandRequest):
    """
    Execute a natural language command from a mobile device or shortcut.
    """
    if not _BOT_INSTANCE:
        raise HTTPException(status_code=503, detail="Bot core not initialized")

    try:
        # We simulate the bot handling the message
        # In ai_telegram_bot_v2.py, handle_message is the entry point.
        # However, for API, we might want to directly call the orchestrator/inference.
        
        # For now, we reuse the query_ollama_with_context or agent_orchestrator
        # To avoid circular imports, we assume _BOT_INSTANCE has the necessary methods.
        
        response = await _BOT_INSTANCE.process_api_command(
            request.user_id, request.command
        )
        return {"response": response}
    except Exception as e:
        logger.error(f"API Command execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def run_proxy(port=8080):
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
