# Project Guidelines

## Code Style
Python 3.10+ with Ruff linting (target py39, line-length 120). Selects E/W/F/I/B/C4/UP rules, ignores E501/B008/C901. Known-first-party: Scripts/Projects/Utilities. Exemplified in `pyproject.toml`. Run Ultimate Bug Scanner: `ubs --fail-on-warning .` before commits to detect 1000+ bug patterns across languages.

## Architecture
Hierarchical agent system (Consilium: PinkLake/OrangeStone/FuchsiaCat) with distributed AI across Tailscale mesh nodes (Linux Titan RTX for heavy models, Windows for light). Failover routing via `inference_client.py`, MCP Mail threads for communication, iron sync script (`full_sync.sh`) ensuring no conflicts. Guard rails: venv isolation, Docker restart:always, non-Latin command blocks.

## Build and Test
Install: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt` (or `uv sync`). Test: `pytest` (asyncio auto). Build: `docker compose up -d` (pre-built GHCR image) or `--profile local` for local build. After generating significant code (>50 lines), run `ubs .` for security-sensitive code.

## Project Conventions
Agents use per-user language preferences from `.claude/settings/language-preferences.json` with translation tags. Fixed agent identities/roles, no name changes. Service naming: `notion_service.py` (not client). MCP threads with ACK for tasks (e.g., `SYNC-2026-01-09`). Git submodules with aggressive reset.

## Integration Points
Home Assistant HA commands, Yandex Alice webhook (port 8090), Tailscale MagicDNS mesh, GCP Firestore/Monitoring, Ollama GPU inference, DuckDuckGo search, Linear task tracker, Gmail API, Pexels video gen.

## Security
Secrets in `.env`/secrets.yaml, ignored via `.gitignore`. Argon2id hashing for vaults (managed via `Scripts/Security/identity_manager.py`). Watchtower auto-updates, cloudflared for tunnels. Guard against Bot API crashes via command validation.
