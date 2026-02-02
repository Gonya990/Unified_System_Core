"""
Home Assistant Integration Tool for AI Agent

Provides smart home device control via Home Assistant API.
"""

import logging
import os
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)


class HomeAssistantTool:
    """Home Assistant device control tool"""

    def __init__(self):
        self.base_url = os.getenv("HA_URL", "http://homeassistant.local:8123")
        self.token = os.getenv("HA_TOKEN")

        if not self.token:
            logger.warning("HA_TOKEN not set - Home Assistant tool will not work")

    def get_definition(self) -> dict[str, Any]:
        """Get OpenAI function definition"""
        return {
            "name": "control_device",
            "description": "Control Home Assistant smart home device (lights, switches, climate, etc). Can turn on/off, toggle, or get current state.",
            "parameters": {
                "type": "object",
                "properties": {
                    "entity_id": {
                        "type": "string",
                        "description": "Entity ID (e.g. 'light.living_room', 'switch.bedroom_fan')"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["turn_on", "turn_off", "toggle", "get_state"],
                        "description": "Action to perform on the device"
                    },
                    "brightness": {
                        "type": "integer",
                        "description": "Brightness level 0-255 (optional, only for lights)",
                        "minimum": 0,
                        "maximum": 255
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Temperature in Celsius (optional, only for climate devices)"
                    }
                },
                "required": ["entity_id", "action"]
            }
        }

    async def handler(
        self,
        entity_id: str,
        action: str,
        brightness: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Execute Home Assistant action.

        Args:
            entity_id: Device entity ID
            action: Action to perform
            brightness: Optional brightness for lights
            temperature: Optional temperature for climate

        Returns:
            Result message
        """
        if not self.token:
            return "❌ Error: Home Assistant not configured (missing HA_TOKEN)"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }

                # Get current state
                if action == "get_state":
                    response = await client.get(
                        f"{self.base_url}/api/states/{entity_id}",
                        headers=headers
                    )

                    if response.status_code == 200:
                        state = response.json()
                        attributes = state.get('attributes', {})

                        result = f"📊 **Device:** {entity_id}\n"
                        result += f"**State:** {state['state']}\n"

                        if 'friendly_name' in attributes:
                            result += f"**Name:** {attributes['friendly_name']}\n"

                        if 'brightness' in attributes:
                            result += f"**Brightness:** {attributes['brightness']}/255\n"

                        if 'temperature' in attributes:
                            result += f"**Temperature:** {attributes['temperature']}°C\n"

                        return result

                    elif response.status_code == 404:
                        return f"❌ Error: Device not found: {entity_id}"
                    else:
                        return f"❌ Error: HTTP {response.status_code}"

                # Control actions
                else:
                    domain = entity_id.split('.')[0]
                    data = {"entity_id": entity_id}

                    if brightness is not None and domain == "light":
                        data["brightness"] = brightness

                    if temperature is not None and domain == "climate":
                        data["temperature"] = temperature

                    response = await client.post(
                        f"{self.base_url}/api/services/{domain}/{action}",
                        headers=headers,
                        json=data
                    )

                    if response.status_code == 200:
                        extras = []
                        if brightness is not None:
                            extras.append(f"brightness={brightness}")
                        if temperature is not None:
                            extras.append(f"temp={temperature}°C")

                        extra_str = f" ({', '.join(extras)})" if extras else ""
                        return f"✅ **{action}** executed on **{entity_id}**{extra_str}"

                    elif response.status_code == 404:
                        return f"❌ Error: Device or service not found: {entity_id}"
                    else:
                        return f"❌ Error: HTTP {response.status_code}"

        except httpx.TimeoutException:
            return f"❌ Error: Timeout connecting to Home Assistant at {self.base_url}"
        except httpx.ConnectError:
            return f"❌ Error: Cannot connect to Home Assistant at {self.base_url}"
        except Exception as e:
            logger.error(f"Home Assistant error: {e}", exc_info=True)
            return f"❌ Error: {str(e)}"
