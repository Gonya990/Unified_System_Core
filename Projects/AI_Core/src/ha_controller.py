
import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Ensure current directory is in path for sibling imports
# Correctly adjust path for imports
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Add parent directory as well
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Try importing with multiple strategies
HA_AVAILABLE = False
HomeAssistantClient = None

try:
    # 1. Direct import (same directory)
    from ha_client import HAConfig, HomeAssistantClient
    HA_AVAILABLE = True
except ImportError:
    try:
        # 2. Package import (from src)
        from src.ha_client import HAConfig, HomeAssistantClient
        HA_AVAILABLE = True
    except ImportError as e:
        logger.error(f"Failed to import ha_client: {e}")
        # Debug: list files in current dir
        try:
             files = [f.name for f in current_dir.iterdir()]
             logger.error(f"Files in {current_dir}: {files}")
        except:
             pass

class HAController:
    """
    Controller for Home Assistant integration.
    Wraps the ha_client.py with bot-specific logic.
    """
    HA_AVAILABLE = HA_AVAILABLE  # Class-level attribute

    def __init__(self):
        self.HA_AVAILABLE = HA_AVAILABLE  # Instance attribute
        if not HA_AVAILABLE:
            logger.warning("Home Assistant Client not available")
            self.client = None
            return

        # Initialize with default config (tokens are hardcoded in ha_client for now)
        # TODO: Move tokens to .env
        self.client = HomeAssistantClient()

    async def get_status(self) -> dict[str, Any]:
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

        # Try exact match first
        # If entity_id not found in states, try fuzzy match
        states = self.client.get_states()
        entity_ids = [s['entity_id'] for s in states]

        target = entity_id
        if target not in entity_ids:
            # Fuzzy match
            import difflib
            # Filter for lights/switches
            candidates = [e for e in entity_ids if e.startswith('light.') or e.startswith('switch.')]
            # Try to match simple name (e.g. "corridor" against "light.corridor_switch_1")

            # 1. Search by Friendly Name (Russian/Exact)
            # Create map of name -> entity_id
            name_map = {}
            for s in states:
                eid = s['entity_id']
                if eid.startswith('light.') or eid.startswith('switch.'):
                    fname = s.get('attributes', {}).get('friendly_name', '').lower()
                    if fname:
                        name_map[fname] = eid

            # Check for partial match in friendly names
            target_lower = target.lower()
            for fname, eid in name_map.items():
                if target_lower in fname:
                    target = eid
                    logger.info(f"Friendly name match found: {entity_id} -> {fname} ({target})")
                    break
            else:
                # 2. Check if 'target' is part of entity_id
                simple_matches = [e for e in candidates if target_lower in e.lower()]
                if simple_matches:
                    target = simple_matches[0]
                    logger.info(f"Exact partial entity_id match found: {entity_id} -> {target}")
                else:
                    # 3. Difflib match on entity_ids
                    matches = difflib.get_close_matches(target, candidates, n=1, cutoff=0.5)
                    if matches:
                        target = matches[0]
                        logger.info(f"Fuzzy entity_id match found: {entity_id} -> {target}")
                    else:
                        logger.warning(f"No match found for {entity_id}")

        return self.client.turn_on_light(target)

    async def turn_off_light(self, entity_id: str):
        if not self.client: return None

        # Try exact match first
        states = self.client.get_states()
        entity_ids = [s['entity_id'] for s in states]

        target = entity_id
        if target not in entity_ids:
            # Fuzzy match
            import difflib
            candidates = [e for e in entity_ids if e.startswith('light.') or e.startswith('switch.')]

            # 1. Search by Friendly Name (Russian/Exact)
            # Create map of name -> entity_id
            name_map = {}
            for s in states:
                eid = s['entity_id']
                if eid.startswith('light.') or eid.startswith('switch.'):
                    fname = s.get('attributes', {}).get('friendly_name', '').lower()
                    if fname:
                        name_map[fname] = eid

            # Check for partial match in friendly names
            target_lower = target.lower()
            for fname, eid in name_map.items():
                if target_lower in fname:
                    target = eid
                    logger.info(f"Friendly name match found: {entity_id} -> {fname} ({target})")
                    break
            else:
                # 2. Check if 'target' is part of entity_id
                simple_matches = [e for e in candidates if target_lower in e.lower()]
                if simple_matches:
                    target = simple_matches[0]
                    logger.info(f"Exact partial entity_id match found: {entity_id} -> {target}")
                else:
                    # 3. Difflib match on entity_ids
                    matches = difflib.get_close_matches(target, candidates, n=1, cutoff=0.5)
                    if matches:
                        target = matches[0]
                        logger.info(f"Fuzzy entity_id match found: {entity_id} -> {target}")
                    else:
                        logger.warning(f"No match found for {entity_id}")

        return self.client.turn_off_light(target)

    async def set_temperature(self, entity_id: str, temp: float):
        if not self.client: return None
        return self.client.set_temperature(entity_id, temp)

    async def get_states(self):
        if not self.client: return []
        return self.client.get_states()

    async def run_script(self, entity_id: str):
        """Run a HA script."""
        if not self.client: return None
        # Scripts are services in 'script' domain
        # E.g. script.goodnight -> domain=script, service=goodnight OR domain=script, service=turn_on?
        # Usually service: script.something is deprecated, better use service: script.turn_on entity_id=script.something
        # But actually for scripts: domain='script', service=name_after_dot

        name = entity_id.replace("script.", "")
        return self.client.call_service("script", name)

    async def activate_scene(self, entity_id: str):
        """Activate a scene."""
        if not self.client: return None
        return self.client.call_service("scene", "turn_on", entity_id=entity_id)

    async def get_sensors_report(self) -> str:
        """Get summary of sensors."""
        if not self.client: return "HA unavailable"

        states = self.client.get_states()
        sensors = []

        for s in states:
            eid = s.get('entity_id', '')
            state = s.get('state', '')
            unit = s.get('attributes', {}).get('unit_of_measurement', '')
            name = s.get('attributes', {}).get('friendly_name', eid)

            if eid.startswith("sensor.") and state not in ["unknown", "unavailable"]:
                # Filter useful sensors but be more inclusive
                # Standard physical measurements
                important_units = ["°C", "%", "W", "lx", "V", "A", "kWh", "ppm", "m/s", "mm", "hPa", "dB"]
                if unit in important_units or "battery" in eid:
                    sensors.append(f"🔹 **{name}**: {state} {unit}")

        if not sensors:
            return "Сенсоров не найдено."

        # Sort by name
        sensors.sort()

        return "📊 **Показания датчиков**:\n" + "\n".join(sensors)

    async def get_integrations(self):
        """Get list of integrations."""
        if not self.client: return []
        return self.client.get_integrations()

    async def reload_integration(self, entry_id: str):
        """Reload an integration."""
        if not self.client: return None
        return self.client.reload_integration(entry_id)

    async def speak_via_yandex(self, message: str, entity_id: str = "media_player.yandex_station_c00tc40000wq8k"):
        """Send TTS message via Yandex Station."""
        if not self.client:
            return False
        try:
            self.client.call_service("tts", "yandex_station_say", entity_id=entity_id, message=message)
            return True
        except Exception as e:
            logger.error(f"Yandex TTS failed: {e}")
            # Try alternative method via media_player
            try:
                self.client.call_service("media_player", "play_media",
                    entity_id=entity_id,
                    media_content_type="text",
                    media_content_id=message
                )
                return True
            except Exception as e2:
                logger.error(f"Yandex TTS fallback failed: {e2}")
                return False

    async def get_full_context(self) -> str:
        """Get condensed context of all relevant HA entities for LLM grounding."""
        if not self.client:
            return "Home Assistant is not integrated or offline."

        try:
            states = self.client.get_states()
            context = []

            for s in states:
                eid = s.get('entity_id', '')
                state = s.get('state', '')
                fname = s.get('attributes', {}).get('friendly_name', '')

                # Filter for relevant domains
                domain = eid.split('.')[0]
                if domain in ['light', 'switch', 'sensor', 'binary_sensor', 'climate', 'media_player', 'script', 'scene']:
                    if state not in ['unknown', 'unavailable']:
                        item = f"{eid} ({fname}): {state}"
                        if domain == 'sensor':
                            unit = s.get('attributes', {}).get('unit_of_measurement', '')
                            if unit: item += f" {unit}"
                        context.append(item)

            if not context:
                return "No active entities found in Home Assistant."

            return "\n".join(context)
        except Exception as e:
            logger.error(f"Failed to get full context: {e}")
            return f"Error retrieving home state: {e}"

