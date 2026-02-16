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

## Toolchain & DevOps

### Git Providers (используются оба)
- **GitHub** (`github.com/Unified-system-Core`, `github.com/Gonya990`) — основной код: `Unified_System_Core`, `antibridge_fixed`, PRs, Issues.
- **GitLab** (`gitlab.com/Gonya990`) — `~/Documents` трекается как GitLab-репо (`Documents.git`), содержит вложенные GitHub-репо как submodules/nested repos.
- **Правило**: НЕ удалять ни один `.git`. Оба провайдера активны и нужны.

### GitKraken (VS Code + MCP)
- GitKraken workspace **"My_Home"** настроен через VS Code extension.
- Доступны 26+ MCP-инструментов: `mcp_gitkraken_git_*` (status, branch, log, diff, add, commit, push, checkout, stash, blame, worktree), `mcp_gitkraken_issues_*`, `mcp_gitkraken_pull_request_*`, `mcp_gitkraken_gitlens_*`.
- Поддерживает оба провайдера: `provider="github"` и `provider="gitlab"`.
- Для Issues/PRs: `mcp_gitkraken_issues_assigned_to_me`, `mcp_gitkraken_pull_request_assigned_to_me`.
- Для code review: `mcp_gitkraken_gitlens_start_review`, `mcp_gitkraken_pull_request_create_review`.
- Для начала работы: `mcp_gitkraken_gitlens_start_work` (Issue → Branch → Checkout).

### GitHub MCP (прямой доступ)
- GitHub API через `mcp_io_github_git_*`: repos, issues, PRs, commits, branches, code search.
- Аккаунт: **Gonya990** (Igor, Unified-system-Core org).
- Используй `mcp_io_github_git_list_issues`, `mcp_io_github_git_create_pull_request`, `mcp_io_github_git_search_code` и т.д.

### Chromium depot_tools
- Расположение: `~/depot_tools/` (528 МБ), в PATH.
- Содержит: `gclient`, `gn`, `autoninja`, `cipd`, `fetch`, `git-cl` и другие утилиты Chromium.
- **НЕ удалять** — используется для Chromium-совместимых проектов.

### CLI Tools (установлены)
| Инструмент | Путь | Назначение |
|---|---|---|
| `git` 2.50+ | system | VCS, LFS поддержка (`git-lfs`) |
| `gcloud` | `/opt/homebrew/bin/gcloud` | GKE, Cloud Run, Firebase |
| `kubectl` | `/opt/homebrew/bin/kubectl` | Kubernetes cluster mgmt |
| `pm2` | `/opt/homebrew/bin/pm2` | Process manager (Node/Python) |
| `ruff` | venv | Python linter/formatter |
| `pytest` | venv | Python test framework |
| `depot_tools/*` | `~/depot_tools/` | Chromium build tools |

### Docker Compose Services
- `content-factory`, `mail-intelligence`, `dashboard`, `gmail-agent`, `markitdown-mcp` — всё в `docker-compose.yml`.

## Integration Points
- Home Assistant (HA REST), Yandex Alice webhook on port `8090`, TokenBroker for key rotation, Tailscale mesh, GKE + Cloud Server, PM2-managed services.
- Content Factory AI providers: ElevenLabs (voice), Runway/Luma/Kling (video), Suno (music) — setup notes in `Projects/Content_Factory/API_SETUP_GUIDE.md`.

## Security
- Secrets live in `.env*`, `Secrets/`, and `secure_vault/`; do not commit or echo sensitive values.
- Identity/Vault logic in `Scripts/Security/identity_manager.py` (Argon2id + RSA).
- TokenBroker-backed keys are referenced by placeholder values `PLEASE_SET_IN_TOKENBROKER` in `Projects/Content_Factory/.env.ai_template`.

## Repository Map
| Директория | Remote | Провайдер |
|---|---|---|
| `~/Documents/` | `gitlab.com/Gonya990/Documents.git` | GitLab |
| `~/Documents/Unified_System_Core/` | `github.com/Unified-system-Core/Unified_System_Core.git` | GitHub |
| `~/Documents/ag_bridge/` | `github.com/KostaGorod/ag_bridge.git` | GitHub |
| `~/depot_tools/` | `chromium.googlesource.com/chromium/tools/depot_tools.git` | Chromium |
