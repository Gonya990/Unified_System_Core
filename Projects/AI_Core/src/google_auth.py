import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

# Scopes required
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Port for the OAuth callback server
OAUTH_CALLBACK_PORT = 8085
REDIRECT_URI = f'http://localhost:{OAUTH_CALLBACK_PORT}/oauth2callback'


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler to capture OAuth callback."""

    def log_message(self, format, *args):
        # Suppress HTTP logs
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/oauth2callback':
            params = parse_qs(parsed.query)
            if 'code' in params:
                self.server.auth_code = params['code'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'''
                    <html><body style="font-family: Arial; text-align: center; padding-top: 50px;">
                    <h1>Authorization Successful!</h1>
                    <p>You can close this window and return to Telegram.</p>
                    </body></html>
                ''')
            else:
                self.server.auth_code = None
                error = params.get('error', ['Unknown error'])[0]
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'''
                    <html><body style="font-family: Arial; text-align: center; padding-top: 50px;">
                    <h1>Authorization Failed</h1>
                    <p>Error: {error}</p>
                    </body></html>
                '''.encode())
        else:
            self.send_response(404)
            self.end_headers()


class GoogleAuthManager:
    def __init__(self, client_secrets_file="client_secret.json"):
        self.client_secrets_file = client_secrets_file
        self._pending_flows = {}  # user_id -> Flow

        if not os.path.exists(self.client_secrets_file):
            logger.warning(f"Client secrets file {self.client_secrets_file} not found locally.")

    def get_auth_url(self, user_id: int = None):
        """Generate Authorization URL for the user."""
        try:
            flow = Flow.from_client_secrets_file(
                self.client_secrets_file,
                scopes=SCOPES,
                redirect_uri=REDIRECT_URI
            )
            auth_url, state = flow.authorization_url(
                prompt='consent',
                access_type='offline',
                include_granted_scopes='true'
            )

            # Store flow for later code exchange
            if user_id:
                self._pending_flows[user_id] = flow
            else:
                self._pending_flows['default'] = flow

            logger.info(f"Generated auth URL for user {user_id}")
            return auth_url
        except Exception as e:
            logger.error(f"Error generating auth URL: {e}")
            return None

    def exchange_code(self, code: str, user_id: int = None):
        """Exchange auth code for credentials."""
        try:
            # Try to get stored flow, or create new one
            flow = self._pending_flows.pop(user_id, None) or self._pending_flows.pop('default', None)

            if not flow:
                # Create new flow if none stored
                flow = Flow.from_client_secrets_file(
                    self.client_secrets_file,
                    scopes=SCOPES,
                    redirect_uri=REDIRECT_URI
                )

            flow.fetch_token(code=code)
            logger.info(f"Successfully exchanged code for user {user_id}")
            return flow.credentials
        except Exception as e:
            logger.error(f"Error exchanging code: {e}")
            return None

    def start_local_server(self, timeout: int = 120):
        """
        Start a local HTTP server to capture OAuth callback.
        Returns the auth code or None if timeout/error.

        Note: This only works if the bot runs on a machine where
        the user can access localhost. For remote bots (like Docker),
        the manual code paste method should be used instead.
        """
        server = HTTPServer(('localhost', OAUTH_CALLBACK_PORT), OAuthCallbackHandler)
        server.auth_code = None
        server.timeout = timeout

        def serve():
            server.handle_request()

        thread = threading.Thread(target=serve)
        thread.start()
        thread.join(timeout=timeout)

        return server.auth_code
