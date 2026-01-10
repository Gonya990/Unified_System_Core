import os
import json
import time
import logging
import base64
from typing import Dict, List, Optional, Any
from itertools import cycle
from pathlib import Path
import yaml
import requests

# Optional cryptography for vault encryption
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes

    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

logger = logging.getLogger("TokenBroker")


class TokenBroker:
    """centralizes API key management, rotation, and health monitoring."""

    def __init__(self, vault_path: str = "~/.config/unified-system/tokens.yaml"):
        self.vault_path = os.path.expanduser(vault_path)
        self.key_store: Dict[str, List[Dict]] = {}
        self._blacklist: Dict[str, float] = {}  # key -> timestamp
        self._blacklist_ttl = 3600  # 1 hour cooldown
        self._indices: Dict[str, int] = {}
        self._aes_key = self._derive_key()

        self.load_vault()

    def _derive_key(self) -> Optional[bytes]:
        """Derives a 256-bit key from AGENT_MAIL_TOKEN env var."""
        master_token = os.getenv("AGENT_MAIL_TOKEN")
        if not master_token or not HAS_CRYPTO:
            return None

        salt = b"unified-system-vibranium-salt"  # Static salt for simplicity
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(master_token.encode())

    def load_vault(self):
        """Loads and decrypts the token vault."""
        if not os.path.exists(self.vault_path):
            logger.info("Token vault not found. Using legacy fallback.")
            self._try_legacy_import()
            return

        try:
            with open(self.vault_path, "r") as f:
                raw_data = yaml.safe_load(f) or {}

            # Decrypt keys if possible
            if self._aes_key and HAS_CRYPTO:
                for provider, pool in raw_data.items():
                    for entry in pool:
                        if "encrypted_key" in entry:
                            decrypted = self.decrypt_value(entry["encrypted_key"])
                            if decrypted:
                                entry["key"] = decrypted

            self.key_store = raw_data
            logger.info(
                f"Loaded {sum(len(v) for v in self.key_store.values())} tokens from vault."
            )
        except Exception as e:
            logger.error(f"Failed to load vault: {e}")

    def save_vault(self):
        """Encrypts and saves current keys to vault."""
        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)

        vault_to_save = {}
        for provider, pool in self.key_store.items():
            encrypted_pool = []
            for entry in pool:
                # Copy entry without the plain 'key' if we have encryption
                save_entry = {k: v for k, v in entry.items() if k != "key"}
                if "key" in entry and self._aes_key and HAS_CRYPTO:
                    encrypted = self.encrypt_value(entry["key"])
                    if encrypted:
                        save_entry["encrypted_key"] = encrypted
                else:
                    save_entry["key"] = entry.get("key")
                encrypted_pool.append(save_entry)
            vault_to_save[provider] = encrypted_pool

        with open(self.vault_path, "w") as f:
            yaml.dump(vault_to_save, f)
        logger.info(f"Vault saved to {self.vault_path}")

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

                # Convert keys.json structure to our pool structure if needed
                # If it's already structured by provider, we use it
                self.key_store = data
                logger.info(
                    f"Imported legacy keys from {legacy_path}. Encrypting now..."
                )
                self.save_vault()
            except Exception as e:
                logger.error(f"Legacy import failed: {e}")

    def get_key(self, provider: str, tier: str = None) -> Optional[str]:
        """
        Get a valid API Key for the provider using Round-Robin and Health Checks.
        """
        provider = provider.lower()
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
            if k["key"] not in self._blacklist
            or (now - self._blacklist[k["key"]] > self._blacklist_ttl)
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
                # Log usage
                alias = token_info.get("alias", "Unknown")
                logger.info(f"TokenBroker: Provided key '{alias}' for {provider}")
                return token_info["key"]
            else:
                self.report_failure(token_info["key"], provider)

        return None

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
            except:
                pass
            time.sleep(0.5)
        return False

    def report_failure(self, key: str, provider: str):
        logger.warning(f"Key failure for {provider}. Cooldown initiated.")
        self._blacklist[key] = time.time()

    def encrypt_value(self, plaintext: str) -> Optional[str]:
        """Encrypt a value with AES-256-GCM."""
        if not self._aes_key or not HAS_CRYPTO:
            return None
        nonce = os.urandom(12)
        aesgcm = AESGCM(self._aes_key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
        return base64.b64encode(nonce + ciphertext).decode()

    def decrypt_value(self, encrypted: str) -> Optional[str]:
        """Decrypt an AES-256-GCM encrypted value."""
        if not self._aes_key or not HAS_CRYPTO:
            return None
        try:
            data = base64.b64decode(encrypted)
            nonce, ciphertext = data[:12], data[12:]
            aesgcm = AESGCM(self._aes_key)
            return aesgcm.decrypt(nonce, ciphertext, None).decode()
        except:
            return None

    def list_available_pools(self) -> Dict[str, Dict[str, int]]:
        """List all provider pools with active/total counts."""
        now = time.time()
        result = {}
        for provider, pool in self.key_store.items():
            active = sum(
                1
                for k in pool
                if k.get("key") not in self._blacklist
                or (now - self._blacklist.get(k.get("key"), 0) > self._blacklist_ttl)
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
            "encryption_enabled": self._aes_key is not None,
            "last_rotation": getattr(self, "_last_rotation", None),
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
        """Reload keys from vault file (for hot-reload without restart)."""
        try:
            self.load_vault()
            self._last_rotation = time.time()
            logger.info("TokenBroker: Keys reloaded from disk")
            return True
        except Exception as e:
            logger.error(f"TokenBroker: Failed to reload keys: {e}")
            return False


if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO)
    broker = TokenBroker()
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        print("Migrating to encrypted vault...")
        broker._try_legacy_import()
        print("Done.")
