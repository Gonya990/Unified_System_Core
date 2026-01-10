
import json
import os
import random
import logging
from typing import Optional, Dict, List

# Setup Logger
logger = logging.getLogger("TokenBroker")

class TokenBroker:
    """
    Manages API keys for the Unified System.
    Loads keys from 'secrets/keys.json' (local vault) or Environment Variables.
    Implements Round-Robin rotation and tier filtering.
    """
    
    def __init__(self, secrets_path: str = None):
        if not secrets_path:
             # Default: Unified_System/secrets/keys.json
             base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
             secrets_path = os.path.join(base_dir, "secrets", "keys.json")
             
        self.secrets_path = secrets_path
        self.key_store = self._load_keys()
        self._usage_counters = {} # Transient validation for rotation logic

    def _load_keys(self) -> Dict[str, List[Dict]]:
        """Loads keys from JSON and Envs."""
        data = {"gemini": [], "openai": [], "claude": [], "other": []}
        
        # 1. Try JSON Vault
        if os.path.exists(self.secrets_path):
            try:
                with open(self.secrets_path, 'r') as f:
                    loaded = json.load(f)
                    # Merge securely
                    for provider, keys in loaded.items():
                        if provider in data:
                            data[provider].extend(keys)
            except Exception as e:
                logger.error(f"Failed to load secrets/keys.json: {e}")
        
        # 2. Fallback to Env Vars (Legacy Support)
        if not data["gemini"] and os.getenv("GEMINI_API_KEY"):
            data["gemini"].append({
                "alias": "Env_Legacy",
                "key": os.getenv("GEMINI_API_KEY"),
                "tier": "unknown",
                "owner": "System"
            })
            
        if not data["openai"] and os.getenv("OPENAI_API_KEY"):
            data["openai"].append({
                "alias": "Env_Legacy",
                "key": os.getenv("OPENAI_API_KEY"),
                "tier": "unknown",
                "owner": "System"
            })
            
        return data

    def get_key(self, provider: str, tier: str = None) -> Optional[str]:
        """
        Get a valid API Key for the provider.
        Auto-rotates between available keys.
        """
        provider = provider.lower()
        pool = self.key_store.get(provider, [])
        
        # Filter by tier if requested
        if tier:
            pool = [k for k in pool if k.get('tier') == tier]
            
        if not pool:
            logger.warning(f"No keys found for provider: {provider} (Tier: {tier})")
            return None
        
        # Simple Random Load Balancing (Effective enough for family use)
        # Can be upgraded to Round-Robin with state later
        selected = random.choice(pool)
        
        # Log usage (masked)
        alias = selected.get('alias', 'Unknown')
        logger.info(f"Using key '{alias}' for {provider}")
        
        return selected['key']

    def list_available_pools(self):
        """Debug helper to see what's loaded."""
        summary = {}
        for prov, keys in self.key_store.items():
            summary[prov] = len(keys)
        return summary
