# Project Guidelines

## Code Style
- Python 3.10+; Ruff config in `pyproject.toml` (target py39, line-length 120, E/W/F/I/B/C4/UP, ignores E501/B008/C901).
- Prefer type hints and JSON-structured logs where available (see `COPILOT_INSTRUCTIONS.md`).

## Architecture
- Monorepo: AI bot in `Projects/AI_Core/`, content pipeline in `Projects/Content_Factory/`, orchestration in `Scripts/Orchestration/` and `Scripts/Production_Factory/`.
- Control-plane/security model documented in `docs/architecture/VASER_HUB.md`.
- GKE bot triggers Cloud factory via SSH; env and flows in `RUNBOOK_GKE_CLOUD_FACTORY_CRYPTO_HA.md`.

## Build and Test
- Python tooling (recommended): `uv sync`, `uv run pytest tests/ -v`, `uv run ruff check src/`, `uv run mypy src/` (see `CLAUDE.md`).
- AI Core quick start: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`, then `python -m src.main` (see `Projects/AI_Core/README.md`).
- Docker: `docker compose up -d` (or `--profile local` for local build) in repo root.
- Content Factory run: `./src/pipeline/factory_scheduler.py --auto` from `Projects/Content_Factory/`.
- Content Factory quick test (remote): `python3 test_ai_factory.py` (see `Projects/Content_Factory/QUICKSTART.md`).
- Content Factory scheduler container: `content-factory` service in `docker-compose.yml` runs `Projects/Content_Factory/src/pipeline/factory_scheduler.py --scheduler`.
- Optional scanner: `ubs --fail-on-warning .` before commits (see `.github/copilot-instructions.md`).

## Project Conventions
- Language preferences are per-user in `.claude/settings/language-preferences.json`; when translating, prepend `translation_tag` and omit original text if `strip_original=true`.
- Service naming uses `*_service.py` (e.g., `notion_service.py`, not `*_client.py`).
- Prefer HA env `HA_URL`/`HA_TOKEN` (aliases exist) and factory envs from `RUNBOOK_GKE_CLOUD_FACTORY_CRYPTO_HA.md`.
- Content Factory API keys are expected via TokenBroker placeholders (see `Projects/Content_Factory/.env.ai_template`).

## Integration Points
- Home Assistant (HA REST), Yandex Alice webhook on port `8090`, TokenBroker for key rotation, Tailscale mesh, GKE + Cloud Server, PM2-managed services.
- Content Factory AI providers: ElevenLabs (voice), Runway/Luma/Kling (video), Suno (music) — setup notes in `Projects/Content_Factory/API_SETUP_GUIDE.md`.

## Security
- Secrets live in `.env*`, `Secrets/`, and `secure_vault/`; do not commit or echo sensitive values.
- Identity/Vault logic in `Scripts/Security/identity_manager.py` (Argon2id + RSA).
- TokenBroker-backed keys are referenced by placeholder values `PLEASE_SET_IN_TOKENBROKER` in `Projects/Content_Factory/.env.ai_template`.
