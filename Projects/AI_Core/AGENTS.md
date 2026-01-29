# AI_Core - Agent Knowledge Base

**Generated:** 2026-01-04T11:45:00Z | **Commit:** 0a4ad48 | **Branch:** main

## OVERVIEW

Telegram bot implementing a **Hybrid AI Orchestration** architecture. Multi-LLM council (Claude/Gemini/OpenAI/Ollama), smart home control, and persistent user memory.

## STRUCTURE

```
AI_Core/
├── src/                    # 46 modules
│   ├── main.py             # Entry: TG bot + service init
│   ├── inference_client.py # "Carpathian Council" multi-LLM
│   ├── config_manager.py   # Fernet-encrypted config
│   ├── firestore_db.py     # Firestore + SQLite fallback
│   ├── ha_controller.py    # Home Assistant bridge
│   └── watchdog.py         # Health + budget monitoring
├── tests/                  # pytest + asyncio
├── config/                 # Encrypted bot_config.json
├── scripts/                # Deployment helpers
└── k8s/                    # Kubernetes manifests
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add LLM provider | `src/inference_client.py` | Update council logic + provider enum |
| Add TG command | `src/main.py` | Register handler in `setup_handlers()` |
| Add HA entity | `src/ha_controller.py` | Uses fuzzy matching for entity names |
| Add user memory | `src/user_context.py` | Extracts "memories" for personalization |
| Add scheduled task | `src/daily_scheduler.py` | Morning digest, nudges |
| Fix persistence | `src/firestore_db.py` | Check both Firestore AND SQLite paths |
| Debug budget | `src/watchdog.py` | Flips to Ollama if GCP budget exceeded |

## KEY PATTERNS

### Carpathian Council (Multi-LLM)
```
Hierarchy: Claude (OpenRouter) > OpenAI/Gemini > Ollama (local)
- Queries multiple providers in parallel
- Selects winner by hierarchy rank
- Auto-fallback on failure
```

### Resilient Persistence
```
Primary: Google Firestore (cross-node sync)
Fallback: SQLite (offline/local dev)
Always handle both paths in CRUD operations
```

### Lazy Dependency Loading
Heavy imports use lazy loading to prevent circular deps and reduce startup time. Pattern:
```python
def get_heavy_module():
    from heavy_module import HeavyClass
    return HeavyClass()
```

## CONVENTIONS

- **Encryption**: API keys stored via Fernet, derived from TG bot token
- **Russian-first**: Digests, notifications default to Russian
- **Async everywhere**: Use `async/await`, never blocking IO
- **Type hints**: Required on all public functions

## ANTI-PATTERNS (THIS PROJECT)

| Forbidden | Why |
|-----------|-----|
| Direct env var access | Use `ConfigManager` for encrypted config |
| Blocking HTTP calls | Use `aiohttp` or async clients |
| Raw Firestore access | Use `FirestoreDB` wrapper for fallback logic |
| Hardcoded entity names | Use `HAController.fuzzy_match()` |

## COMMANDS

```bash
# Dev
cd Projects/AI_Core
uv run python -m src.main           # Start bot locally

# Test
uv run pytest tests/ -v             # Run all tests
uv run pytest tests/test_core.py    # Single file

# Deploy
./scripts/deploy_bot.sh             # Remote deployment
systemctl --user restart ai-bot     # Restart service
```

## NOTES

- **Budget watchdog**: Monitors GCP spend, auto-switches to Ollama if threshold exceeded
- **Systemd service**: `ai-bot.service` in `infra/`
- **Config location**: `config/bot_config.json` (encrypted)
- Test naming: `test_{func}_with_{condition}_returns_{expected}`
