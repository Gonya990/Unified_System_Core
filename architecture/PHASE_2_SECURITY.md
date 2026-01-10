# Meta-Orchestration Phase 2: Security & RBAC

## 1. Objective

Secure the `TokenBroker` by encrypting stored keys and enforcing Role-Based Access Control (RBAC) to prevent unauthorized token usage.

## 2. Encryption Strategy (At Rest)

### Implementation

- **Algorithm:** AES (Fernet via `cryptography` library).
- **Storage:** Keys stored in `secrets/keys.enc` (replacing `keys.json`).
- **Master Key:** Provided via Environment Variable `UNIFIED_VAULT_KEY`.
  - Key generated once, distributed securely to `pve-antigravity-1`, `macbook`, etc.
  - **Never** stored in git.

### Workflow

1. **Setup:** Admin runs `python setup_vault.py` -> enters keys -> generates `keys.enc`.
2. **Runtime:** `TokenBroker` reads `UNIFIED_VAULT_KEY` -> decrypts `keys.enc` in memory.

## 3. Role-Based Access Control (RBAC)

### Policy File: `config/rbac_policy.yaml`

```yaml
roles:
  researcher:
    allow:
      - provider: openai
        tier: paid
      - provider: gemini
        tier: free
  
  maintenance_bot:
    allow:
      - provider: gemini
        tier: free
      - provider: openrouter
        tier: free

agents:
  OrangeStone: [researcher, maintenance_bot]
  VioletCastle: [admin] # All access
  PinkLake: [maintenance_bot]
```

### Enforcement

- `TokenBroker.get_key(agent_name, provider, tier)`
- If `agent_name` not authorized -> `AccessDeniedError`.

## 4. Audit Logging

- Log every key request: `timestamp | agent | provider | tier | status`.
- Flag anomalies (e.g., 100 requests/min from a maintenance bot).

## 5. Implementation Plan

1. **Dependency:** Add `cryptography` to `pyproject.toml` / `requirements.txt`.
2. **Tooling:** Create `Scripts/Utilities/vault_manager.py` (CLI for encrypt/decrypt).
3. **Broker Update:** Modify `TokenBroker` to support decryption.
4. **RBAC:** Add `check_permission` method to Broker.

## 6. Request for Approval

Please approve this specification to proceed with coding.
