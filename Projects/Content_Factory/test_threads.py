import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from threads_api.src.http_sessions.instagrapi_session import InstagrapiSession
from threads_api.src.threads_api import ThreadsAPI

# Load env from Root
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
load_dotenv(ROOT_DIR / ".env")


class SessionIDInstagrapiSession(InstagrapiSession):
    async def auth(self, username, password=None, session_id=None):
        # Override to use Session ID
        self._instagrapi_client.private.headers = self._instagrapi_headers
        if session_id:
            print(f"🔑 Logging in via Session ID: {session_id[:10]}...")
            self._instagrapi_client.login_by_sessionid(session_id)
        elif username and password:
            self._instagrapi_client.login(username, password)
        else:
            raise ValueError("No credentials provided")

        try:
            token = self._instagrapi_client.private.headers.get("Authorization", "").split("Bearer IGT:2:")[1]
        except:
            token = "SESSION_BASED_AUTH"

        # override with Threads headers
        self._instagrapi_client.private.headers = self._threads_headers
        return token


async def test_threads():
    session_id = os.getenv("INSTAGRAM_SESSION_ID")
    # Clean session ID (remove URL encoding if present, though usually it's fine)
    if session_id:
        import urllib.parse

        session_id = urllib.parse.unquote(session_id)

    username = "goncharenko9283"

    if not session_id:
        print("❌ No Session ID found in .env")
        return

    print("🧵 Initializing ThreadsAPI with Session ID...")

    api = ThreadsAPI(http_session_class=SessionIDInstagrapiSession)

    # Manually auth
    try:
        # We need to access the session object directly since we want to pass 'session_id' kwarg
        # which standard login() might not pass.
        token = await api._auth_session.auth(username, session_id=session_id)

        api.token = token
        api.is_logged_in = True

        # Determine User ID (needed?)
        # Let's try to get it from instagrapi client
        api.user_id = api._auth_session._instagrapi_client.user_id
        print(f"✅ Authenticated as User ID: {api.user_id}")

        print("🚀 Publishing test post...")
        await api.post(caption="Megaforma System Test: Threads Integration 🚀 #AI #Automated")
        print("✅ Successfully posted to Threads!")
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_threads())
