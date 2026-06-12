#!/usr/bin/env python3
"""
YouTube OAuth Setup — UnifiedCore Content Factory
Run this once to authorize YouTube API access for the Megaforma channel.

Usage:
  python3 setup_youtube_oauth_megaforma.py

This will open a browser window for Google authorization.
After approval, tokens are saved for future automated use.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Setup paths
UPLOADERS_DIR = Path(__file__).parent.resolve()
FACTORY_DIR = UPLOADERS_DIR.parent.parent
ROOT_DIR = FACTORY_DIR.parent.parent

load_dotenv(FACTORY_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=False)

# Credentials directory
CREDENTIALS_DIR = UPLOADERS_DIR / ".credentials"
CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)

# Required scopes for full YouTube automation
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",           # Upload videos
    "https://www.googleapis.com/auth/youtube",                  # Manage channel
    "https://www.googleapis.com/auth/youtube.readonly",         # Read data
    "https://www.googleapis.com/auth/yt-analytics.readonly",    # Analytics
    "https://www.googleapis.com/auth/youtube.force-ssl",        # Secure access
]

CLIENT_SECRETS_FILE = CREDENTIALS_DIR / "client_secrets.json"
TOKEN_FILE = CREDENTIALS_DIR / "youtube_token_megaforma_full.json"


def setup_oauth():
    """Run OAuth 2.0 authorization flow."""
    print("=" * 60)
    print("🔐 YouTube OAuth Setup — Megaforma Channel")
    print("=" * 60)

    if not CLIENT_SECRETS_FILE.exists():
        print(f"\n❌ client_secrets.json not found at:")
        print(f"   {CLIENT_SECRETS_FILE}")
        print("\n📋 Steps to fix:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Select project: my-home-435112")
        print("3. APIs & Services → Credentials")
        print("4. Download OAuth 2.0 Client ID (type: Desktop)")
        print(f"5. Save as: {CLIENT_SECRETS_FILE}")
        return False

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        print(f"\n📂 Client secrets: {CLIENT_SECRETS_FILE}")
        print(f"💾 Token will be saved to: {TOKEN_FILE}")
        print(f"\n🌐 Scopes requested:")
        for scope in SCOPES:
            print(f"   ✓ {scope.split('/')[-1]}")

        print("\n🚀 Opening browser for authorization...")
        print("   (If browser doesn't open, check the URL printed below)")

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CLIENT_SECRETS_FILE),
            SCOPES,
            redirect_uri="urn:ietf:wg:oauth:2.0:oob"
        )

        # Try local server first, fallback to manual
        try:
            creds = flow.run_local_server(
                port=0,
                prompt="consent",
                authorization_prompt_message="Please visit this URL:\n{url}",
                success_message="✅ Authorization successful! You can close this window.",
            )
        except Exception:
            # Manual flow for environments without browser
            auth_url, _ = flow.authorization_url(prompt="consent")
            print(f"\n🔗 Open this URL in your browser:\n{auth_url}\n")
            code = input("📝 Enter the authorization code: ").strip()
            flow.fetch_token(code=code)
            creds = flow.credentials

        # Save token
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

        print(f"\n✅ Token saved: {TOKEN_FILE}")

        # Test the connection
        youtube = build("youtube", "v3", credentials=creds)
        response = youtube.channels().list(part="snippet,statistics", mine=True).execute()

        if response.get("items"):
            ch = response["items"][0]
            name = ch["snippet"]["title"]
            subs = int(ch["statistics"].get("subscriberCount", 0))
            videos = int(ch["statistics"].get("videoCount", 0))
            print(f"\n🎉 SUCCESS! Connected to channel:")
            print(f"   📺 Channel: {name}")
            print(f"   👥 Subscribers: {subs:,}")
            print(f"   🎬 Videos: {videos}")
            print(f"\n✅ YouTube automation is now READY!")
            print(f"   Run the factory: python3 produce_content_v7_final.py")
            return True
        else:
            print("⚠️ Token saved but couldn't verify channel. Try running again.")
            return False

    except ImportError as e:
        print(f"\n❌ Missing library: {e}")
        print("Install: pip install google-auth-oauthlib google-api-python-client")
        return False
    except Exception as e:
        print(f"\n❌ OAuth failed: {e}")
        return False


if __name__ == "__main__":
    success = setup_oauth()
    sys.exit(0 if success else 1)
