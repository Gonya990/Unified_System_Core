import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

logger = logging.getLogger(__name__)

# Default port for local OAuth callback server (if used)
OAUTH_CALLBACK_PORT = 8080

# Scopes required - must match OAuth consent screen configuration
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/youtube.upload",
    "openid",
]

# Redirect URI - must match what's configured in Google Cloud Console
# Using http://localhost (no port, no path) as it's pre-authorized for desktop apps
REDIRECT_URI = "http://localhost"


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler to capture OAuth callback."""

    def log_message(self, format, *args):
        # Suppress HTTP logs
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/oauth2callback":
            params = parse_qs(parsed.query)
            if "code" in params:
                self.server.auth_code = params["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                    <html><body style="font-family: Arial; text-align: center;
                    padding-top: 50px;">
                    <h1>Authorization Successful!</h1>
                    <p>You can close this window and return to Telegram.</p>
                    </body></html>
                """)
            else:
                self.server.auth_code = None
                error = params.get("error", ["Unknown error"])[0]
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(
                    f"""
                    <html><body style="font-family: Arial; text-align: center;
                    padding-top: 50px;">
                    <h1>Authorization Failed</h1>
                    <p>Error: {error}</p>
                    </body></html>
                """.encode()
                )
        else:
            self.send_response(404)
            self.end_headers()


# Directory for persistent tokens (mounted from ./secrets in docker-compose)
SECRETS_DIR = os.getenv("TOKENS_PATH", "/app/data/tokens")
if not os.path.exists(SECRETS_DIR):
    try:
        os.makedirs(SECRETS_DIR, exist_ok=True)
    except Exception:
        # Fallback for local dev without docker or permission issues
        SECRETS_DIR = "."


class GoogleAuthManager:
    def __init__(self, client_secrets_file="client_secret.json"):
        # Allow environment variable override
        self.client_secrets_file = os.getenv("GOOGLE_CLIENT_SECRETS", client_secrets_file)
        self._pending_flows = {}  # user_id -> Flow

        if not os.path.exists(self.client_secrets_file):
            logger.warning(f"Client secrets file {self.client_secrets_file} not found locally.")

    def get_auth_url(self, user_id: int = None):
        """Generate Authorization URL for the user."""
        try:
            flow = Flow.from_client_secrets_file(self.client_secrets_file, scopes=SCOPES, redirect_uri=REDIRECT_URI)
            auth_url, state = flow.authorization_url(
                prompt="consent", access_type="offline", include_granted_scopes="true"
            )

            # Store flow for later code exchange
            if user_id:
                self._pending_flows[user_id] = flow
            else:
                self._pending_flows["default"] = flow

            logger.info(f"Generated auth URL for user {user_id}")
            return auth_url
        except Exception as e:
            logger.error(f"Error generating auth URL: {e}")
            return None

    def exchange_code(self, code: str, user_id: int = None):
        """Exchange auth code for credentials."""
        try:
            # Try to get stored flow, or create new one
            flow = self._pending_flows.pop(user_id, None) or self._pending_flows.pop("default", None)

            if not flow:
                # Create new flow if none stored
                flow = Flow.from_client_secrets_file(self.client_secrets_file, scopes=SCOPES, redirect_uri=REDIRECT_URI)

            flow.fetch_token(code=code)
            creds = flow.credentials

            # Save to persistent file
            if user_id:
                token_path = os.path.join(SECRETS_DIR, f"token_{user_id}.json")
                with open(token_path, "w") as token_file:
                    token_file.write(creds.to_json())
                logger.info(f"Saved persistent token to {token_path}")

            logger.info(f"Successfully exchanged code for user {user_id}")
            return creds
        except Exception as e:
            logger.error(f"Error exchanging code: {e}")
            return None

    def load_credentials(self, user_id: int):
        """Load credentials from persistent file."""
        try:
            token_path = os.path.join(SECRETS_DIR, f"token_{user_id}.json")
            if os.path.exists(token_path):
                logger.info(f"Loading persistent token for {user_id} from {token_path}")
                return Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            logger.error(f"Error loading persistent credentials: {e}")
        return None

    def start_local_server(self, timeout: int = 120):
        """
        Start a local HTTP server to capture OAuth callback.
        Returns the auth code or None if timeout/error.

        Note: This only works if the bot runs on a machine where
        the user can access localhost. For remote bots (like Docker),
        the manual code paste method should be used instead.
        """
        server = HTTPServer(("localhost", OAUTH_CALLBACK_PORT), OAuthCallbackHandler)
        server.auth_code = None
        server.timeout = timeout

        def serve():
            server.handle_request()

        thread = threading.Thread(target=serve)
        thread.start()
        thread.join(timeout=timeout)

        return server.auth_code
