
import sys
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Add Scripts/homeassistant to path to import ha_client
# Assuming structure: Unified_System/Windows_AI_Core/src/ha_controller.py
# Target: Unified_System/Scripts/homeassistant/ha_client.py
current_dir = Path(__file__).resolve().parent
scripts_dir = current_dir.parent.parent / "Scripts" / "homeassistant"

if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))

logger = logging.getLogger(__name__)

try:
    from ha_client import HomeAssistantClient, HAConfig
    HA_AVAILABLE = True
except ImportError as e:
    logger.error(f"Failed to import HomeAssistantClient: {e}")
    HA_AVAILABLE = False
    HomeAssistantClient = None

class HAController:
    """
    Controller for Home Assistant integration.
    Wraps the ha_client.py with bot-specific logic.
    """
    def __init__(self):
        if not HA_AVAILABLE:
            logger.warning("Home Assistant Client not available")
            self.client = None
            return
            
        # Initialize with default config (tokens are hardcoded in ha_client for now)
        # TODO: Move tokens to .env
        self.client = HomeAssistantClient()
    
    async def get_status(self) -> Dict[str, Any]:
        """Check HA connection status."""
        if not self.client:
            return {"status": "error", "message": "Client not loaded"}
        
        # ha_client is synchronous - run in executor?
        # For now, simplistic sync call (should convert ha_client to async later)
        try:
            return self.client.check_health()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def turn_on_light(self, entity_id: str):
        if not self.client: return None
        return self.client.turn_on_light(entity_id)
        
    async def turn_off_light(self, entity_id: str):
        if not self.client: return None
        return self.client.turn_off_light(entity_id)
        
    async def set_temperature(self, entity_id: str, temp: float):
        if not self.client: return None
        return self.client.set_temperature(entity_id, temp)
    
    async def get_states(self):
        if not self.client: return []
        return self.client.get_states()
