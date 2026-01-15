import json
import logging
from typing import Any, Optional

try:
    # Import TokenBroker from Utilities
    import sys
    from pathlib import Path

    from calendar_client import CalendarClient
    from gmail_client import GmailClient
    from google_auth import GoogleAuthManager

    ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
    UTILS_DIR = ROOT_DIR / "Scripts" / "Utilities"
    if str(UTILS_DIR) not in sys.path:
        sys.path.insert(0, str(UTILS_DIR))
    from token_broker import TokenBroker
except ImportError:
    # Fallback for when running setup without full env
    GoogleAuthManager = None
    CalendarClient = None
    GmailClient = None
    TokenBroker = None

logger = logging.getLogger("IdentityOrchestrator")


class IdentityOrchestrator:
    """
    The Passport: Manages User Identity, Access Control (RBAC), and External Account Sessions.

    Extended with granular RBAC system for project-level and resource-level permissions.
    """

    def __init__(self, db, config_manager, auth_manager: Any = None):
        self.db = db
        self.config = config_manager
        self.auth_manager = auth_manager

        # Unified TokenBroker for encryption/decryption
        if TokenBroker:
            self.token_broker = TokenBroker()
        else:
            self.token_broker = None
            if hasattr(logging.getLogger("IdentityOrchestrator"), "warning"):
                logging.getLogger("IdentityOrchestrator").warning("TokenBroker not available")

        # Load Admin Config
        self.allowed_users = self._load_allowed_users()

        # Initialize RBAC system
        try:
            from rbac import RBACManager

            self.rbac = RBACManager(db)
            logger.info("RBAC system initialized")
        except ImportError as e:
            logger.warning(f"RBAC system not available: {e}")
            self.rbac = None

    def decrypt_value(self, encrypted: str) -> Optional[str]:
        """Unified AES-256-GCM decryption via TokenBroker."""
        if not self.token_broker:
            return None
        return self.token_broker.decrypt_value(encrypted)

    def encrypt_value(self, plaintext: str) -> Optional[str]:
        """Unified AES-256-GCM encryption via TokenBroker."""
        if not self.token_broker:
            return None
        return self.token_broker.encrypt_value(plaintext)

    def _load_allowed_users(self) -> list[int]:
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
                logger.info(f"IdentityOrchestrator: Auto-approved whitelisted user {user_id}")
                return True
            return False
        return True

    def get_google_services(self, user_id: int) -> dict[str, Any]:
        """
        Returns initialized clients for Google Services (Calendar, Gmail) if authorized.
        """
        services: dict[str, Any] = {"calendar": None, "gmail": None}

        user_data = self.db.get_user(user_id)
        if not user_data or not user_data.get("is_google_connected") or not user_data.get("google_creds"):
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
                        logger.error(f"IdentityOrchestrator: Decrypted data for {user_id} is not valid JSON.")
                else:
                    logger.error(f"IdentityOrchestrator: Failed to decrypt credentials for {user_id}.")

            if not creds_dict:
                return services

            if CalendarClient:
                services["calendar"] = CalendarClient(credentials_dict=creds_dict)

            if GmailClient:
                services["gmail"] = GmailClient(credentials_dict=creds_dict)

        except Exception as e:
            logger.error(f"IdentityOrchestrator: Failed to init services for {user_id}: {e}")

        return services

    def save_google_creds(self, user_id: int, credentials_json: str):
        """Encrypts and saves Google credentials to the database."""
        encrypted = self.encrypt_value(credentials_json)
        if encrypted:
            self.db.set_google_creds(user_id, encrypted)
            self.db.set_google_connected(user_id, True)
            logger.info(f"IdentityOrchestrator: Encrypted credentials saved for user {user_id}")
        else:
            # Fallback to plaintext if encryption fails (unsafe but preserves functionality)
            # In a real production system, we might want to raise an error instead
            logger.warning(f"IdentityOrchestrator: Encryption failed for user {user_id}. Saving plaintext.")
            self.db.set_google_creds(user_id, credentials_json)
            self.db.set_google_connected(user_id, True)

    def get_auth_url(self, user_id: int) -> Optional[str]:
        """Proxy to AuthManager."""
        if self.auth_manager:
            return self.auth_manager.get_auth_url(user_id)
        return None
