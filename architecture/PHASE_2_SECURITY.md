# Meta-Orchestration Phase 2: Security & RBAC

## 1. Objective

Secure the `TokenBroker` by encrypting stored keys and enforcing Role-Based Access Control (RBAC) to prevent unauthorized token usage.

## 2. Encryption Strategy (At Rest)

### Implementation

- **Algorithm:** AES-256-GCM (AEAD via `cryptography` library)
- **Key Derivation:** Argon2id (memory-hard, side-channel resistant)
  - Parameters: `memory=65536 KB`, `iterations=3`, `parallelism=4`
  - Fallback: PBKDF2-SHA256 with 600,000 iterations (OWASP 2023)
  - **Rationale:** Argon2id resists GPU/ASIC brute-force attacks that PBKDF2 is vulnerable to.
    Modern password managers (1Password, Bitwarden) use Argon2. Winner of Password Hashing
    Competition (2015). Adds `argon2-cffi` dependency (~50KB, C extension via wheel).
- **Nonce Handling:** 96-bit random nonce per encryption (cryptographically secure RNG)
- **Storage Format:** `salt (16B) || nonce (12B) || ciphertext || tag (16B)`
- **Storage Location:** `secrets/keys.enc` (replacing `keys.json`)
- **Master Key:** Provided via Environment Variable `UNIFIED_VAULT_KEY`
  - Key generated once, distributed securely to `pve-antigravity-1`, `macbook`, etc.
  - **Never** stored in git

### Post-Quantum Posture

- AES-256 provides 128-bit security margin against Grover's algorithm
- Hybrid Kyber wrapping reserved for future enhancement (NIST PQC)
- Current symmetric encryption is quantum-resistant for foreseeable future

### Workflow

1. **Setup:** Admin runs `python setup_vault.py` -> enters keys -> derives key via Argon2id -> generates `keys.enc`
2. **Runtime:** `TokenBroker` reads `UNIFIED_VAULT_KEY` -> derives key -> decrypts `keys.enc` in memory
3. **Re-encryption:** New nonce generated on every write (safe with AES-GCM)

## 2.1 SessionStore Encryption

SessionStore delegates encryption to TokenBroker's vault mechanism. No separate encryption layer.

- **At-rest:** Session data encrypted with same AES-256-GCM + Argon2id
- **In-memory:** Decrypted only during active session
- **Key isolation:** Each session can use derived subkey (HKDF) if multi-tenant

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

1. **Dependency:** Add `cryptography` and `argon2-cffi` to `pyproject.toml` / `requirements.txt`.
2. **Tooling:** Create `Scripts/Utilities/vault_manager.py` (CLI for encrypt/decrypt).
3. **Broker Update:** Modify `TokenBroker` to support decryption.
4. **RBAC:** Add `check_permission` method to Broker.

## 6. Request for Approval

Please approve this specification to proceed with coding.
