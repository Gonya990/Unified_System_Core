# Data sovereignty and cloud vendor registry

Unified Core separates **where data lives** (sovereignty zones) from **who may automate what** (decision policy). This document is the human-readable index; machine-readable sources live under `Agent_Context/Knowledge_Base/identity/`.

## Canonical files

| File | Purpose |
|------|---------|
| [cloud_vendors.yaml](../../Agent_Context/Knowledge_Base/identity/cloud_vendors.yaml) | Vendors by category, `person_id`, data types, risk, `automation_allowed` |
| [data_map.yaml](../../Agent_Context/Knowledge_Base/identity/data_map.yaml) | Sovereign local / mesh / cloud / forbidden-write zones |
| [decision_policy.yaml](../../Agent_Context/Knowledge_Base/identity/decision_policy.yaml) | Per-person rules including cloud inventory and ads/social bans |
| [registry.yaml](../../Agent_Context/Knowledge_Base/identity/registry.yaml) | Persons, devices, accounts (no secrets) |
| [SOVEREIGN_MANIFEST.yaml](../../config/SOVEREIGN_MANIFEST.yaml) | Root-of-trust domains (finance, secrets, infrastructure) |

## Cloud services discovered in this monorepo

From `firebase.json` and `dataconnect/`:

| Product | Config | Region / notes |
|---------|--------|----------------|
| Firebase Auth | `firebase.json` → `auth` | Google Sign-In brand for Unified System Core |
| Firestore | `firestore` | `europe-west1` |
| Realtime Database | `database` | rules in `database.rules.json` |
| Cloud Functions | `functions` | codebases `default`, `unified` |
| Hosting | `hosting` | `public/` |
| App Hosting | `apphosting` | backend `chatkit-dashboard` → `Projects/ChatKit_Dashboard` |
| Data Connect + Cloud SQL | `dataconnect/dataconnect.yaml` | `unifiedsystemcore`, instance `unifiedsystemcore-fdc`, `us-central1` |
| Remote Config | `remoteconfig.template.json` | — |
| Emulator suite | `emulators` | Local dev only |

GKE manifests under `Projects/AI_Core/k8s/`, `Projects/Bybit_Bot/k8s/`, `infra/k8s/`.

**Secrets** never live in git. [TokenBroker](../../Scripts/Utilities/token_broker.py) reads `~/.config/unified-system/tokens.yaml`; sync via [token-sync.sh](../../Scripts/Orchestration/sync/token-sync.sh).

## Sovereignty zones (summary)

```text
┌─────────────────────┐     ┌──────────────────────┐
│ sovereign_local     │     │ sovereign_mesh       │
│ memory-wiki,        │◄───►│ Tailscale nodes      │
│ identity YAML,      │ SSH │ Mac, gaming, smart,  │
│ TokenBroker vault   │     │ gpu-node, cloud VM   │
└──────────┬──────────┘     └──────────┬───────────┘
           │                           │
           │         read-only         │
           ▼         inventory         ▼
┌─────────────────────────────────────────────────┐
│ cloud_controlled (GCP/Firebase, GKE, Moneytor,  │
│ Bybit) — delete/export → YubiKey                │
└─────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────┐
│ forbidden_agent_write (Meta ads/social HTML,     │
│ bulk marketing, iCloud destructive ops)         │
└─────────────────────────────────────────────────┘
```

## Automation policy highlights

| Rule | Enforcement |
|------|-------------|
| No automated posts to ads/social | `deny_always`: `ads_social.post_create` |
| Cloud delete / export | `require_yubikey`: `cloud.data_export`, `cloud.resource_delete` |
| Cloud inventory | `allow_without_yubikey`: `cloud.inventory_read_only` for Igor |

Categories in `cloud_vendors.yaml`: `hyperscaler`, `apple_icloud`, `google_ecosystem`, `dev_tools`, `comms`, `finance_readonly`, `ads_tracking_spam`, `smart_home`, `email_marketing`.

`automation_allowed` values: `none`, `read_only`, `non_critical_only`, `forbidden`.

## Ingest from Downloads

Safe exports are staged into `identity/_inbox/`:

```bash
./scripts/ingest-downloads-identity.sh --dry-run
./scripts/ingest-downloads-identity.sh
./scripts/ingest-downloads-identity.sh --include-apple-license   # optional apple.md
```

Blocked: Meta Accounts Center HTML (`Центр аккаунтов.html`), recovery codes, certs, vault files. See [SENSITIVE_DO_NOT_IMPORT.md](../../Agent_Context/Knowledge_Base/identity/SENSITIVE_DO_NOT_IMPORT.md).

After review, merge labels into `registry.yaml` — never paste tokens.

## Approval flow

Non-critical allowed actions log to `data/memory-wiki/agent_actions/`. Critical paths use `services/approval-gateway` + YubiKey per `SOVEREIGN_MANIFEST.yaml`.

**Owner:** Igor Goncharenko (`person_id: igor`)  
**Last updated:** 2026-05-15
