# Full System Revision - 2026-05-15

## Scope

This revision covers the current `/workspace` checkout of `Unified_System_Core`, its declared submodules, the uploaded PDFs, and the security/dependency signals that could be verified from this cloud machine.

The review intentionally avoids printing secret values. Findings below distinguish between current-tree evidence, git-history evidence, and configuration risk.

## Repository inventory

### Main repository

- Remote: `github.com/Unified-system-Core/Unified_System_Core`
- Working branch for this revision: `cursor/full-revision-architecture-9bc5`
- Main subsystems:
  - `Projects/AI_Core/` - Telegram/AI orchestration bot, Home Assistant, Google integrations, multi-provider LLM usage.
  - `Projects/Content_Factory/` - autonomous media/content generation pipeline.
  - `Projects/ChatKit_Dashboard/` - Next.js/Firebase dashboard.
  - `Projects/Bybit_Bot/`, `Projects/Bybit_Arb_Bot/` - trading/crypto automation.
  - `Scripts/Orchestration/`, `Scripts/Production_Factory/`, `Scripts/Security/` - operational automation.
  - `functions/`, `unified/`, `dataconnect/`, `firebase.json`, `firestore.rules` - Firebase Functions/Data Connect/Firestore.
  - `infra/` - Docker, Kubernetes, Tailscale, deployment manifests.
  - `Agent_Context/`, `docs/`, `skills/`, `.claude/` - agent rules, knowledge, architecture, skills.

### Submodules initialized and included

| Path | Remote | Pinned revision/status |
| --- | --- | --- |
| `External_Tools/Stack/mcp_agent_mail` | `https://github.com/Dicklesworthstone/mcp_agent_mail.git` | Declared in `.gitmodules`; directory was not present as a checked submodule in `git submodule status` output. |
| `infra/cliproxyapi/src` | `https://github.com/router-for-me/CLIProxyAPI` | `d47b7dc...` (`v6.6.93`) |
| `Projects/AI_Core/antibridge` | `https://github.com/Unified-system-Core/antibridge.git` | `a55073e...` |
| `Projects/AI_Core/gk-cli` | `https://github.com/gitkraken/gk-cli.git` | `5e5eeeb...` (`v3.1.1`) |
| `tools/chrome-devtools-mcp` | `https://github.com/ChromeDevTools/chrome-devtools-mcp.git` | `d459266...` |
| `Projects/Content_Factory/src/lip_sync/Wav2Lip` | `https://github.com/Rudrabha/Wav2Lip.git` | `bac9a81...` |
| `Projects/Content_Factory/src/live_portrait` | `https://github.com/KwaiVGI/LivePortrait.git` | `60d7501...` |

## Uploaded document facts

Files reviewed from `/home/ubuntu/.cursor/projects/workspace/uploads`:

- `Vibranium_Presentation_06bc.pdf` - readable text. Main strategic source for "Sovereign Core", "Vibranium", "U-Core", "Sovereign-as-a-Service", "blind cloud", local orchestrator, agent swarm, PII scrubbing, cost guardrails, digital notary/content factory, and consumer "Vibranium Home Plug".
- `The_Sovereign_Core_-_Pitch_Deck_cad2.pdf` - extraction returned page markers only; no reliable factual text.
- `Mercantile_20230430_0115171864_a8de.pdf` - password-protected; not readable in this pass.
- `332716927-1233802008_a4a0.pdf` - Hebrew road/toll-style tax invoice with 2023 billing context.
- `89404160_28_1_1_2d52.pdf` - Hebrew mobile/telecom VAT invoice with late-2024 billing context.
- `6030591241116463145-...5784.pdf` - Hebrew daily suspended-scaffold safety inspection checklist with 2024 operational context.

Planning interpretation:

- Only `Vibranium_Presentation_06bc.pdf` materially supports the software/product architecture narrative.
- The invoices and construction checklist are useful for document-store classification, compliance hygiene, and jurisdictional context, but they do not validate revenue, product security, or architecture claims.
- Pitch claims such as "blind cloud", "Pegasus-level", RSA/HMAC strength, and 30% OPEX reduction must be converted into explicit threat models, controls, measurements, and acceptance tests before they are used in product commitments.

## Verified high-priority findings

### 1. Firestore rules are expired and were previously open

`firestore.rules` currently allows every document read/write only while:

```text
request.time < timestamp.date(2026, 3, 16)
```

Today is 2026-05-15, so these rules now deny all client requests if deployed as-is. Before the expiry date they allowed unauthenticated full database access. This is both an availability risk and a data-exposure design flaw.

Recommended action:

1. Replace the blanket rule with collection-specific authenticated rules.
2. Add emulator tests for every collection.
3. Add `firebase emulators:exec` or rules-unit tests to CI.
4. Deploy only after validating current production rules and backup state.

### 2. Redacted secret scanning found current-tree and history findings

Commands run:

- `gitleaks dir /workspace --redact`
- `gitleaks detect --source /workspace --redact`

Current tree:

- Total redacted findings: `110`
- Top rule classes:
  - `generic-api-key`: `77`
  - `openai-api-key`: `19`
  - `curl-auth-header`: `9`
  - `jwt`: `3`
  - `huggingface-access-token`: `1`
  - `gcp-api-key`: `1`
- Top current files by finding count:
  - `dataconnect/seed_data.gql`
  - `Projects/AI_Core/src/emails_4_months.json`
  - `docs/SMARTTHINGS_FIX_GUIDE.md`
  - `Projects/ChatKit_Dashboard/.next/...`
  - `infra/INTEGRATION_GUIDE.md`
  - `Reports/email_actions.json`
  - `Projects/AI_Core/config/gmail_credentials.json`

Git history:

- Total redacted findings: `357`
- Top rule classes:
  - `generic-api-key`: `201`
  - `openai-api-key`: `38`
  - `telegram-bot-api-token`: `34`
  - `gcp-api-key`: `31`
  - `curl-auth-header`: `22`
  - `linear-api-key`: `11`
  - `jwt`: `9`
  - `private-key`: `7`
  - `github-pat`: `2`
  - `huggingface-access-token`: `1`
  - `github-fine-grained-pat`: `1`

Tracked sensitive-looking files:

- `Projects/AI_Core/.env.igor`
- `Projects/AI_Core/config/gmail_credentials.json`
- `Projects/AI_Core/gmail_credentials.json`
- `Projects/Content_Factory/insta_session.json`
- `config/gmail_credentials.json`
- `config/google_drive_credentials.json`
- `gmail_credentials_template.json`

Safe structural read confirmed that `Projects/AI_Core/.env.igor` contains keys named like Telegram, Gemini, OpenAI, OpenRouter, SerpAPI, Linear, Home Assistant, and Notion credentials. Values were not printed.

Recommended action:

1. Treat all current and historical scanner hits as compromised until individually proven false-positive.
2. Rotate Telegram, OpenAI, Gemini, OpenRouter, SerpAPI, Linear, Home Assistant, Notion, Google OAuth, Instagram session, GitHub PAT, Hugging Face, and GCP keys/tokens referenced by current files or history.
3. Move live secrets to Google Secret Manager, GitHub Actions secrets, or the existing TokenBroker/vault flow.
4. Delete local `.env*`, OAuth client/session/token files, and generated cache files from tracked history where feasible.
5. Add a blocking pre-commit and CI secret scan.

### 3. Generated Next.js artifacts and caches are committed

Tracked generated/build-like artifacts count:

- `466` paths matching `.next/`, `dist/`, `build/`, `__pycache__`, `venv`, or similar patterns.

Most are under `Projects/ChatKit_Dashboard/.next/`. Gitleaks also flagged `.next` cache/manifests. Even when many are false positives, committed build output increases repository noise, leaks environment-derived metadata, and makes scans harder to trust.

Recommended action:

1. Add `.next/`, `.turbo/`, build caches, and local runtime artifacts to `.gitignore`.
2. Remove generated artifacts from the index.
3. Rebuild in CI/deploy only.

### 4. Node dependency advisories

Command: `npm audit --json` in each lockfile-backed Node project.

| Project | Critical | High | Moderate | Low | Total | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `functions` | 2 | 22 | 7 | 12 | 43 | Genkit/Firebase/Google Cloud chain; some fixes are semver-major or unavailable. |
| `unified` | 1 | 7 | 4 | 9 | 21 | `fast-xml-parser`, `flatted`, `protobufjs`, Firebase chain. |
| `Projects/ChatKit_Dashboard` | 1 | 1 | 2 | 0 | 4 | `next` request smuggling, `protobufjs` RCE, `postcss` XSS. |
| `Projects/antigravity-vscode` | 0 | 3 | 2 | 0 | 5 | `minimatch`, `picomatch`, `flatted`, `ajv`, `brace-expansion`. |
| `Projects/AI_Core/antibridge` | 0 | 4 | 1 | 0 | 5 | `lodash`, `serialize-javascript`, `fast-uri`, webpack chain. |
| `Projects/AI_Core/antibridge/backend` | 2 | 1 | 1 | 1 | 5 | `simple-git` command execution, `basic-ftp` path traversal, `path-to-regexp` ReDoS. |
| `tools/chrome-devtools-mcp` | 2 | 11 | 4 | 1 | 18 | Dev-tool submodule; includes `basic-ftp`, Hono, rate limit, `protobufjs`. |

Recommended action:

1. Prioritize deployed runtime surfaces: `Projects/ChatKit_Dashboard`, `functions`, `unified`, then `antibridge/backend`.
2. Upgrade `next`, `protobufjs`, `postcss`, Firebase/Genkit packages, and backend transitive chains.
3. Re-run `npm audit --audit-level=high` in CI.

### 5. Python dependency advisories and resolution gaps

`pip-audit` was installed and `python3.12-venv` had to be added to the cloud machine to run resolved scans.

Resolved scan results:

| Requirements file | Result |
| --- | --- |
| `LLM_Council/requirements.txt` | 47 deps, 0 vulns |
| `Projects/AI_Core/requirements.txt` | 105 deps, 0 vulns |
| `Projects/AI_Core/requirements_voice.txt` | 63 deps, 0 vulns |
| `Projects/Bybit_Arb_Bot/requirements.txt` | 27 deps, 0 vulns |
| `Projects/Copilot_SDK_Experiment/requirements.txt` | 8 deps, 0 vulns |
| `Projects/Bybit_Bot/requirements.txt` | 59 deps, 0 vulns |
| `Scripts/openai_mcp_server/requirements_simple.txt` | 17 deps, 0 vulns |
| `Scripts/openai_mcp_server/requirements.txt` | 75 deps, 0 vulns |
| `Scripts/monitoring/requirements.txt` | 22 deps, 0 vulns |
| `Projects/Content_Factory/requirements.txt` | `pillow 11.3.0`, 6 vulns, fixes include `12.1.1`/`12.2.0` |
| `Projects/Content_Factory/src/live_portrait/requirements_base.txt` | `onnx`, `gradio`, `pillow`; 22 vulns |
| `Projects/Content_Factory/src/live_portrait/requirements.txt` | `onnx`, `gradio`, `transformers`, `pillow`; 40 vulns |
| `templates/python-microservice/requirements.txt` | `fastapi`, `starlette`; 3 vulns |
| `Projects/Content_Factory/src/live_portrait/requirements_macOS.txt` | failed on Linux/Python 3.12 because `onnxruntime-silicon==1.16.3` is macOS-specific |
| `Projects/Content_Factory/src/lip_sync/Wav2Lip/requirements.txt` | failed because old numpy metadata generation is incompatible with this Python 3.12 environment |

Recommended action:

1. Pin and hash all Python dependencies with `pip-tools` or `uv`.
2. Split platform-specific requirement files and scan them in matching runners.
3. Upgrade `pillow`, `onnx`, `gradio`, `transformers`, `fastapi`, and `starlette`.
4. Replace or containerize legacy Wav2Lip dependencies with a Python version they support.

### 6. Python static security scan findings

Command: `bandit -r Projects Scripts LLM_Council templates External_Tools unified.py check_secrets.py`

Totals:

- Lines scanned: `69,245`
- High severity: `21`
- Medium severity: `115`
- Low severity: `638`

Representative high findings:

- `Projects/AI_Core/src/ai_telegram_bot_v2.py` - `subprocess` with `shell=True`.
- `Projects/AI_Core/src/modules/proxmox_manager.py` - `subprocess` with `shell=True`.
- `Projects/Content_Factory/src/audio/voice_generator.py` - MD5 used in a security-sensitive context per Bandit.
- `Projects/Content_Factory/src/lip_sync/Wav2Lip/*` - multiple shell invocation findings.
- `Scripts/Maintenance/check_openai_updates.py` and `Scripts/generate_audit.py` - shell invocation findings.
- `External_Tools/nodriver/nodriver_daemon.py` - permissive `chmod 777` on socket path.

Recommended action:

1. Replace shell string calls with argument arrays and explicit allowlists.
2. Add a command policy layer for admin/remote execution paths.
3. Triage generated/third-party submodules separately from first-party code.

### 7. Go vulnerability scan findings

Target: `infra/cliproxyapi/src`

Command: `govulncheck ./...`

Result:

- `29` reachable vulnerabilities from one module and the Go standard library.
- `11` additional vulnerabilities in imported packages not apparently called.
- `4` additional vulnerabilities in required modules not apparently called.
- Example affected areas:
  - `net/http/httputil` reverse proxy behavior, fixed in Go `1.25.10`.
  - `golang.org/x/net` HTTP/2 issue, fixed in `v0.53.0`.
  - `crypto/tls`, `crypto/x509`, `net/http`, `net`, `os/syscall` standard-library findings.

Recommended action:

1. Build `infra/cliproxyapi/src` with a patched Go toolchain (`>=1.25.10` based on scan output).
2. Upgrade `golang.org/x/net` and related modules.
3. Re-run `govulncheck ./...` in the submodule.

### 8. Insecure and permissive runtime/deployment defaults

Observed evidence:

- `Projects/AI_Core/src/google_auth.py` sets `OAUTHLIB_INSECURE_TRANSPORT=1`.
- `Projects/AI_Core/k8s/deployment-gke.yaml` also sets `OAUTHLIB_INSECURE_TRANSPORT=1`.
- Multiple Docker/Kubernetes manifests use `:latest` tags.
- `docker-compose.yml` bind-mounts `./gcp-service-account.json` into the Gmail agent.
- Tailscale/device docs and archived setup notes contain operational metadata that can help targeting if the repo is broadly shared.

Recommended action:

1. Remove insecure OAuth transport outside local development.
2. Pin images by immutable digest for production.
3. Replace local service-account JSON mounts with Workload Identity or Secret Manager.
4. Move device/IP/personally identifying operational docs to a private vault.

## Tooling and environment gaps

Missing at start of audit:

- `uv`
- `ruff`
- `pytest`
- `gitleaks`
- `trivy`
- `bandit`
- `pip-audit`
- `govulncheck`
- `python3.12-venv`

Installed during this audit on the ephemeral cloud machine:

- `pip-audit`
- `bandit`
- `python3.12-venv`
- `govulncheck`
- `gitleaks`

Recommended permanent Cloud Agent environment setup:

```text
Install uv, ruff, pytest, pip-audit, bandit, gitleaks, trivy, govulncheck, python3.12-venv, and Go >= 1.25.10. Pre-cache npm and Python audit dependencies. Validate that scans can run from /workspace without printing secret values.
```

## Immediate remediation backlog

1. **Emergency secret rotation**
   - Rotate all current and historical credentials flagged by gitleaks or tracked sensitive files.
   - Revoke and recreate OAuth clients where client secrets were committed.
2. **Firestore rules**
   - Replace expired blanket rules.
   - Add emulator rules tests.
3. **Remove generated/cache artifacts**
   - Untrack `.next/` and runtime caches.
   - Add ignores and CI rebuild.
4. **Dependency upgrades**
   - Dashboard: `next`, `protobufjs`, `postcss`.
   - Functions/unified: Firebase/Genkit vulnerable chains.
   - Content Factory/LivePortrait: `pillow`, `onnx`, `gradio`, `transformers`.
   - Template: `fastapi`, `starlette`.
   - Go submodule: Go toolchain and `x/net`.
5. **Runtime hardening**
   - Remove `OAUTHLIB_INSECURE_TRANSPORT=1` from deployed paths.
   - Replace `:latest` with digests.
   - Add execution allowlists and approval gates for subprocess/SSH/remote commands.
6. **Audit automation**
   - Add CI jobs for secret scanning, dependency scans, Bandit, govulncheck, Firebase rules tests, and container scanning.
7. **Document governance**
   - Classify PDFs and personal/ops records.
   - Move sensitive records to encrypted Google Drive/Vault with metadata-only references in git.

## Evidence command log

| Area | Command/tool | Result summary |
| --- | --- | --- |
| Git topology | `git submodule update --init --recursive` | Initialized declared submodules. |
| Manifest inventory | `Glob **/{package.json,pyproject.toml,requirements*.txt,...}` | 66 dependency/build manifests after submodule init. |
| Tracked sensitive filenames | `git ls-files | rg ...` | 7 sensitive-looking tracked paths. |
| Current secret scan | `gitleaks dir --redact` | 110 redacted findings. |
| History secret scan | `gitleaks detect --redact` | 357 redacted findings. |
| Node audit | `npm audit --json` | Vulnerabilities in all audited Node projects. |
| Python audit | `pip-audit -r` | Mostly clean; Content Factory/LivePortrait/template vulnerable; platform/legacy scan failures noted. |
| Python static scan | `bandit -r` | 21 high, 115 medium, 638 low findings. |
| Go audit | `govulncheck ./...` | 29 reachable vulnerabilities in `infra/cliproxyapi/src`. |
| Firebase rules | `ReadFile firestore.rules` | Expired blanket rule. |
| Uploaded PDFs | PDF text extraction/read pass | One readable product deck, one empty-text deck, one locked PDF, three operational/invoice docs. |

## Bottom line

The system already contains many useful building blocks for a sovereign/local-first AI control plane: Telegram bot orchestration, Content Factory, VASER-Hub policy concepts, TokenBroker/vault references, Firebase/Google integrations, Tailscale/GKE/HA runbooks, and agent rules. The current repository state is not production-safe without a hardening pass: secrets and generated artifacts must be cleaned up, Firestore rules must be rewritten, dependency vulnerabilities must be upgraded, and audit automation must become a blocking one-button pipeline.
