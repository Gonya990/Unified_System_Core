#!/usr/bin/env python3
"""
YouTube OAuth Setup — UnifiedSystem Channel
https://www.youtube.com/@UnifiedSystem-l6d
"""

import json
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

CREDS_DIR = Path(__file__).parent / ".credentials"
CLIENT_SECRETS = CREDS_DIR / "client_secrets.json"
TOKEN_FILE = CREDS_DIR / "youtube_token_unifiedsystem.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

print("=" * 60)
print("🔐 YouTube OAuth Setup — UnifiedSystem Channel")
print("=" * 60)
print(f"\n📂 Client secrets: {CLIENT_SECRETS}")
print(f"💾 Token will be saved to: {TOKEN_FILE}")
print("\n🌐 Scopes requested:")
for s in SCOPES:
    print(f"   ✓ {s.split('/')[-1]}")

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError as e:
    print(f"\n❌ Missing library: {e}")
    print("Install: pip install google-auth-oauthlib google-api-python-client")
    raise SystemExit(1) from e

print("\n⚠️  IMPORTANT: Sign in with the @UnifiedSystem-l6d account!")
print("   (NOT your personal account)")
print("\n🚀 Opening browser for authorization...")

flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), scopes=SCOPES)
creds = flow.run_local_server(
    port=0,
    prompt="consent",
    access_type="offline",
    open_browser=True,
)

# Save token
token_data = {
    "token": creds.token,
    "refresh_token": creds.refresh_token,
    "token_uri": creds.token_uri,
    "client_id": creds.client_id,
    "client_secret": creds.client_secret,
    "scopes": list(creds.scopes or SCOPES),
    "channel": "unifiedsystem",
}
CREDS_DIR.mkdir(parents=True, exist_ok=True)
with open(TOKEN_FILE, "w") as f:
    json.dump(token_data, f, indent=2)

print(f"\n✅ Token saved: {TOKEN_FILE}")

# Verify
try:
    youtube = build("youtube", "v3", credentials=creds)
    resp = youtube.channels().list(part="snippet,statistics", mine=True).execute()
    items = resp.get("items", [])
    if items:
        ch = items[0]
        print("\n🎉 VERIFIED — Channel connected!")
        print(f"   Channel:  {ch['snippet']['title']}")
        print(f"   Handle:   {ch['snippet'].get('customUrl', 'n/a')}")
        print(f"   Subs:     {ch['statistics'].get('subscriberCount', '?')}")
        print(f"   Videos:   {ch['statistics'].get('videoCount', '?')}")
        print(f"   Channel ID: {ch['id']}")
        print("\n📝 Add to youtube_channels_config.py:")
        print(f'   "channel_id": "{ch["id"]}",')
        print(f'   "handle": "{ch["snippet"].get("customUrl", "?")}",')
    else:
        print("⚠️  No channel found — did you log into the right account?")
except Exception as e:
    print(f"\n❌ Verification failed: {e}")
    print("   Token saved but channel check failed.")
    print("   Make sure YouTube Data API v3 is enabled.")
