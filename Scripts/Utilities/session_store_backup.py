import json
import logging
import os
import time
from typing import Any, Optional

import yaml
from token_broker import TokenBroker

logger = logging.getLogger("SessionStore")

class SessionStore:
    """
    Unified SessionStore (Phase 2 - Vibranium)
    Encrypted storage for OAuth tokens, Session IDs, and SSH keys.
    Delegates encryption to TokenBroker.
    """

    def __init__(self, store_path: str = None):
        if not store_path:
            self.store_path = os.path.expanduser("~/.config/unified-system/sessions.yaml")
        else:
            self.store_path = store_path

        self.broker = TokenBroker()
        self.sessions: dict[str, Any] = {}
        self.load_sessions()

    def load_sessions(self):
        """Loads and decrypts the sessions from YAML."""
        if not os.path.exists(self.store_path):
            return

        try:
            with open(self.store_path) as f:
                data = yaml.safe_load(f)

            if not data or 'encrypted_data' not in data:
                return

            decrypted = self.broker.decrypt_value(data['encrypted_data'])
            if decrypted:
                self.sessions = json.loads(decrypted)
                logger.info(f"Sessions loaded and decrypted: {self.store_path}")
        except Exception as e:
            logger.error(f"Failed to load sessions: {e}")

    def save_sessions(self):
        """Encrypts and saves the current sessions to YAML."""
        try:
            raw_data = json.dumps(self.sessions)
            encrypted = self.broker.encrypt_value(raw_data)

            if not encrypted:
                logger.error("Encryption failed. Cannot save sessions.")
                return

            data = {
                'encrypted_data': encrypted,
                'updated_at': time.strftime("%Y-%m-%d %H:%M:%S")
            }

            os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
            with open(self.store_path, 'w') as f:
                yaml.dump(data, f)
        except Exception as e:
            logger.error(f"Failed to save sessions: {e}")

    def set_session(self, key: str, value: Any):
        self.sessions[key] = value
        self.save_sessions()

    def get_session(self, key: str) -> Optional[Any]:
        return self.sessions.get(key)

    def delete_session(self, key: str):
        if key in self.sessions:
            del self.sessions[key]
            self.save_sessions()
