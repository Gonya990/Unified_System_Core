#!/usr/bin/env python3
"""
YouTube Uploader Module
Automates video uploads to YouTube using the YouTube Data API v3.
"""

import argparse
import time
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Scopes needed for uploading
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Paths
current_file = Path(__file__).resolve()
UPLOADERS_DIR = current_file.parent
CREDENTIALS_DIR = UPLOADERS_DIR / ".credentials"
CLIENT_SECRETS_FILE = CREDENTIALS_DIR / "client_secrets.json"
TOKEN_FILE = CREDENTIALS_DIR / "youtube_token.json"

CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)

def get_authenticated_service(token_file=None):
    """Authenticates the user and returns the YouTube API service."""
    creds = None

    # Use provided token_file or default
    active_token_file = Path(token_file) if token_file else TOKEN_FILE

    # Check if token exists
    if active_token_file.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(active_token_file), SCOPES)
        except Exception as e:
            print(f"⚠️ Error loading token: {e}")
            creds = None

    # If no valid token, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"❌ Token refresh failed: {e}")
                creds = None

        if not creds:
            if not CLIENT_SECRETS_FILE.exists():
                print(f"❌ Error: Client secrets file not found at {CLIENT_SECRETS_FILE}")
                print("ℹ️  Please download 'client_secrets.json' from Google Cloud Console (OAuth 2.0 Client ID) and place it there.")
                return None

            print("🔐 Initiating OAuth 2.0 login flow...")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(active_token_file, 'w') as token:
            token.write(creds.to_json())
            print(f"✅ Token saved to {active_token_file}")

    try:
        return build('youtube', 'v3', credentials=creds)
    except HttpError as e:
        print(f"❌ An HTTP error occurred: {e}")
        return None

def upload_video(file_path: Path, title, description, tags=None, category_id="28", privacy_status="private", token_file=None):
    """
    Uploads a video to YouTube.
    category_id "28" is 'Science & Technology'. "22" is 'People & Blogs'. "25" is 'News & Politics'.
    """
    youtube = get_authenticated_service(token_file=token_file)
    if not youtube:
        return False

    if not file_path.exists():
        print(f"❌ Video file not found: {file_path}")
        return False

    tags = tags or []

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status,
            'selfDeclaredMadeForKids': False
        }
    }

    print(f"🚀 Uploading '{title}'...")

    # Chunk size: 4MB
    media = MediaFileUpload(str(file_path), chunksize=4*1024*1024, resumable=True, mimetype='video/mp4')

    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"📊 Uploaded {int(status.progress() * 100)}%")
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                print(f"⚠️ Media upload failed with error {e}. Retrying in 5 seconds...")
                time.sleep(5)
                continue
            else:
                print(f"❌ Upload failed with error: {e}")
                return False

    print(f"✅ Upload Complete! Video ID: {response['id']}")
    print(f"🔗 URL: https://youtu.be/{response['id']}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YouTube Uploader')
    parser.add_argument('--file', required=True, help='Path to video file')
    parser.add_argument('--title', required=True, help='Video title')
    parser.add_argument('--description', default="Uploaded by AI Content Factory", help='Video description')
    parser.add_argument('--tags', default="", help='Comma separated tags')
    parser.add_argument('--privacy', default="private", choices=['public', 'private', 'unlisted'], help='Privacy status')

    args = parser.parse_args()

    tags_list = [t.strip() for t in args.tags.split(',')] if args.tags else []

    upload_video(Path(args.file), args.title, args.description, tags_list, privacy_status=args.privacy)
