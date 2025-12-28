"""
Device Monitor Service
Monitors critical Home Assistant entities and alerts on failure.
"""
import logging
import asyncio
from typing import List, Dict, Set
from .ha_controller import HAController

logger = logging.getLogger(__name__)

class DeviceMonitor:
    """Monitors HA entities for availability."""
    
    def __init__(self, ha_controller: HAController, notify_callback=None):
        self.ha = ha_controller
        self.notify_callback = notify_callback
        
        # Configuration
        self.monitored_entities: Set[str] = set()
        self.ignored_entities: Set[str] = set()
        
        # State tracking
        self.unavailable_entities: Set[str] = set()
        self.is_monitoring = False
        
    def add_entity(self, entity_id: str):
        """Add entity to monitor."""
        self.monitored_entities.add(entity_id)
        
    def ignore_entity(self, entity_id: str):
        """Ignore entity from monitoring."""
        self.ignored_entities.add(entity_id)
        if entity_id in self.monitored_entities:
            self.monitored_entities.remove(entity_id)
            
    async def check_devices(self) -> List[str]:
        """Check all monitored devices and return list of new failures."""
        if not self.ha:
            logger.warning("HA Controller not available for monitoring")
            return []
            
        try:
            states = await self.ha.get_states()
            if not states:
                logger.warning("Failed to fetch states from HA")
                return []
                
            current_failures = set()
            new_failures = []
            
            for state_obj in states:
                entity_id = state_obj.get('entity_id')
                state = state_obj.get('state')
                
                # Check if we should monitor this entity
                # Rule 1: Explicitly monitored
                # Rule 2: Critical domain (switch, climate, lock) if auto-discovery is on (future)
                
                should_monitor = entity_id in self.monitored_entities
                
                if should_monitor:
                    if state in ["unavailable", "unknown"]:
                        current_failures.add(entity_id)
                        if entity_id not in self.unavailable_entities:
                            logger.warning(f"Entity {entity_id} became unavailable!")
                            new_failures.append(entity_id)
            
            # Update state
            # Check for recoveries
            recovered = self.unavailable_entities - current_failures
            for entity_id in recovered:
                logger.info(f"Entity {entity_id} recovered.")
                if self.notify_callback:
                    await self.notify_callback(f"✅ Устройство доступно: `{entity_id}`")
            
            self.unavailable_entities = current_failures
            
            return new_failures
            
        except Exception as e:
            logger.error(f"Device check failed: {e}")
            return []
            
    async def run_check(self):
        """Periodic check method."""
        failures = await self.check_devices()
        if failures and self.notify_callback:
            # Send alert
            msg = "⚠️ **Внимание! Проблемы с устройствами:**\n\n"
            for entity in failures:
                # Try to get friendly name? (Optimization: cache names)
                msg += f"❌ `{entity}` недоступен\n"
            
            await self.notify_callback(msg)
