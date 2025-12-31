import os
import logging
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

# Scopes required
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleAuthManager:
    def __init__(self, client_secrets_file="client_secret.json"):
        self.client_secrets_file = client_secrets_file
        # Check if file exists, or try to load from ENV
        if not os.path.exists(self.client_secrets_file):
            logger.warning(f"Client secrets file {self.client_secrets_file} not found locally.")

    def get_auth_url(self):
        """Generate Authorization URL for the user."""
        try:
            flow = Flow.from_client_secrets_file(
                self.client_secrets_file,
                scopes=SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )
            auth_url, _ = flow.authorization_url(prompt='consent')
            return auth_url
        except Exception as e:
            logger.error(f"Error generating auth URL: {e}")
            return None

    def exchange_code(self, code: str):
        """Exchange auth code for credentials."""
        try:
            flow = Flow.from_client_secrets_file(
                self.client_secrets_file,
                scopes=SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )
            flow.fetch_token(code=code)
            return flow.credentials
        except Exception as e:
            logger.error(f"Error exchanging code: {e}")
            return None
