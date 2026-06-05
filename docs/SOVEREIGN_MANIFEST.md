# Sovereign Manifest

Machine-readable source: [`config/SOVEREIGN_MANIFEST.yaml`](../config/SOVEREIGN_MANIFEST.yaml)

Human summary:

- **Infrastructure**: any root/sudo/destructive ops → YubiKey.
- **Secrets**: `.env`, SSH, vault → YubiKey.
- **Finance**: new spend → YubiKey; recurring → whitelist only; Moneytor read-only.
- **Self-modify**: manifest/policy changes → YubiKey.

Enforcement: `services/approval-gateway` + `config/policy.json` via `integrations/ag_bridge_policy_hook.js`.
