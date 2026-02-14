import logging
import time
from typing import List, Optional, Any

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

app = FastAPI(title="Vibranium AI Gateway (OpenAI Compatible)")

# Global reference to the bot/orchestrator/inference
_BOT_INSTANCE = None
_INFERENCE_CLIENT = None


class AlertRequest(BaseModel):
    summary: str
    description: str
    severity: str  # e.g., "CRITICAL", "ERROR", "WARNING"


class CommandRequest(BaseModel):
    user_id: int
    command: str


# --- OpenAI Compatibility Models ---


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.7


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible endpoint that routes requests to the bot's internal inference client.
    """
    if not _INFERENCE_CLIENT:
        raise HTTPException(status_code=503, detail="Inference engine not initialized")

    try:
        # Convert ChatMessage objects to dicts for InferenceClient
        messages = [{"role": m.role, "content": m.content} for m in request.messages]

        # Call internal inference
        response_text, usage = await _INFERENCE_CLIENT.chat(messages)

        if response_text.startswith("Error:"):
            raise HTTPException(status_code=500, detail=response_text)

        # Build OpenAI-style response
        return {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": response_text},
                    "finish_reason": "stop",
                }
            ],
            "usage": usage,
        }
    except Exception as e:
        logger.error(f"OpenAI Proxy Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/alert")
async def receive_alert(request: AlertRequest):
    """
    Receive alerts from GCP Monitoring and forward to Telegram.
    """
    if not _BOT_INSTANCE:
        raise HTTPException(status_code=503, detail="Bot core not initialized")

    try:
        alert_message = f"🚨 GCP Alert: {request.summary}\n\n{request.description}\n\nSeverity: {request.severity}"
        await _BOT_INSTANCE.send_alert_to_admin(alert_message)
        return {"status": "alert sent"}
    except Exception as e:
        logger.error(f"Alert forwarding error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/health")
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "bot_connected": _BOT_INSTANCE is not None,
        "inference_ready": _INFERENCE_CLIENT is not None,
    }


@app.post("/v1/execute")
async def execute_command(request: CommandRequest):
    """
    Execute a natural language command from a mobile device or shortcut.
    """
    if not _BOT_INSTANCE:
        raise HTTPException(status_code=503, detail="Bot core not initialized")

    try:
        response = await _BOT_INSTANCE.process_api_command(request.user_id, request.command)
        return {"response": response}
    except Exception as e:
        logger.error(f"API Command execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def set_context(bot=None, inference=None):
    global _BOT_INSTANCE, _INFERENCE_CLIENT
    if bot:
        _BOT_INSTANCE = bot
    if inference:
        _INFERENCE_CLIENT = inference


def run_proxy(port=3030):
    import uvicorn

    logger.info(f"🚀 Starting Vibranium Gateway on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

