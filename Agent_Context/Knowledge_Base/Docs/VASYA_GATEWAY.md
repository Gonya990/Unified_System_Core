# 🤖 Vasya Gateway — AI Research Assistant

> Load-balanced LLM gateway with Pydantic validation, deployed on `unified-home-core`.

## Architecture

```
┌────────────────┐     ┌──────────────────────────────────────────┐
│  User/Agent    │────▶│  Vasya Gateway (Docker :8080)            │
│  MacBook       │     │  unified-home-core                       │
└────────────────┘     └───────────────┬───────────────────────────┘
                                       │
                       ┌───────────────┼───────────────┐
                       ▼               ▼               ▼
              ┌────────────┐   ┌─────────────┐   Round Robin
              │ Ollama     │   │ Gemini API  │   Load Balancer
              │ :11434     │   │ Cloud       │
              │ qwen2:0.5b │   │ flash-exp   │
              └────────────┘   └─────────────┘
```

## Quick Start

### HTTP API

```bash
curl -X POST http://unified-home-core:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Find Docker resources"}'
```

### Python (AIOS)

```python
from aios_client import AIOSClient
client = AIOSClient()
result = client.query("agent", "llm", {
    "messages": [{"role": "user", "content": "Use vasya_query tool"}],
    "tools": [{"type": "function", "function": {"name": "vasya_query"}}]
})
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate` | POST | Send query, get structured JSON |
| `/health` | GET | Status, mode, providers |
| `/docs` | GET | Swagger UI |
| `/openapi.json` | GET | OpenAPI spec |

## Request Format

```json
{
  "prompt": "your query",
  "model": "qwen2:0.5b",
  "provider": "ollama|gemini",
  "temperature": 0.7
}
```

## Response Format

```json
{
  "results": [
    {"title": "...", "url": "...", "description": "..."}
  ],
  "summary": "...",
  "provider": "ollama|gemini"
}
```

## Deployment

**Location:** `unified-home-core:/home/gonya/projects/vasya-gateway/`

```bash
# Start
cd /home/gonya/projects/vasya-gateway
docker compose up -d

# Logs
docker logs vasya-gateway-vasya-gateway-1

# Health
curl http://localhost:8080/health
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | 100.88.65.71 | Ollama server (igor-gaming-1) |
| `OLLAMA_PORT` | 11434 | Ollama port |
| `DEFAULT_MODEL` | qwen2:0.5b | Default LLM model |
| `LOAD_BALANCE_MODE` | round_robin | `round_robin` or `random` |
| `GEMINI_API_KEY` | - | Gemini API key |

## MCP Integration

Registered as AIOS tool:

```python
@mcp.tool(description="Query Vasya research assistant")
async def vasya_query(prompt: str, model: str = "qwen2:0.5b") -> str:
    ...
```

## Files

| Path | Description |
|------|-------------|
| `src/main.py` | FastAPI gateway |
| `docker-compose.yml` | Container config |
| `Dockerfile` | Build instructions |
| `requirements.txt` | Dependencies |

---

*Last updated: 2025-12-26*
