import base64
import json
import logging
import os
import time
from itertools import cycle
from typing import Any, Dict, List, Optional

import requests
import yaml

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    AESGCM = None
    PBKDF2HMAC = None

# Argon2id support (preferred over PBKDF2 for new vaults)
try:
    from argon2.low_level import hash_secret_raw, Type

    HAS_ARGON2 = True
except ImportError:
    HAS_ARGON2 = False
    hash_secret_raw = None
    Type = None

logger = logging.getLogger("TokenBroker")


class TokenBroker:
    """
    Upgraded TokenBroker (Phase 2 - Vibranium)
    Encrypted YAML storage using AES-256-GCM.
    Implements Round-Robin rotation, HTTP health checks, and sticky sessions.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TokenBroker, cls).__new__(cls)
        return cls._instance

    def __init__(self, vault_path: str = None, master_key: str = None):
        if hasattr(self, "initialized") and self.initialized:
            return

        if not vault_path:
            # Canonical Location: ~/.config/unified-system/tokens.yaml
            self.vault_path = os.path.expanduser("~/.config/unified-system/tokens.yaml")
        else:
            self.vault_path = vault_path

        # Master Key from ENV or provided
        self.master_key = (
            master_key
            or os.getenv(
                "AGENT_MAIL_TOKEN", "c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb"
            )
        ).encode()

        self.key_store: Dict[str, List[Dict]] = {}
        self._indices: Dict[str, int] = {}
        self._blacklist: Dict[str, float] = {}
        self._blacklist_ttl = 300
        self._session_sticky_keys: Dict[str, str] = {}
        self._last_rotation = time.time()

        self.load_vault()
        self.initialized = True

    def _derive_key(self, salt: bytes, kdf_type: str = "argon2id") -> Optional[bytes]:
        """
        Derive encryption key from master key using Argon2id (preferred) or PBKDF2 (fallback).

        Argon2id parameters (OWASP recommended):
        - memory_cost: 65536 KB (64 MB)
        - time_cost: 3 iterations
        - parallelism: 4 threads
        """
        if not HAS_CRYPTO:
            return None

        # Prefer Argon2id for new vaults (memory-hard, GPU/ASIC resistant)
        if kdf_type == "argon2id" and HAS_ARGON2:
            return hash_secret_raw(
                secret=self.master_key,
                salt=salt,
                time_cost=3,
                memory_cost=65536,  # 64 MB
                parallelism=4,
                hash_len=32,
                type=Type.ID,
            )

        # PBKDF2 fallback for existing vaults or missing argon2-cffi
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(self.master_key)

    def get_key(
        self, provider: str, tier: str = None, session_id: str = None
    ) -> Optional[str]:
        """
        Get a valid API Key for the provider using Round-Robin and Health Checks.
        Supports session stickiness.
        """
        provider = provider.lower()

        # 1. Sticky Session Check
        if session_id and session_id in self._session_sticky_keys:
            sticky_key = self._session_sticky_keys[session_id]
            if sticky_key not in self._blacklist or (
                time.time() - self._blacklist[sticky_key] > self._blacklist_ttl
            ):
                return sticky_key
            else:
                logger.warning(
                    f"TokenBroker: Sticky key for session '{session_id}' is blacklisted. Falling back."
                )
                del self._session_sticky_keys[session_id]

        pool = self.key_store.get(provider, [])

        if tier:
            pool = [k for k in pool if k.get("tier") == tier]

        if not pool:
            return None

        # Filter blacklist
        now = time.time()
        valid_pool = [
            k
            for k in pool
            if k.get("key")
            and (
                k["key"] not in self._blacklist
                or (now - self._blacklist[k["key"]] > self._blacklist_ttl)
            )
        ]

        if not valid_pool:
            logger.error(f"All keys for {provider} are silent.")
            return None

        # Round Robin
        iter_id = f"{provider}_{tier or 'any'}"
        start_idx = self._indices.get(iter_id, 0)
        num_tokens = len(valid_pool)

        for i in range(num_tokens):
            idx = (start_idx + i) % num_tokens
            token_info = valid_pool[idx]

            if self._check_health(token_info):
                self._indices[iter_id] = (idx + 1) % num_tokens
                selected_key = token_info["key"]

                # 2. Set Sticky Key
                if session_id:
                    self._session_sticky_keys[session_id] = selected_key

                # Log usage
                alias = token_info.get("alias", "Unknown")
                logger.info(f"TokenBroker: Provided key '{alias}' for {provider}")
                return selected_key
            else:
                self.report_failure(token_info.get("key", ""), provider)

        return None

    def load_vault(self):
        """Loads and decrypts the token vault. Supports both Argon2id and PBKDF2 vaults."""
        if not os.path.exists(self.vault_path):
            logger.info("Token vault not found. Using legacy fallback.")
            self._try_legacy_import()
            return

        try:
            with open(self.vault_path, "r") as f:
                data = yaml.safe_load(f) or {}

            if not data or "encrypted_data" not in data:
                # Might be old format (unencrypted)
                self.key_store = data
                return

            encrypted_data = bytes.fromhex(data["encrypted_data"])
            nonce = bytes.fromhex(data["nonce"])
            salt = bytes.fromhex(data["salt"])
            kdf_type = data.get("kdf", "pbkdf2")  # Default to pbkdf2 for existing vaults

            key = self._derive_key(salt, kdf_type=kdf_type)
            if key and HAS_CRYPTO and AESGCM:
                aesgcm = AESGCM(key)
                decrypted = aesgcm.decrypt(nonce, encrypted_data, None)
                self.key_store = yaml.safe_load(decrypted)
                logger.info(f"Vault loaded and decrypted ({kdf_type}): {self.vault_path}")
        except Exception as e:
            logger.error(f"TokenBroker: Failed to load vault: {e}")

    def save_vault(self, tokens: Dict[str, List[Dict[str, Any]]] = None, force_kdf: str = None):
        """
        Encrypts and saves the current key_store to YAML.
        Uses Argon2id for new vaults (if available), PBKDF2 as fallback.
        """
        if tokens is not None:
            self.key_store = tokens

        if not HAS_CRYPTO:
            logger.error("Cryptography not available. Cannot save encrypted vault.")
            return

        # Determine KDF type: prefer Argon2id for new vaults
        kdf_type = force_kdf or ("argon2id" if HAS_ARGON2 else "pbkdf2")

        try:
            salt = os.urandom(16)
            nonce = os.urandom(12)
            key = self._derive_key(salt, kdf_type=kdf_type)
            aesgcm = AESGCM(key)

            raw_data = yaml.dump(self.key_store).encode()
            encrypted = aesgcm.encrypt(nonce, raw_data, None)

            data = {
                "encrypted_data": encrypted.hex(),
                "nonce": nonce.hex(),
                "salt": salt.hex(),
                "kdf": kdf_type,
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
            with open(self.vault_path, "w") as f:
                yaml.dump(data, f)

            logger.info(f"Vault saved and encrypted: {self.vault_path}")
        except Exception as e:
            logger.error(f"TokenBroker: Failed to save vault: {e}")

    def _try_legacy_import(self):
        """Attempts to import from old keys.json if vault is missing."""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        legacy_path = os.path.join(base_dir, "secrets", "keys.json")

        if os.path.exists(legacy_path):
            try:
                with open(legacy_path, "r") as f:
                    self.key_store = json.load(f)
                logger.info(f"Imported legacy keys from {legacy_path}. Encrypting now...")
                self.save_vault()
            except Exception as e:
                logger.error(f"TokenBroker: Legacy import failed: {e}")

    def _check_health(self, token_info: Dict[str, Any]) -> bool:
        """Kosta's Health Check: HTTP GET /health, 5s timeout, 3 retries."""
        health_url = token_info.get("health_url")
        if not health_url:
            return True

        for _ in range(3):
            try:
                resp = requests.get(health_url, timeout=5)
                if resp.status_code == 200:
                    return True
            except:
                pass
            time.sleep(0.5)
        return False

    def report_failure(self, key: str, provider: str):
        if not key:
            return
        logger.warning(f"Key failure for {provider}. Cooldown initiated.")
        self._blacklist[key] = time.time()

    def encrypt_value(self, plaintext: str, salt: bytes = b"unified-system-vibranium-salt") -> Optional[str]:
        """Encrypt a single value with AES-256-GCM (unified standard)."""
        if not HAS_CRYPTO or AESGCM is None:
            return None

        key = self._derive_key(salt)
        if not key:
            return None

        nonce = os.urandom(12)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
        return base64.b64encode(nonce + ciphertext).decode()

    def decrypt_value(self, encrypted: str, salt: bytes = b"unified-system-vibranium-salt") -> Optional[str]:
        """Decrypt a single AES-256-GCM encrypted value (unified standard)."""
        if not HAS_CRYPTO or AESGCM is None:
            return None
        try:
            key = self._derive_key(salt)
            if not key:
                return None

            data = base64.b64decode(encrypted)
            nonce, ciphertext = data[:12], data[12:]
            aesgcm = AESGCM(key)
            return aesgcm.decrypt(nonce, ciphertext, None).decode()
        except Exception:
            return None

    def list_available_pools(self) -> Dict[str, Dict[str, int]]:
        """List all provider pools with active/total counts."""
        now = time.time()
        result = {}
        for provider, pool in self.key_store.items():
            if not isinstance(pool, list):
                continue
            active = sum(
                1
                for k in pool
                if k.get("key")
                and (
                    k["key"] not in self._blacklist
                    or (now - self._blacklist.get(k["key"], 0) > self._blacklist_ttl)
                )
            )
            result[provider] = {"total": len(pool), "active": active}
        return result

    def health_check(self) -> Dict[str, Any]:
        """Health check endpoint for monitoring."""
        pools = self.list_available_pools()
        total_keys = sum(p["total"] for p in pools.values())
        active_keys = sum(p["active"] for p in pools.values())
        blacklisted = len(self._blacklist)

        return {
            "status": "healthy" if active_keys > 0 else "degraded",
            "total_keys": total_keys,
            "active_keys": active_keys,
            "blacklisted_keys": blacklisted,
            "encryption_enabled": HAS_CRYPTO,
            "argon2_available": HAS_ARGON2,
            "kdf_preferred": "argon2id" if HAS_ARGON2 else "pbkdf2",
            "last_rotation": self._last_rotation,
            "pools": pools,
            "timestamp": time.time(),
        }

    def rotate_keys(self) -> Dict[str, Any]:
        """Force rotation by clearing blacklist and resetting indices."""
        self._blacklist.clear()
        self._indices.clear()
        self._last_rotation = time.time()
        logger.info("TokenBroker: Forced key rotation completed")
        return {
            "rotated_at": self._last_rotation,
            "blacklist_cleared": True,
            "indices_reset": True,
        }

    def reload_keys(self) -> bool:
        """Reload keys from vault file."""
        try:
            self.load_vault()
            self._last_rotation = time.time()
            logger.info("TokenBroker: Keys reloaded from disk")
            return True
        except Exception as e:
            logger.error(f"TokenBroker: Failed to reload keys: {e}")
            return False

    def check_permission(self, agent_name: str, provider: str, tier: str = None) -> bool:
        """
        RBAC Check: Does this agent have access to this resource?
        Loads from config/rbac_policy.yaml (canonical) or falls back to runtime.
        """
        # 1. Try Canonical Config Folder (Unified_System/config/rbac_policy.yaml)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        canonical_path = os.path.join(root_dir, "config", "rbac_policy.yaml")
        runtime_path = os.path.expanduser("~/.config/unified-system/rbac.yaml")
        
        policy = {}
        for path in [canonical_path, runtime_path]:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        data = yaml.safe_load(f) or {}
                        if "agents" in data:
                            policy.setdefault("agents", {}).update(data["agents"])
                        if "roles" in data:
                            policy.setdefault("roles", {}).update(data["roles"])
                        if not policy.get("default_role") and "default_role" in data:
                            policy["default_role"] = data["default_role"]
                except Exception as e:
                    logger.warning(f"Failed to load RBAC from {path}: {e}")
        
        default_role = policy.get("default_role", "worker")
        agent_role = policy.get("agents", {}).get(agent_name, default_role)
        
        if agent_role == "admin":
            return True
        
        if tier and tier in ["pro", "tier1", "high"]:
            return agent_role in ["admin", "pro_agent"]
            
        return True # Default access for lower tiers


if __name__ == "__main__":
    # Migration CLI
    import sys

    logging.basicConfig(level=logging.INFO)
    broker = TokenBroker()
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        print("🚀 Migrating to encrypted vault...")
        broker._try_legacy_import()
        print("✅ Done.")
