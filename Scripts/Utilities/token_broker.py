import json
import os
import time
import logging
from typing import Optional, Dict, List
from itertools import cycle

# Setup Logger
logger = logging.getLogger("TokenBroker")

class TokenBroker:
    """
    Manages API keys for the Unified System.
    Loads keys from 'secrets/keys.json' (local vault) or Environment Variables.
    Implements Round-Robin rotation and basic health tracking.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TokenBroker, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, secrets_path: str = None):
        if hasattr(self, 'initialized') and self.initialized:
            return
            
        if not secrets_path:
             # Default: Unified_System/secrets/keys.json
             base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
             secrets_path = os.path.join(base_dir, "secrets", "keys.json")
             
        self.secrets_path = secrets_path
        self.key_store = self._load_keys()
        
        # Round-Robin iterators cache: { "provider_tier": iterator }
        self._iterators = {}
        
        # Blacklist for failed keys: { "key_value": timestamp_of_failure }
        self._blacklist = {}
        self._blacklist_ttl = 300 # Seconds to ignore a failed key (5 mins)
        
        self.initialized = True

    def _load_keys(self) -> Dict[str, List[Dict]]:
        """Loads keys from JSON and Envs."""
        data = {"gemini": [], "openai": [], "claude": [], "other": []}
        
        # 1. Try JSON Vault
        if os.path.exists(self.secrets_path):
            try:
                with open(self.secrets_path, 'r') as f:
                    loaded = json.load(f)
                    # Merge securely and dynamically
                    for provider, keys in loaded.items():
                        if provider not in data:
                            data[provider] = []
                        data[provider].extend(keys)
            except Exception as e:
                logger.error(f"Failed to load secrets/keys.json: {e}")
        
        # 2. Fallback to Env Vars (Legacy Support)
        if not data["gemini"] and os.getenv("GEMINI_API_KEY"):
            data["gemini"].append({
                "alias": "Env_Legacy",
                "key": os.getenv("GEMINI_API_KEY"),
                "tier": "free",
                "owner": "System"
            })
            
        if not data["openai"] and os.getenv("OPENAI_API_KEY"):
            data["openai"].append({
                "alias": "Env_Legacy",
                "key": os.getenv("OPENAI_API_KEY"),
                "tier": "tier1",
                "owner": "System"
            })
            
        return data

    def get_key(self, provider: str, tier: str = None) -> Optional[str]:
        """
        Get a valid API Key for the provider using Round-Robin.
        Skips keys currently in the blacklist (cooldown).
        """
        provider = provider.lower()
        pool = self.key_store.get(provider, [])
        
        # Filter by tier if requested
        if tier:
            pool = [k for k in pool if k.get('tier') == tier]
            
        if not pool:
            logger.warning(f"No keys found for provider: {provider} (Tier: {tier})")
            return None
        
        # Filter out blacklisted keys
        valid_pool = []
        now = time.time()
        for k in pool:
            key_val = k['key']
            if key_val in self._blacklist:
                if now - self._blacklist[key_val] < self._blacklist_ttl:
                    continue # Still in cooldown
                else:
                    del self._blacklist[key_val] # Cooldown expired
            valid_pool.append(k)
            
        if not valid_pool:
            logger.error(f"All keys for {provider} are currently blacklisted/failed!")
            return None

        # Get iterator identifier
        iter_id = f"{provider}_{tier if tier else 'any'}"
        
        # Create or update iterator if pool size changed (naive check)
        if iter_id not in self._iterators:
            self._iterators[iter_id] = cycle(valid_pool)
            
        # Get next key
        # Reset cycle if valid_pool changed drastically or we hit next
        # For simplicity in Phase 1, we just create a fresh cycle from the valid pool every time
        # wait, proper round robin requires persistence.
        # Let's simple implementation: use a persistent cycle, but if next yields a blacklisted key (race condition), skip it.
        # Actually simplest for Phase 1: 
        # Just use the index logic:
        
        if not hasattr(self, '_indices'):
            self._indices = {}
            
        current_idx = self._indices.get(iter_id, 0)
        
        # Try to find a valid key starting from current_idx
        for _ in range(len(valid_pool)):
            idx = current_idx % len(valid_pool)
            candidate = valid_pool[idx]
            
            # Use this one
            self._indices[iter_id] = idx + 1
            
            # Log usage
            alias = candidate.get('alias', 'Unknown')
            logger.info(f"TokenBroker: Provided key '{alias}' for {provider} (Owner: {candidate.get('owner')})")
            
            return candidate['key']
            
        return None

    def report_failure(self, key: str, provider: str):
        """
        Report a key failure (429/401).
        Adds key to temporary blacklist.
        """
        logger.warning(f"TokenBroker: Key failure reported for {provider}. Blacklisting for {self._blacklist_ttl}s.")
        self._blacklist[key] = time.time()

    def list_available_pools(self):
        """Debug helper to see what's loaded."""
        summary = {}
        for prov, keys in self.key_store.items():
            active = len([k for k in keys if k['key'] not in self._blacklist])
            summary[prov] = {"total": len(keys), "active": active}
        return summary
