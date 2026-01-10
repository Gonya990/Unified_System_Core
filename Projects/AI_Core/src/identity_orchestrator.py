import logging
import json
from typing import Optional, Dict, Any, List
from google.oauth2.credentials import Credentials

try:
    from google_auth import GoogleAuthManager
    from calendar_client import CalendarClient
    from gmail_client import GmailClient
except ImportError:
    # Fallback for when running setup without full env
    GoogleAuthManager = None
    CalendarClient = None
    GmailClient = None

logger = logging.getLogger("IdentityOrchestrator")

class IdentityOrchestrator:
    """
    The Passport: Manages User Identity, Access Control (RBAC), and External Account Sessions.
    """
    
    def __init__(self, db, config_manager, auth_manager: Optional[GoogleAuthManager] = None):
        self.db = db
        self.config = config_manager
        self.auth_manager = auth_manager
        
        # Load Admin Config
        self.allowed_users = self._load_allowed_users()
        
    def _load_allowed_users(self) -> List[int]:
        """Loads allowed users from Env and YAML via ConfigManager logic."""
        # Simplified replication of previous logic, ideally ConfigManager handles this
        users_str = self.config.get("ALLOWED_USERS", "708531393,5569219290,578363419")
        try:
             return [int(uid.strip()) for uid in users_str.split(",") if uid.strip()]
        except:
             return [708531393] # Safety fallback

    def check_access(self, user_id: int) -> bool:
        """
        Check if user is approved. 
        Auto-approves if in ALLOWED_USERS whitelist.
        """
        if not self.db.is_approved(user_id):
            if user_id in self.allowed_users:
                self.db.approve_user(user_id, True)
                logger.info(f"IdentityOrchestrator: Auto-approved whitelisted user {user_id}")
                return True
            return False
        return True

    def get_google_services(self, user_id: int) -> Dict[str, Any]:
        """
        Returns initialized clients for Google Services (Calendar, Gmail) if authorized.
        """
        services = {"calendar": None, "gmail": None}
        
        user_data = self.db.get_user(user_id)
        if not user_data or not user_data.get('is_google_connected') or not user_data.get('google_creds'):
            return services
            
        try:
            creds_dict = json.loads(user_data['google_creds'])
            
            if CalendarClient:
                services["calendar"] = CalendarClient(credentials_dict=creds_dict)
                
            if GmailClient:
                services["gmail"] = GmailClient(credentials_dict=creds_dict)
                
        except Exception as e:
            logger.error(f"IdentityOrchestrator: Failed to init services for {user_id}: {e}")
            
        return services

    def get_auth_url(self, user_id: int) -> Optional[str]:
        """Proxy to AuthManager."""
        if self.auth_manager:
            return self.auth_manager.get_auth_url(user_id)
        return None
