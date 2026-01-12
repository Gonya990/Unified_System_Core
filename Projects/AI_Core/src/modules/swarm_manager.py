import logging
import random
import sys
from pathlib import Path
from typing import List, Optional

import yaml

logger = logging.getLogger(__name__)

try:
    sys.path.insert(
        0,
        str(
            Path(__file__).parent.parent.parent.parent.parent / "Scripts" / "Utilities"
        ),
    )
    from token_broker import TokenBroker

    HAS_TOKEN_BROKER = True
except ImportError:
    HAS_TOKEN_BROKER = False
    TokenBroker = None


class SwarmManager:
    """Manages a pool of API keys (the Swarm) for multiple AI services.

    Uses TokenBroker as backend when available for unified key management,
    encryption, and health monitoring.
    """

    def __init__(self, resources_path: str = "config/resources.yaml"):
        self.resources_path = Path(resources_path)
        self.gemini_pool: List[dict] = []
        self.openai_pool: List[dict] = []
        self._current_gemini_idx = 0
        self._token_broker: Optional[TokenBroker] = None

        if HAS_TOKEN_BROKER:
            try:
                self._token_broker = TokenBroker()
                logger.info("SwarmManager using TokenBroker backend")
            except Exception as e:
                logger.warning(f"TokenBroker init failed, using legacy mode: {e}")

        self.load_resources()

    def load_resources(self):
        """Load API keys from resources.yaml."""
        if not self.resources_path.exists():
            logger.warning(f"Resources file not found at {self.resources_path}")
            return

        try:
            with open(self.resources_path) as f:
                data = yaml.safe_load(f)
                if not data:
                    return

                self.gemini_pool = data.get("gemini_pool", [])
                self.openai_pool = data.get("openai_pool", [])

                # Filter out inactive or empty keys
                self.gemini_pool = [
                    k
                    for k in self.gemini_pool
                    if k.get("status") == "active" and k.get("api_key")
                ]

                logger.info(
                    f"Swarm loaded: {len(self.gemini_pool)} Gemini keys, {len(self.openai_pool)} OpenAI keys."
                )
        except Exception as e:
            logger.error(f"Failed to load swarm resources: {e}")

    def get_gemini_key(
        self, branch_id: str = "HOME_HQ", project_context: str = "PERSONAL"
    ) -> Optional[str]:
        """Get the next available Gemini API key with branch awareness."""
        if self._token_broker:
            key = self._token_broker.get_key("gemini")
            if key:
                logger.debug(f"Using Gemini key from TokenBroker (Branch: {branch_id})")
                return key

        pool = self.gemini_pool

        if project_context != "UNIFIED_CORE":
            pool = [
                k
                for k in self.gemini_pool
                if k.get("branch_id", "HOME_HQ") == branch_id
            ]

        if not pool:
            return None

        idx = self._current_gemini_idx % len(pool)
        key_data = pool[idx]
        self._current_gemini_idx += 1

        logger.debug(
            f"Using Gemini key from: {key_data.get('owner', 'Unknown')} (Branch: {key_data.get('branch_id', 'Unknown')})"
        )
        return key_data.get("api_key")

    def add_gemini_key(self, api_key: str, owner: str, branch_id: str = "HOME_HQ"):
        """Add a new Gemini key to the pool and persist it."""
        new_key = {
            "id": f"key_{random.randint(1000, 9999)}",
            "owner": owner,
            "api_key": api_key,
            "status": "active",
            "branch_id": branch_id,
        }

        # Load existing data to avoid overwriting other pools
        data = {"gemini_pool": [], "openai_pool": []}
        if self.resources_path.exists():
            with open(self.resources_path) as f:
                data = yaml.safe_load(f) or data

        data.setdefault("gemini_pool", []).append(new_key)

        with open(self.resources_path, "w") as f:
            yaml.safe_dump(data, f, allow_unicode=True)

        self.load_resources()
        return True

    def mark_key_failed(self, service: str, api_key: str):
        """Temporarily mark a key as failed (e.g. on 429)."""
        if self._token_broker:
            self._token_broker.blacklist_key(service, api_key)
        logger.warning(f"Key for {service} reported failure. Rotating...")

    def get_stats(self) -> dict:
        """Return swarm health stats."""
        stats = {
            "gemini_keys_active": len(self.gemini_pool),
            "openai_keys_active": len(self.openai_pool),
        }
        if self._token_broker:
            stats["token_broker"] = self._token_broker.health_check()
        return stats
