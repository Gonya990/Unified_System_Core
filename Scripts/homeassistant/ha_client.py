#!/usr/bin/env python3
"""
Home Assistant API Client
Provides full programmatic control over HA integrations, entities, and services.
"""

import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class HAConfig:
    """Home Assistant configuration"""
    url: str = "http://100.81.133.25:8123"
    token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhYWQ3YjJiN2M4NDg0NWEzODA0YTU4MWUwYWYyNjk3MyIsImlhdCI6MTc2Njg0NTEyNywiZXhwIjoyMDgyMjA1MTI3fQ.H4iTu7T_IYaom9ecHVA5EVBJ-cFBXyFXwkgykPdDcjc"
    timeout: int = 30


class HomeAssistantClient:
    """Client for interacting with Home Assistant REST API"""
    
    def __init__(self, config: Optional[HAConfig] = None):
        self.config = config or HAConfig()
        self.headers = {
            "Authorization": f"Bearer {self.config.token}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request to HA API"""
        url = f"{self.config.url}/api/{endpoint}"
        kwargs.setdefault('headers', self.headers)
        kwargs.setdefault('timeout', self.config.timeout)
        
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    
    def get(self, endpoint: str) -> Any:
        """GET request"""
        return self._request('GET', endpoint).json()
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Any:
        """POST request"""
        return self._request('POST', endpoint, json=data).json()
    
    # ========== General API ==========
    
    def get_config(self) -> Dict:
        """Get HA configuration"""
        return self.get('config')
    
    def get_states(self) -> List[Dict]:
        """Get all entity states"""
        return self.get('states')
    
    def get_entity_state(self, entity_id: str) -> Dict:
        """Get specific entity state"""
        return self.get(f'states/{entity_id}')
    
    def get_services(self) -> List[Dict]:
        """Get all available services"""
        return self.get('services')
    
    def call_service(self, domain: str, service: str, entity_id: Optional[str] = None, **kwargs) -> List[Dict]:
        """Call a service"""
        data = kwargs
        if entity_id:
            data['entity_id'] = entity_id
        return self.post(f'services/{domain}/{service}', data)
    
    # ========== Integrations ==========
    
    def get_integrations(self) -> List[Dict]:
        """Get all integration entries"""
        # Note: This endpoint may not be available in all HA versions
        # Alternative: parse .storage/core.config_entries directly
        try:
            return self.get('config_entries/entry')
        except:
            # Fallback: try to get from states
            return []
    
    def get_homekit_integration(self) -> Optional[Dict]:
        """Get HomeKit Bridge integration details"""
        integrations = self.get_integrations()
        for integration in integrations:
            if integration.get('domain') == 'homekit':
                return integration
        return None
    
    def reload_integration(self, entry_id: str) -> Dict:
        """Reload a config entry"""
        return self.post(f'config/config_entries/{entry_id}/reload')
    
    # ========== HomeKit Specific ==========
    
    def get_homekit_status(self) -> Dict:
        """Get HomeKit Bridge status and pairing info"""
        hk = self.get_homekit_integration()
        if not hk:
            return {"status": "not_configured"}
        
        return {
            "status": "configured",
            "entry_id": hk.get('entry_id'),
            "title": hk.get('title'),
            "domain": hk.get('domain'),
            "state": hk.get('state'),
            "options": hk.get('options', {}),
            "data": hk.get('data', {})
        }
    
    def restart_homekit(self) -> Dict:
        """Restart HomeKit Bridge"""
        hk = self.get_homekit_integration()
        if not hk:
            return {"error": "HomeKit not configured"}
        
        return self.reload_integration(hk['entry_id'])
    
    # ========== Lights ==========
    
    def turn_on_light(self, entity_id: str, **kwargs) -> List[Dict]:
        """Turn on a light with optional parameters"""
        return self.call_service('light', 'turn_on', entity_id, **kwargs)
    
    def turn_off_light(self, entity_id: str) -> List[Dict]:
        """Turn off a light"""
        return self.call_service('light', 'turn_off', entity_id)
    
    # ========== Switches ==========
    
    def turn_on_switch(self, entity_id: str) -> List[Dict]:
        """Turn on a switch"""
        return self.call_service('switch', 'turn_on', entity_id)
    
    def turn_off_switch(self, entity_id: str) -> List[Dict]:
        """Turn off a switch"""
        return self.call_service('switch', 'turn_off', entity_id)
    
    # ========== Climate ==========
    
    def set_temperature(self, entity_id: str, temperature: float) -> List[Dict]:
        """Set climate temperature"""
        return self.call_service('climate', 'set_temperature', entity_id, temperature=temperature)
    
    # ========== Diagnostics ==========
    
    def check_health(self) -> Dict:
        """Check HA health and connectivity"""
        try:
            config = self.get_config()
            states_count = len(self.get_states())
            hk_status = self.get_homekit_status()
            
            return {
                "status": "ok",
                "healthy": True,
                "version": config.get('version'),
                "location_name": config.get('location_name'),
                "entities_count": states_count,
                "homekit_status": hk_status
            }
        except Exception as e:
            return {
                "status": "error",
                "healthy": False,
                "message": str(e),
                "error": str(e)
            }


# ========== CLI Usage ==========

def main():
    """CLI interface for testing"""
    import sys
    
    client = HomeAssistantClient()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ha_client.py health          # Check HA health")
        print("  python ha_client.py homekit         # Get HomeKit status")
        print("  python ha_client.py restart_homekit # Restart HomeKit Bridge")
        print("  python ha_client.py states          # List all entities")
        print("  python ha_client.py integrations    # List integrations")
        return
    
    command = sys.argv[1]
    
    if command == 'health':
        result = client.check_health()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == 'homekit':
        result = client.get_homekit_status()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == 'restart_homekit':
        result = client.restart_homekit()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == 'states':
        result = client.get_states()
        print(f"Total entities: {len(result)}")
        for state in result:  # Show all
            print(f"  {state['entity_id']}: {state['state']}")
    
    elif command == 'integrations':
        result = client.get_integrations()
        print(f"Total integrations: {len(result)}")
        for integration in result:
            print(f"  {integration['domain']}: {integration['title']}")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
