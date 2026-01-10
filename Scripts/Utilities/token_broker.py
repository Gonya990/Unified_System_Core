
import os
import yaml
import random
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load envs mainly for resolving ${VAR} in yaml
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env")

class TokenBroker:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenBroker, cls).__new__(cls)
            cls._instance.config_path = ROOT_DIR / "config/resources.yaml"
            cls._instance.pools = {}
            cls._instance.reload_config()
        return cls._instance
    
    def reload_config(self):
        """Load resources.yaml and resolve env vars."""
        if not self.config_path.exists():
            print(f"⚠️ Config not found: {self.config_path}")
            return
            
        with open(self.config_path, "r") as f:
            raw_data = f.read()
            
        # Basic ENV resolution
        # This allows defining api_key: "${OPENAI_API_KEY}" in YAML
        resolved_data = os.path.expandvars(raw_data)
        
        try:
            data = yaml.safe_load(resolved_data)
            self.pools = {}
            
            # Parse Pools
            if "openai_pool" in data:
                self.pools["openai"] = data["openai_pool"]
            if "gemini_pool" in data:
                self.pools["gemini"] = data["gemini_pool"]
                
            # Add other providers as needed
            
            # Print status
            total_keys = sum(len(p) for p in self.pools.values())
            print(f"✅ TokenBroker loaded. Pools: {list(self.pools.keys())}. Total Keys: {total_keys}")
            
        except yaml.YAMLError as e:
            print(f"❌ Error parsing resources.yaml: {e}")

    def get_key(self, provider: str, owner: str = None) -> Optional[str]:
        """
        Get an active API key for the provider.
        Args:
            provider: 'openai' | 'gemini'
            owner: Optional filter (e.g. 'Igor', 'Artur')
        Returns:
            API Key string or None
        """
        pool = self.pools.get(provider, [])
        if not pool:
            return None
            
        # Filter active keys
        candidates = [k for k in pool if k.get('status') == 'active']
        
        # Filter by owner if specified
        if owner:
            owner_candidates = [k for k in candidates if k.get('owner') == owner]
            if owner_candidates:
                candidates = owner_candidates
            else:
                print(f"⚠️ No active keys for owner '{owner}' in '{provider}'. Falling back to general pool.")
        
        if not candidates:
            return None
            
        # Strategy: Random for now (Load Balancing)
        # Future: Least Usage / Priority Weighted
        selected = random.choice(candidates)
        return selected['api_key']

    def report_failure(self, provider: str, key: str):
        """Mark a key as failing (simple circuit breaker)."""
        # Complex logic to disable key temporarily can go here
        masked = f"{key[:5]}...{key[-3:]}"
        print(f"⚠️ Key reported failure: {masked} ({provider})")

# Usage Example
if __name__ == "__main__":
    broker = TokenBroker()
    
    print("\n--- Testing Gemini Pool ---")
    key = broker.get_key("gemini")
    print(f"Got Gemini Key: {key[:10]}..." if key else "No Gemini Key found.")
    
    print("\n--- Testing OpenAI Pool ---")
    key = broker.get_key("openai")
    print(f"Got OpenAI Key: {key[:10]}..." if key else "No OpenAI Key found.")
