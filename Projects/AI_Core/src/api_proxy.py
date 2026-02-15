import json
import logging
import os
import time
from pathlib import Path
from typing import Any, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel

logger = logging.getLogger(__name__)

app = FastAPI(title="Vibranium AI Gateway (OpenAI Compatible)")

# Global reference to the bot/orchestrator/inference
_BOT_INSTANCE = None
_INFERENCE_CLIENT = None
_TOKEN_CACHE: Optional[str] = None


def _load_token_from_env_file() -> Optional[str]:
    global _TOKEN_CACHE
    if _TOKEN_CACHE is not None:
        return _TOKEN_CACHE

    root = Path(__file__).resolve().parents[3]
    candidates = [".env.igor", ".env.local", ".env"]
    keys = {"API_GATEWAY_TOKEN", "COPILOT_API_TOKEN", "API_TOKEN"}

    for name in candidates:
        path = root / name
        if not path.exists():
            continue
        try:
            for raw in path.read_text().splitlines():
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[len("export ") :]
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                if key in keys:
                    value = value.strip().strip("'").strip('"')
                    _TOKEN_CACHE = value
                    return value
        except Exception:
            continue

    _TOKEN_CACHE = None
    return None


def _expected_api_token() -> Optional[str]:
    return (
        os.getenv("API_GATEWAY_TOKEN")
        or os.getenv("COPILOT_API_TOKEN")
        or os.getenv("API_TOKEN")
        or _load_token_from_env_file()
    )


async def require_api_key(request: Request):
    """Optional API key guard. Enabled when API_GATEWAY_TOKEN is set."""
    expected = _expected_api_token()
    if not expected:
        return

    auth = request.headers.get("authorization", "")
    token = None
    if auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()

    if not token:
        token = request.headers.get("x-api-key")

    if not token or token != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")


def _summarize_chat_payload(payload: dict) -> dict[str, Any]:
    """Return a safe summary of a chat request without user content."""
    model = payload.get("model")
    messages = payload.get("messages", [])
    msg_count = len(messages) if isinstance(messages, list) else 0
    total_chars = 0

    if isinstance(messages, list):
        for msg in messages:
            if isinstance(msg, dict):
                content = msg.get("content")
                if isinstance(content, str):
                    total_chars += len(content)

    return {
        "model": model,
        "messages": msg_count,
        "chars": total_chars,
        "stream": payload.get("stream"),
        "temperature": payload.get("temperature"),
    }


@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    """Log sanitized request info for debugging without leaking content."""
    body = b""
    if request.method in {"POST", "PUT", "PATCH"}:
        try:
            body = await request.body()
        except Exception:
            body = b""

    if body:
        # Recreate the request so downstream can read the body
        async def receive():
            return {"type": "http.request", "body": body, "more_body": False}

        request = Request(request.scope, receive)

        if request.url.path == "/v1/chat/completions":
            try:
                payload = json.loads(body.decode("utf-8"))
                summary = _summarize_chat_payload(payload)
                logger.info(f"[api_proxy] chat_completions request: {summary}")
            except Exception:
                logger.info(f"[api_proxy] chat_completions request: unreadable_json bytes={len(body)}")
        else:
            logger.info(f"[api_proxy] {request.method} {request.url.path} bytes={len(body)}")

    response = await call_next(request)
    return response


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


@app.post("/v1/chat/completions", dependencies=[Depends(require_api_key)])
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


@app.post("/v1/alert", dependencies=[Depends(require_api_key)])
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


@app.post("/v1/execute", dependencies=[Depends(require_api_key)])
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


# Backward-compatible aliases used by older callers/logged errors
def set_bot_instance(bot=None):
    set_context(bot=bot)


def set_inference_client(inference=None):
    set_context(inference=inference)


def run_proxy(port=3030):
    import uvicorn

    logger.info(f"🚀 Starting Vibranium Gateway on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
