# Repository Revision and One-Button PO Plan

Date: 2026-05-15
Branch: `cursor/repository-audit-po-plan-05a8`
Base: `main`

## Purpose

This report captures a point-in-time revision of the Unified System Core workspace, its registered submodules, uploaded evidence documents, security and dependency surfaces, and a practical architecture for turning future reviews into a one-button PO package.

In this document, "PO" is treated as an approval-ready package: product/project order, owner handoff, or procurement order. If the target PO system is a specific ERP, CRM, Google Docs template, or Product Owner workflow, the final exporter should be mapped to that destination.

## Scope reviewed

### Main repository

- Git remote: `github.com/Unified-system-Core/Unified_System_Core`
- Current branch created for this work: `cursor/repository-audit-po-plan-05a8`
- Monorepo layout includes:
  - `Projects/AI_Core/` - Telegram bot, Home Assistant, LLM, GKE/Kubernetes surfaces.
  - `Projects/Content_Factory/` - media/content pipeline.
  - `Projects/ChatKit_Dashboard/` - Next.js/Firebase App Hosting dashboard.
  - `functions/` and `unified/` - Firebase Functions codebases.
  - `Scripts/` - orchestration, automation, security, and utility scripts.
  - `infra/` - Docker, Kubernetes, Tailscale, and service runtime configuration.
  - `docs/`, `Management/`, `Reports/`, `.beads/`, `.claude/` - process, architecture, task, and agent framework records.

### Registered and initialized submodules

`git submodule update --init --recursive --depth 1` initialized the active submodules pinned by the index:

| Path | Remote | Pinned revision |
| --- | --- | --- |
| `Projects/AI_Core/antibridge` | `https://github.com/Unified-system-Core/antibridge.git` | `a55073e6abac7359da052f785c90b4d283ae2e07` |
| `Projects/AI_Core/gk-cli` | `https://github.com/gitkraken/gk-cli.git` | `5e5eeebf9533db5e2c6c0e849f171d5f3488dfeb` |
| `Projects/Content_Factory/src/lip_sync/Wav2Lip` | `https://github.com/Rudrabha/Wav2Lip.git` | `bac9a81e63ecc153202353372e5724b83d9e6322` |
| `Projects/Content_Factory/src/live_portrait` | `https://github.com/KwaiVGI/LivePortrait.git` | `60d750181002351069b5288381c6f3d38a7b2ae4` |
| `infra/cliproxyapi/src` | `https://github.com/router-for-me/CLIProxyAPI` | `d47b7dc79ae9bd78127d3c0e3837ab55799f4948` |
| `tools/chrome-devtools-mcp` | `https://github.com/ChromeDevTools/chrome-devtools-mcp.git` | `d4592664142c7dccf89da7d9c43a60df72f1ec23` |

Note: `.gitmodules` also lists `External_Tools/Stack/mcp_agent_mail`, but `git submodule status --recursive` did not show it as an active indexed submodule in this checkout. Treat this as repository metadata drift to reconcile.

### Uploaded documents

The uploaded PDFs were inspected with text extraction only. No OCR or password cracking was performed.

| File | Extraction result | Handling note |
| --- | --- | --- |
| `332716927-1233802008_24f7.pdf` | Hebrew toll-road invoice with personal/customer/vehicle data and a small ILS charge. | Contains PII; do not commit or reproduce raw details. |
| `6030591241116463145-...ab26.pdf` | Hebrew daily suspended-scaffold inspection checklist with equipment/site details. | Operational safety record; store in restricted evidence location. |
| `89404160_28_1_1_6012.pdf` | Hebrew telecom invoice with personal/customer/billing data. | Contains PII; do not commit or reproduce raw details. |
| `Mercantile_20230430_0115171864_7af5.pdf` | Password-protected; text extraction failed. | Requires owner-supplied password or bank export before validation. |
| `The_Sovereign_Core_-_Pitch_Deck_0821.pdf` | Image-only or non-extractable text in this environment. | Requires OCR if it must be fact-checked. |
| `Vibranium_Presentation_5e90.pdf` | Russian pitch deck text for Sovereign Core / Vibranium / U-Core. | Claims require independent validation before external use. |

## Tooling actually available in this environment

Available:

- `git`
- `npm`
- `python3`
- `pip` user install path

Installed during the review:

- `pip-audit` 2.10.0, user-local only, to attempt Python dependency auditing.

Not available at review start:

- `uv`
- `pip-audit`
- `gitleaks`
- `trufflehog`
- `firebase`
- `bd`

Environment limitation:

- Python `venv` support is missing (`python3.12-venv` not installed). As a result, `pip-audit` could only audit exact pinned requirements using `--no-deps --disable-pip`; unpinned requirements were reported as unsupported for reliable dependency auditing.

## High-priority findings

### 1. Firestore rules are open until a time cutoff

Path: `firestore.rules`

The rule `allow read, write: if request.time < timestamp.date(2026, 3, 16);` allows broad read/write for anyone with database access during the cutoff window. This is a production blocker and becomes especially dangerous because other code paths store Google token material in Firestore.

Immediate action:

1. Replace the catch-all rule with collection-specific authenticated rules.
2. Add Firebase rules tests before deploy.
3. Require App Check or equivalent for public clients where applicable.

### 2. OAuth token payloads are written to Firestore user documents

Path: `sync_token_to_cloud.py`

The script serializes a local Google token JSON into `users/{id}.google_tokens`. If Firestore rules are permissive or later regress, this exposes refresh-capable user credentials.

Immediate action:

1. Stop storing refresh tokens in client-readable Firestore documents.
2. Move token storage to Secret Manager, a KMS-wrapped vault, or TokenBroker-backed storage.
3. Rotate any token ever synced through this path.

### 3. Tracked credential-shaped files and operational identifiers

Examples:

- `Projects/AI_Core/.env.igor`
- `Projects/AI_Core/config/gmail_credentials.json`
- `Projects/AI_Core/gmail_credentials.json`
- `config/gmail_credentials.json`
- `config/google_drive_credentials.json`
- `.secrets.baseline`
- `Agent_Context/Archive/Sessions/arthur_tablet_setup/SECRET_ACCESS.md`

Some values may be placeholders, examples, or already revoked, but the repository normalizes tracking credential-shaped artifacts. This increases the probability of future real-secret exposure.

Immediate action:

1. Move all real credentials to Secret Manager, TokenBroker, or local ignored paths.
2. Convert committed credential files to redacted templates where possible.
3. Run historical secret scanning and rotate anything ever exposed.

### 4. Next.js build output is tracked

Path family: `Projects/ChatKit_Dashboard/.next/`

The repository tracks generated `.next` build/dev cache artifacts. This creates noise, increases repo size, and can accidentally capture build-time environment values.

Immediate action:

1. Add `.next/` ignore coverage at repo and dashboard level.
2. Remove tracked `.next` files in a dedicated cleanup commit.
3. Rebuild in CI/App Hosting instead of storing generated output.

### 5. Kubernetes ConfigMap contains database credentials

Path: `Projects/Bybit_Bot/k8s/configmap.yaml`

`database_url` includes a PostgreSQL username and password in a `ConfigMap`. ConfigMaps are not secret storage.

Immediate action:

1. Move database credentials into a Kubernetes `Secret` or external secret operator.
2. Reference the secret from the deployment via `valueFrom.secretKeyRef`.
3. Rotate the credential if it has ever pointed to a real database.

### 6. Historical security incident details are tracked

Path: `Reports/email_actions.json`

The report includes detailed text about exposed GCP service-account material, project identifiers, and GitHub URLs. Even when historical, this gives attackers a map of likely assets and previous failure modes.

Immediate action:

1. Redact operational identifiers from tracked incident mail dumps.
2. Keep detailed incident records in a restricted evidence store.
3. Record only sanitized postmortems in the public repository.

### 7. Docker Compose encourages local key bind mounts

Path: `docker-compose.yml`

The `gmail-agent` service mounts `./gcp-service-account.json` into the container and sets `GOOGLE_APPLICATION_CREDENTIALS`. This encourages long-lived JSON keys beside the repository.

Immediate action:

1. Prefer workload identity in cloud.
2. Use Docker/Kubernetes secrets or Secret Manager access at runtime.
3. Do not keep service-account JSON files at repo root.

### 8. Risky command execution and deserialization patterns

Examples:

- `Projects/AI_Core/antibridge/backend/services/AntigravityBridge.js` uses dynamic execution patterns, including `eval`.
- `Projects/AI_Core/antibridge/backend/routes/*.js` use shell command execution.
- `Scripts/Orchestration/deploy/remote-update.sh` disables SSH host key checking.
- `Projects/Content_Factory/src/live_portrait/src/utils/video.py` uses `shell=True`.
- `Projects/Content_Factory/src/live_portrait/src/utils/io.py` and related dependency code load pickle files.
- `Projects/Content_Factory/src/lip_sync/Wav2Lip/**` invokes `ffmpeg` through shell strings.

Immediate action:

1. Treat vendored AI/media repos as untrusted execution zones.
2. Use argument lists instead of shell strings for first-party scripts.
3. Keep pickle loading restricted to trusted local artifacts.
4. Restore SSH host key verification or pin known hosts for remote deploy flows.

## Dependency audit results

### npm audit

Command shape used:

```bash
npm audit --omit=dev --json
```

Summary:

| Path | Vulnerabilities |
| --- | --- |
| `functions/` | 31 total: 12 low, 4 moderate, 13 high, 2 critical |
| `unified/` | 15 total: 9 low, 2 moderate, 3 high, 1 critical |
| `Projects/ChatKit_Dashboard/` | 4 total: 2 moderate, 1 high, 1 critical |
| `Projects/AI_Core/antibridge/backend/` | 5 total: 1 low, 1 moderate, 1 high, 2 critical |
| `Projects/antigravity-vscode/` | 0 reported |
| `Projects/AI_Core/antibridge/` | 0 reported |
| `tools/chrome-devtools-mcp/` | 0 reported |

Notable packages flagged by npm audit included `next`, `protobufjs`, `fast-xml-parser`, `basic-ftp`, `simple-git`, `path-to-regexp`, and transitive Google/Genkit/OpenTelemetry dependencies.

### Python audit

Command shape used where possible:

```bash
python3 -m pip_audit -r <requirements.txt> --no-deps --disable-pip --format json
```

Results:

- `Projects/Content_Factory/src/live_portrait/requirements.txt` reported `transformers==4.38.0` with 18 vulnerability records and fixed version `4.48.0` listed for the sampled advisories.
- Most other requirement files are not exact-pinned, for example `python-telegram-bot>=20.7`, so `pip-audit --no-deps --disable-pip` refused to audit them reliably.
- Full Python dependency auditing requires either:
  - installing `python3.12-venv` and running `pip-audit` with resolver support, or
  - using `uv`/lockfiles with exact pinned versions, or
  - generating fully hashed lock files with `pip-compile`.

## Repository and documentation drift

Observed drift:

- `CLAUDE.md`, `SYSTEM_MAP.md`, and management docs reference `Scripts/Orchestration/full_sync.sh`, but the repository contains `Scripts/Orchestration/sync.sh`.
- Workspace rules reference `Scripts/Production_Factory/`, but this path is not present in the checkout.
- `.gitmodules` lists `External_Tools/Stack/mcp_agent_mail`, but it was not active in `git submodule status --recursive`.
- `.github/workflows/deploy.yaml` invokes `python3 scripts/security/scan_release.py`, but the repository path is `Scripts/Security/scan_release.py`. This is likely to fail on Linux because of case sensitivity.
- Google Drive sync code uses a hardcoded macOS local path and pickle token storage: `Projects/Content_Factory/src/two_chimps/sync_context.py`.
- Agent Mail project names and hub URLs appear in multiple docs/scripts and should be centralized.

## Target architecture: one-button revision to PO

The goal is a reproducible workflow that turns repository state plus Google Drive evidence into an approval-ready package.

```text
Operator / GitHub workflow dispatch
        |
        v
One-button orchestrator
        |
        +--> Repository inventory
        |       - git status, current SHA, submodule SHAs
        |       - manifests, deployments, Firebase config, task records
        |
        +--> Evidence intake
        |       - uploaded docs
        |       - Google Drive folder
        |       - local rules and policy files
        |
        +--> Audit engines
        |       - npm audit
        |       - pip-audit / uv audit
        |       - secret scanner
        |       - Firebase rules tests
        |       - Docker/Kubernetes scanners
        |       - custom repo drift checks
        |
        +--> Risk register
        |       - JSON evidence index
        |       - Markdown executive report
        |       - remediation backlog
        |
        +--> PO builder
        |       - Google Docs template or local Markdown template
        |       - cost/risk/owner sections
        |       - sign-off checklist
        |
        +--> Approval gate
                - Beads task
                - Agent Mail broadcast
                - GitHub PR / issue
                - optional export to Drive PDF
```

## Step-by-step implementation plan

### Phase 1 - Define local rules and evidence contract

Create a versioned policy folder, for example `policy/po_factory/`, with:

1. `local_rules.yaml`
   - allowed repositories and submodule policy
   - forbidden tracked file patterns
   - required scanners
   - severity thresholds
   - PII handling rules
2. `drive_mapping.yaml`
   - Google Drive folder IDs
   - document categories
   - retention labels
   - which documents require OCR
3. `po_template.md`
   - summary
   - validated facts
   - risks
   - approvals
   - required tools/configuration
   - implementation checklist

Recommended initial rules:

- No real `.env`, credential JSON, service-account key, OAuth token, or browser session file in git.
- No generated `.next/`, build cache, or debug artifact in git.
- Firestore must not use catch-all public read/write rules.
- K8s credentials must be in `Secret` or external secret references, not `ConfigMap`.
- Any uploaded PII evidence must be summarized and redacted in repo artifacts.

### Phase 2 - Install and standardize tools

Required local/CI tools:

| Tool | Purpose | Configuration |
| --- | --- | --- |
| `git` | repo/submodule inventory | already available |
| `npm` | JS dependency audit | use `npm audit --omit=dev --json` |
| `uv` or `python3-venv + pip-audit` | Python dependency audit | install `uv`; generate lockfiles where missing |
| `gitleaks` or `trufflehog` | secret scanning, including history | add repo config and CI job |
| Firebase CLI | rules tests and deploy validation | configure `.firebaserc`, emulator tests, service account/WIF |
| `trivy` or Anchore | container/SBOM scanning | use in GitHub Actions and local script |
| `kubeconform`, `kube-score`, or `conftest` | Kubernetes policy checks | include rule for ConfigMap credential blocks |
| `bd` | Beads task creation | configure `.beads/config.yaml` and sync remote |
| Google Drive API client | Drive evidence upload/export | use service account or OAuth with least privilege |

Cloud-agent environment recommendation:

- Add `uv`, `firebase-tools`, `gitleaks`, `trivy`, `kubeconform`, `bd`, and `python3.12-venv` to the base image/startup setup so each future audit does not repeat local installation work.

### Phase 3 - Build the orchestrator

Use `Scripts/Orchestration/one_button_po.sh` as the local button:

```bash
bash Scripts/Orchestration/one_button_po.sh --with-npm-audit --with-pip-audit
```

The initial script should:

1. Create a run folder under `Reports/po_workflow/<run_id>/`.
2. Capture `git status`, `git rev-parse HEAD`, and `git submodule status --recursive`.
3. Capture tracked risk-named file paths without printing secret values.
4. Run optional npm and Python audits into machine-readable files.
5. Produce a local `README.md` for the run.
6. Stop before external side effects unless explicitly passed `--drive-sync` or `--create-beads`.

### Phase 4 - Wire Google Drive

Create a dedicated Drive hierarchy:

```text
Unified PO Factory/
  Templates/
  Audit Runs/
    <run_id>/
      evidence/
      scanner-output/
      po-package/
  Approved/
  Rejected/
```

Configuration:

- `GOOGLE_DRIVE_FOLDER_ID` - root folder for generated runs.
- `GOOGLE_APPLICATION_CREDENTIALS` - only for local development; prefer workload identity in CI.
- `GOOGLE_DRIVE_TEMPLATE_ID` - Docs template for the final PO.
- `GOOGLE_DRIVE_SYNC_CMD` - command the one-button script can call after local artifacts are generated.

Implementation guidance:

- Replace hardcoded paths in `sync_context.py` with environment variables.
- Avoid `pickle` token storage for shared automation.
- Use least-privilege Drive scopes; prefer `drive.file` when possible.
- Store generated PII summaries, not raw personal documents, in repo.

### Phase 5 - Wire Beads / Agent Mail / PR

After local evidence is generated:

1. Create or update a Beads issue for each blocking finding.
2. Broadcast the summary to Agent Mail for reviewer assignment.
3. Attach the run artifact path to the PR.
4. Require explicit human approval before any production deploy or PO export.

Suggested Beads task types:

- `security`
- `infra`
- `firebase`
- `dependency`
- `documentation`
- `po-approval`

### Phase 6 - Add GitHub workflow dispatch

Add a manual workflow later, for example `.github/workflows/one-button-po.yaml`, with:

1. `workflow_dispatch` input for target scope.
2. Checkout with submodules.
3. Tool setup.
4. Run `Scripts/Orchestration/one_button_po.sh`.
5. Upload artifacts.
6. Optionally sync to Drive with workload identity.
7. Create/update PR or issue.

Keep deployment separate from audit/PO generation. The PO package should approve production changes, not deploy them implicitly.

## Immediate remediation backlog

1. Replace open Firestore rules with collection-specific rules and tests.
2. Remove tracked `.next/` output and add ignore coverage.
3. Move credential-shaped files to templates or secret storage; run historical secret scan.
4. Move Bybit database URL out of ConfigMap into Secret/external secret.
5. Refactor `sync_token_to_cloud.py` away from Firestore token storage.
6. Fix `.github/workflows/deploy.yaml` path casing for `Scripts/Security/scan_release.py`.
7. Standardize Agent Mail and Beads config in one source of truth.
8. Make Google Drive sync configurable and non-pickle based.
9. Update vulnerable npm packages, starting with critical `protobufjs`, `simple-git`, `basic-ftp`, and dashboard `next`.
10. Add Python lockfile strategy and re-run full Python vulnerability audit.

## Open questions

1. What exact destination does "PO" mean here: Product Owner handoff, project order, procurement order, or another system?
2. Which Google Drive folder should become the canonical evidence root?
3. Which records are allowed to be stored in the repository after redaction, and which must remain Drive-only?
4. Should the one-button workflow create Beads tasks, GitHub issues, or both?
5. Which environment is authoritative for production: GKE, Firebase App Hosting, Docker Compose, or local Tailscale nodes?
