"""
HomeKit Bridge Service - Full Implementation
Creates a virtual HomeKit bridge to expose Home Assistant devices to Apple Home.
"""
import asyncio
import logging

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_LIGHTBULB, CATEGORY_SENSOR, CATEGORY_SWITCH

logger = logging.getLogger(__name__)


class HALightAccessory(Accessory):
    """HomeKit Light accessory synced with Home Assistant."""

    category = CATEGORY_LIGHTBULB

    def __init__(self, ha_controller, entity_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ha_controller = ha_controller
        self.entity_id = entity_id

        # Add Lightbulb service
        serv_light = self.add_preload_service('Lightbulb')
        self.char_on = serv_light.configure_char('On', setter_callback=self.set_state)

    def set_state(self, value):
        """Called when HomeKit changes the light state."""
        try:
            if value:
                asyncio.create_task(self.ha_controller.turn_on_light(self.entity_id))
            else:
                asyncio.create_task(self.ha_controller.turn_off_light(self.entity_id))
            logger.info(f"HomeKit set {self.entity_id} to {value}")
        except Exception as e:
            logger.error(f"Failed to set light state: {e}")

    @Accessory.run_at_interval(3)
    async def run(self):
        """Sync state from HA to HomeKit every 3 seconds."""
        try:
            states = await self.ha_controller.get_states()
            for state in states:
                if state.get('entity_id') == self.entity_id:
                    is_on = state.get('state') == 'on'
                    self.char_on.set_value(is_on)
                    break
        except Exception as e:
            logger.error(f"Failed to sync light state: {e}")


class HASwitchAccessory(Accessory):
    """HomeKit Switch accessory synced with Home Assistant."""

    category = CATEGORY_SWITCH

    def __init__(self, ha_controller, entity_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ha_controller = ha_controller
        self.entity_id = entity_id

        serv_switch = self.add_preload_service('Switch')
        self.char_on = serv_switch.configure_char('On', setter_callback=self.set_state)

    def set_state(self, value):
        """Called when HomeKit changes the switch state."""
        try:
            if value:
                asyncio.create_task(self.ha_controller.turn_on_switch(self.entity_id))
            else:
                asyncio.create_task(self.ha_controller.turn_off_switch(self.entity_id))
            logger.info(f"HomeKit set switch {self.entity_id} to {value}")
        except Exception as e:
            logger.error(f"Failed to set switch state: {e}")

    @Accessory.run_at_interval(3)
    async def run(self):
        """Sync state from HA."""
        try:
            states = await self.ha_controller.get_states()
            for state in states:
                if state.get('entity_id') == self.entity_id:
                    is_on = state.get('state') == 'on'
                    self.char_on.set_value(is_on)
                    break
        except Exception as e:
            logger.error(f"Failed to sync switch state: {e}")


class HATemperatureSensor(Accessory):
    """HomeKit Temperature Sensor synced with Home Assistant."""

    category = CATEGORY_SENSOR

    def __init__(self, ha_controller, entity_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ha_controller = ha_controller
        self.entity_id = entity_id

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')

    @Accessory.run_at_interval(10)
    async def run(self):
        """Update temperature from HA."""
        try:
            states = await self.ha_controller.get_states()
            for state in states:
                if state.get('entity_id') == self.entity_id:
                    try:
                        temp = float(state.get('state', 0))
                        self.char_temp.set_value(temp)
                    except ValueError:
                        pass
                    break
        except Exception as e:
            logger.error(f"Failed to sync temperature: {e}")


class HomeKitBridge:
    """HomeKit Bridge for Home Assistant devices."""

    def __init__(self, ha_controller, port=51826):
        """
        Initialize HomeKit Bridge.
        
        Args:
            ha_controller: Home Assistant controller instance
            port: Port for HomeKit server (default 51826)
        """
        self.ha_controller = ha_controller
        self.port = port
        self.driver = None
        self.bridge = None

    async def discover_and_add_devices(self):
        """Discover devices from HA and add them to the bridge."""
        try:
            states = await self.ha_controller.get_states()

            for state in states:
                entity_id = state.get('entity_id', '')
                friendly_name = state.get('attributes', {}).get('friendly_name', entity_id)

                # Add lights
                if entity_id.startswith('light.'):
                    accessory = HALightAccessory(
                        self.ha_controller,
                        entity_id,
                        display_name=friendly_name
                    )
                    self.bridge.add_accessory(accessory)
                    logger.info(f"Added light: {friendly_name}")

                # Add switches
                elif entity_id.startswith('switch.'):
                    accessory = HASwitchAccessory(
                        self.ha_controller,
                        entity_id,
                        display_name=friendly_name
                    )
                    self.bridge.add_accessory(accessory)
                    logger.info(f"Added switch: {friendly_name}")

                # Add temperature sensors
                elif entity_id.startswith('sensor.') and 'temperature' in entity_id.lower():
                    unit = state.get('attributes', {}).get('unit_of_measurement', '')
                    if unit in ['°C', '°F']:
                        accessory = HATemperatureSensor(
                            self.ha_controller,
                            entity_id,
                            display_name=friendly_name
                        )
                        self.bridge.add_accessory(accessory)
                        logger.info(f"Added temperature sensor: {friendly_name}")

        except Exception as e:
            logger.error(f"Failed to discover devices: {e}")

    def start(self):
        """Start the HomeKit bridge."""
        try:
            # Create bridge accessory
            self.bridge = Bridge(display_name="Unified System Bridge")

            # Discover and add devices
            asyncio.create_task(self.discover_and_add_devices())

            # Create driver
            self.driver = AccessoryDriver(
                self.bridge,
                port=self.port,
                persist_file='homekit_state.json'
            )

            logger.info(f"HomeKit Bridge starting on port {self.port}")
            logger.info("Setup code: 123-45-678")
            logger.info("Scan QR code or use setup code to pair with Apple Home")

            # Start in background thread
            import threading
            thread = threading.Thread(target=self._run_driver, daemon=True)
            thread.start()

        except Exception as e:
            logger.error(f"Failed to start HomeKit bridge: {e}")

    def _run_driver(self):
        """Run the accessory driver (blocking)."""
        try:
            self.driver.start()
        except Exception as e:
            logger.error(f"HomeKit driver error: {e}")

    def stop(self):
        """Stop the HomeKit bridge."""
        if self.driver:
            self.driver.stop()
            logger.info("HomeKit Bridge stopped")
