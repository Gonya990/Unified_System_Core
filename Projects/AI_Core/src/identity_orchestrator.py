import logging
import json
import os
from typing import Optional, Dict, Any, List
from google.oauth2.credentials import Credentials

try:
    from google_auth import GoogleAuthManager
    from calendar_client import CalendarClient
    from gmail_client import GmailClient
except ImportError:
    # Fallback for when running setup without full env
    GoogleAuthManager = None
    CalendarClient = None
    GmailClient = None

logger = logging.getLogger("IdentityOrchestrator")


class IdentityOrchestrator:
    """
    The Passport: Manages User Identity, Access Control (RBAC), and External Account Sessions.
    """

    def __init__(self, db, config_manager, auth_manager: Any = None):
        self.db = db
        self.config = config_manager
        self.auth_manager = auth_manager
        self._aes_key = self._derive_key()

        # Load Admin Config
        self.allowed_users = self._load_allowed_users()

    def _derive_key(self) -> Optional[bytes]:
        """Unified AES-256-GCM key derivation from AGENT_MAIL_TOKEN."""
        master_token = os.getenv("AGENT_MAIL_TOKEN")
        if not master_token:
            return None

        try:
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes

            salt = b"unified-system-vibranium-salt"
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            return kdf.derive(master_token.encode())
        except ImportError:
            return None

    def decrypt_value(self, encrypted: str) -> Optional[str]:
        """Unified AES-256-GCM decryption."""
        if not self._aes_key:
            return None
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            import base64

            data = base64.b64decode(encrypted)
            nonce, ciphertext = data[:12], data[12:]
            aesgcm = AESGCM(self._aes_key)
            return aesgcm.decrypt(nonce, ciphertext, None).decode()
        except Exception:
            return None

    def encrypt_value(self, plaintext: str) -> Optional[str]:
        """Unified AES-256-GCM encryption."""
        if not self._aes_key:
            return None
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            import base64
            import os

            nonce = os.urandom(12)
            aesgcm = AESGCM(self._aes_key)
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
            return base64.b64encode(nonce + ciphertext).decode()
        except Exception:
            return None

    def _load_allowed_users(self) -> List[int]:
        """Loads allowed users from Env and YAML via ConfigManager logic."""
        # Simplified replication of previous logic, ideally ConfigManager handles this
        users_str = self.config.get("ALLOWED_USERS", "708531393,5569219290,578363419")
        try:
            return [int(uid.strip()) for uid in users_str.split(",") if uid.strip()]
        except Exception:
            return [708531393]  # Safety fallback

    def check_access(self, user_id: int) -> bool:
        """
        Check if user is approved.
        Auto-approves if in ALLOWED_USERS whitelist.
        """
        if not self.db.is_approved(user_id):
            if user_id in self.allowed_users:
                self.db.approve_user(user_id, True)
                logger.info(
                    f"IdentityOrchestrator: Auto-approved whitelisted user {user_id}"
                )
                return True
            return False
        return True

    def get_google_services(self, user_id: int) -> Dict[str, Any]:
        """
        Returns initialized clients for Google Services (Calendar, Gmail) if authorized.
        """
        services: Dict[str, Any] = {"calendar": None, "gmail": None}

        user_data = self.db.get_user(user_id)
        if (
            not user_data
            or not user_data.get("is_google_connected")
            or not user_data.get("google_creds")
        ):
            return services

        try:
            creds_raw = user_data["google_creds"]
            creds_dict = None

            # 1. Try plaintext JSON first (legacy)
            try:
                creds_dict = json.loads(creds_raw)
            except json.JSONDecodeError:
                # 2. Try unified AES-GCM decryption
                decrypted = self.decrypt_value(creds_raw)
                if decrypted:
                    try:
                        creds_dict = json.loads(decrypted)
                    except json.JSONDecodeError:
                        logger.error(
                            f"IdentityOrchestrator: Decrypted data for {user_id} is not valid JSON."
                        )
                else:
                    logger.error(
                        f"IdentityOrchestrator: Failed to decrypt credentials for {user_id}."
                    )

            if not creds_dict:
                return services

            if CalendarClient:
                services["calendar"] = CalendarClient(credentials_dict=creds_dict)

            if GmailClient:
                services["gmail"] = GmailClient(credentials_dict=creds_dict)

        except Exception as e:
            logger.error(
                f"IdentityOrchestrator: Failed to init services for {user_id}: {e}"
            )

        return services

    def save_google_creds(self, user_id: int, credentials_json: str):
        """Encrypts and saves Google credentials to the database."""
        encrypted = self.encrypt_value(credentials_json)
        if encrypted:
            self.db.set_google_creds(user_id, encrypted)
            self.db.set_google_connected(user_id, True)
            logger.info(
                f"IdentityOrchestrator: Encrypted credentials saved for user {user_id}"
            )
        else:
            # Fallback to plaintext if encryption fails (unsafe but preserves functionality)
            # In a real production system, we might want to raise an error instead
            logger.warning(
                f"IdentityOrchestrator: Encryption failed for user {user_id}. Saving plaintext."
            )
            self.db.set_google_creds(user_id, credentials_json)
            self.db.set_google_connected(user_id, True)

    def get_auth_url(self, user_id: int) -> Optional[str]:
        """Proxy to AuthManager."""
        if self.auth_manager:
            return self.auth_manager.get_auth_url(user_id)
        return None
