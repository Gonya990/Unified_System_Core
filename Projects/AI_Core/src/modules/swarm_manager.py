import logging
import random
import yaml
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

class SwarmManager:
    """Manages a pool of API keys (the Swarm) for multiple AI services."""
    
    def __init__(self, resources_path: str = "config/resources.yaml"):
        self.resources_path = Path(resources_path)
        self.gemini_pool: List[dict] = []
        self.openai_pool: List[dict] = []
        self._current_gemini_idx = 0
        self.load_resources()

    def load_resources(self):
        """Load API keys from resources.yaml."""
        if not self.resources_path.exists():
            logger.warning(f"Resources file not found at {self.resources_path}")
            return

        try:
            with open(self.resources_path, "r") as f:
                data = yaml.safe_load(f)
                if not data:
                    return
                
                self.gemini_pool = data.get("gemini_pool", [])
                self.openai_pool = data.get("openai_pool", [])
                
                # Filter out inactive or empty keys
                self.gemini_pool = [k for k in self.gemini_pool if k.get("status") == "active" and k.get("api_key")]
                
                logger.info(f"Swarm loaded: {len(self.gemini_pool)} Gemini keys, {len(self.openai_pool)} OpenAI keys.")
        except Exception as e:
            logger.error(f"Failed to load swarm resources: {e}")

    def get_gemini_key(self) -> Optional[str]:
        """Get the next available Gemini API key using round-robin."""
        if not self.gemini_pool:
            return None
        
        # Round-robin rotation
        key_data = self.gemini_pool[self._current_gemini_idx]
        self._current_gemini_idx = (self._current_gemini_idx + 1) % len(self.gemini_pool)
        
        logger.debug(f"Using Gemini key from swarm member: {key_data.get('owner', 'Unknown')}")
        return key_data.get("api_key")

    def mark_key_failed(self, service: str, api_key: str):
        """Temporarily mark a key as failed (e.g. on 429)."""
        # For now, just log it. In the future, we could add a cooldown timer.
        logger.warning(f"Key for {service} reported failure. Rotating...")

    def get_stats(self) -> dict:
        """Return swarm health stats."""
        return {
            "gemini_keys_active": len(self.gemini_pool),
            "openai_keys_active": len(self.openai_pool)
        }
