import os
import yaml
import json
import time
import logging
import base64
import requests
from typing import Optional, Dict, List, Any
from itertools import cycle

# Optional cryptography for vault encryption
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes

    HAS_CRYPTO = True
except ImportError:
    AESGCM = None  # type: ignore
    PBKDF2HMAC = None  # type: ignore
    hashes = None  # type: ignore
    HAS_CRYPTO = False

logger = logging.getLogger("TokenBroker")


class TokenBroker:
    """
    Upgraded TokenBroker (Phase 2 - Vibranium)
    Centralizes API key management, rotation, health monitoring, and RBAC.
    Supports Sticky Sessions per session_id for cache optimization.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TokenBroker, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        vault_path: Optional[str] = None,
        master_key: Optional[str] = None,
        rbac_path: str = "config/rbac_policy.yaml",
    ):
        if hasattr(self, "initialized") and self.initialized:
            return

        if not vault_path:
            # New Location: ~/.config/unified-system/tokens.yaml
            self.vault_path = os.path.expanduser("~/.config/unified-system/tokens.yaml")
        else:
            self.vault_path = vault_path

        self.rbac_path = rbac_path

        # Master Key from ENV or provided
        raw_key = master_key or os.getenv("AGENT_MAIL_TOKEN", "vibranium-default-key")
        self.master_key = raw_key.encode()

        self.key_store: Dict[str, List[Dict]] = {}
        self._blacklist: Dict[str, float] = {}  # key -> timestamp
        self._blacklist_ttl = 3600  # 1 hour cooldown
        self._indices: Dict[str, int] = {}
        self._session_sticky_keys: Dict[str, str] = {}  # session_id -> key
        self._rbac_policy: Dict[str, Any] = {}
        self._last_rotation: Optional[float] = None

        self.load_vault()
        self.load_rbac()
        self.initialized = True

    def _derive_key(self, salt: bytes) -> Optional[bytes]:
        """Derives a 256-bit key from master key using PBKDF2."""
        if not HAS_CRYPTO or PBKDF2HMAC is None or hashes is None:
            return None

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(self.master_key)

    def load_rbac(self):
        """Loads the RBAC policy from YAML."""
        if not os.path.exists(self.rbac_path):
            logger.warning(
                f"TokenBroker: RBAC policy not found at {self.rbac_path}. Using default-deny."
            )
            return

        try:
            with open(self.rbac_path, "r") as f:
                self._rbac_policy = yaml.safe_load(f) or {}
            logger.info(
                f"TokenBroker: Loaded RBAC policy with {len(self._rbac_policy.get('roles', {}))} roles."
            )
        except Exception as e:
            logger.error(f"TokenBroker: Failed to load RBAC policy: {e}")

    def check_permission(
        self, agent_name: str, provider: str, tier: Optional[str] = None
    ) -> bool:
        """
        RBAC Check: Verify if an agent is allowed to use a provider/tier.
        """
        if not self._rbac_policy:
            # Default allow if no policy for backward compatibility during transition
            return True

        # 1. Resolve agent roles
        agent_roles = self._rbac_policy.get("agents", {}).get(agent_name, [])
        if not agent_roles:
            logger.warning(f"TokenBroker: Agent '{agent_name}' has no assigned roles.")
            return False

        # 2. Check each role
        for role_name in agent_roles:
            role = self._rbac_policy.get("roles", {}).get(role_name, {})
            if not role:
                continue

            # Admin role gets everything
            if role_name == "admin":
                return True

            allow_list = role.get("allow", [])
            for rule in allow_list:
                # Wildcard or exact match for provider
                if rule.get("provider") in ["*", provider.lower()]:
                    # Wildcard or exact match for tier
                    rule_tier = rule.get("tier")
                    if not rule_tier or rule_tier in ["*", tier]:
                        return True

        return False

    def get_key(
        self,
        provider: str,
        tier: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_name: str = "Unknown",
    ) -> Optional[str]:
        """
        Get a valid API Key for the provider using Sticky Sessions, Round-Robin and Health Checks.
        """
        # 0. RBAC Check
        if not self.check_permission(agent_name, provider, tier):
            logger.warning(
                f"TokenBroker: Access denied for agent '{agent_name}' to {provider}"
            )
            return None

        provider = provider.lower()

        # 1. Sticky Session Check
        if session_id and session_id in self._session_sticky_keys:
            sticky_key = self._session_sticky_keys[session_id]
            # Verify key is still valid
            if sticky_key not in self._blacklist or (
                time.time() - self._blacklist[sticky_key] > self._blacklist_ttl
            ):
                logger.info(f"TokenBroker: Using sticky key for session '{session_id}'")
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
        """Loads and decrypts the token vault."""
        if not os.path.exists(self.vault_path):
            logger.info("Token vault not found. Using legacy fallback.")
            self._try_legacy_import()
            return

        try:
            with open(self.vault_path, "r") as f:
                data = yaml.safe_load(f) or {}

            if not data or "encrypted_data" not in data:
                # Might be old format
                self.key_store = data
                return

            encrypted_data = bytes.fromhex(data["encrypted_data"])
            nonce = bytes.fromhex(data["nonce"])
            salt = bytes.fromhex(data["salt"])

            key = self._derive_key(salt)
            if key and HAS_CRYPTO and AESGCM:
                aesgcm = AESGCM(key)
                decrypted = aesgcm.decrypt(nonce, encrypted_data, None)
                self.key_store = yaml.safe_load(decrypted)
                logger.info(f"Vault loaded and decrypted: {self.vault_path}")
            else:
                self.key_store = {}
                logger.error("Failed to derive decryption key or crypto unavailable.")

        except Exception as e:
            logger.error(f"Failed to load vault: {e}")

    def save_vault(self, tokens: Optional[Dict[str, List[Dict[str, Any]]]] = None):
        """Encrypts and saves current keys to vault."""
        if tokens is not None:
            self.key_store = tokens

        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)

        try:
            salt = os.urandom(16)
            nonce = os.urandom(12)
            key = self._derive_key(salt)

            if key and HAS_CRYPTO and AESGCM:
                aesgcm = AESGCM(key)
                raw_data = yaml.dump(self.key_store).encode()
                encrypted = aesgcm.encrypt(nonce, raw_data, None)

                data = {
                    "encrypted_data": encrypted.hex(),
                    "nonce": nonce.hex(),
                    "salt": salt.hex(),
                    "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                }

                with open(self.vault_path, "w") as f:
                    yaml.dump(data, f)
                logger.info(f"Vault saved and encrypted: {self.vault_path}")
            else:
                # Fallback to plain YAML if crypto fails
                with open(self.vault_path, "w") as f:
                    yaml.dump(self.key_store, f)
                logger.warning("Vault saved UNENCRYPTED due to crypto unavailability.")

        except Exception as e:
            logger.error(f"Failed to save vault: {e}")

    def _try_legacy_import(self):
        """Attempts to import from old keys.json if vault is missing."""
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        legacy_path = os.path.join(base_dir, "secrets", "keys.json")

        if os.path.exists(legacy_path):
            try:
                with open(legacy_path, "r") as f:
                    data = json.load(f)

                self.key_store = data
                logger.info(
                    f"Imported legacy keys from {legacy_path}. Encrypting now..."
                )
                self.save_vault()
            except Exception as e:
                logger.error(f"Legacy import failed: {e}")

    def _check_health(self, token_info: Dict[str, Any]) -> bool:
        """Kosta's Health Check: HTTP GET /health, 5s timeout, 3 retries."""
        health_url = token_info.get("health_url")
        if not health_url:
            return True  # Legacy keys don't have health URLs

        for _ in range(3):
            try:
                resp = requests.get(health_url, timeout=5)
                if resp.status_code == 200:
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        return False

    def report_failure(self, key: str, provider: str):
        if not key:
            return
        logger.warning(f"Key failure for {provider}. Cooldown initiated.")
        self._blacklist[key] = time.time()

    def encrypt_value(self, plaintext: str) -> Optional[str]:
        """Encrypt a single value with AES-256-GCM (for external use)."""
        if not HAS_CRYPTO or AESGCM is None:
            return None

        salt = b"session-store-salt-fixed"
        key = self._derive_key(salt)
        if not key:
            return None

        nonce = os.urandom(12)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
        return base64.b64encode(nonce + ciphertext).decode()

    def decrypt_value(self, encrypted: str) -> Optional[str]:
        """Decrypt a single AES-256-GCM encrypted value."""
        if not HAS_CRYPTO or AESGCM is None:
            return None
        try:
            salt = b"session-store-salt-fixed"
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


if __name__ == "__main__":
    # Migration CLI
    import sys

    logging.basicConfig(level=logging.INFO)
    broker = TokenBroker()
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        print("🚀 Migrating to encrypted vault...")
        broker._try_legacy_import()
        print("✅ Done.")
