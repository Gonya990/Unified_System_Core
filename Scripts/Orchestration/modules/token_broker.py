
import os
import yaml
import time
import logging
import requests
from typing import List, Dict, Optional, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

logger = logging.getLogger(__name__)

class TokenBroker:
    """
    Resource Orchestrator Pillar: TokenBroker
    Handles secure storage, rotation, and health monitoring of API tokens.
    """
    def __init__(self, config_path: str, master_key: str):
        self.config_path = config_path
        self.master_key = master_key.encode()
        self.tokens: Dict[str, List[Dict[str, Any]]] = {}
        self.indices: Dict[str, int] = {}
        self._load_tokens()

    def _derive_key(self, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(self.master_key)

    def _load_tokens(self):
        """Loads and decrypts the token store."""
        if not os.path.exists(self.config_path):
            logger.warning(f"Token store not found at {self.config_path}")
            return

        try:
            with open(self.config_path, 'r') as f:
                data = yaml.safe_load(f)
            
            if not data or 'encrypted_data' not in data:
                return

            # Decryption logic
            encrypted_data = bytes.fromhex(data['encrypted_data'])
            nonce = bytes.fromhex(data['nonce'])
            salt = bytes.fromhex(data['salt'])
            
            key = self._derive_key(salt)
            aesgcm = AESGCM(key)
            decrypted = aesgcm.decrypt(nonce, encrypted_data, None)
            
            self.tokens = yaml.safe_load(decrypted)
            logger.info(f"Loaded {sum(len(v) for v in self.tokens.values())} tokens from store.")
        except Exception as e:
            logger.error(f"Failed to load tokens: {e}")

    def save_tokens(self, tokens: Dict[str, List[Dict[str, Any]]]):
        """Encrypts and saves the token store."""
        try:
            salt = os.urandom(16)
            nonce = os.urandom(12)
            key = self._derive_key(salt)
            aesgcm = AESGCM(key)
            
            raw_data = yaml.dump(tokens).encode()
            encrypted = aesgcm.encrypt(nonce, raw_data, None)
            
            data = {
                'encrypted_data': encrypted.hex(),
                'nonce': nonce.hex(),
                'salt': salt.hex()
            }
            
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(data, f)
            
            self.tokens = tokens
            logger.info("Tokens encrypted and saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save tokens: {e}")

    def get_token(self, provider: str) -> Optional[str]:
        """Returns a healthy token using round-robin rotation."""
        if provider not in self.tokens or not self.tokens[provider]:
            return None

        # Round-robin selection
        start_idx = self.indices.get(provider, 0)
        num_tokens = len(self.tokens[provider])
        
        for i in range(num_tokens):
            idx = (start_idx + i) % num_tokens
            token_info = self.tokens[provider][idx]
            
            if self._check_health(token_info):
                self.indices[provider] = (idx + 1) % num_tokens
                return token_info['key']
        
        logger.warning(f"No healthy tokens found for provider: {provider}")
        return None

    def _check_health(self, token_info: Dict[str, Any]) -> bool:
        """Checks the health of a token (stub for now, as per specs)."""
        health_url = token_info.get('health_url')
        if not health_url:
            return True # Assume healthy if no check URL
            
        retries = 3
        timeout = 5
        
        for attempt in range(retries):
            try:
                # Basic health check as specified
                resp = requests.get(health_url, timeout=timeout)
                if resp.status_code == 200:
                    return True
            except Exception:
                pass
            time.sleep(1)
            
        return False

if __name__ == "__main__":
    # Test stub
    logging.basicConfig(level=logging.INFO)
    broker = TokenBroker("/tmp/tokens.yaml", "vibranium-master-key")
    
    test_tokens = {
        "gemini": [{"key": "AIza...", "health_url": None}],
        "openai": [{"key": "sk-...", "health_url": "https://api.openai.com/v1/models"}]
    }
    broker.save_tokens(test_tokens)
    print(f"Retrieved token: {broker.get_token('gemini')}")
