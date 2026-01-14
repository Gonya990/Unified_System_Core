# Identity Vault (Сейф Личности)

Directory: `/secure_vault`
Security Level: **HIGH (Local Only)**

## ⛔️ ACCESS RESTRICTED

This directory contains sensitive biometric data and cryptographic keys.
**NEVER COMMIT THIS DIRECTORY TO GIT.**
**NEVER UPLOAD CONTENTS TO CLOUD STORAGE.**

## Structure

- `/keys`: Private/Public RSA keys for signing content (Proof of Ownership).
- `/biometrics`: Local storage for voice clones (e.g., XTTS latents) and face references.

## Protocols

1. **Local Sovereign**: All "Thinking" models (LLMs) treat this data as read-only and local.
2. **Signature**: All content produced by the factory is signed with `private_key.pem`.
3. **No-Leak**: The `IdentityManager` script checks that these paths are excluded from any upload manifests.
