#!/usr/bin/env python3
"""
YouTube User Analyzer
Analyzes the authorized user's channel, playlists, and liked videos to determine content preferences.
"""

import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Paths
current_file = Path(__file__).resolve()
CREDENTIALS_DIR = current_file.parent / ".credentials"
TOKEN_FILE = CREDENTIALS_DIR / "youtube_token.json"

def get_authenticated_service():
    if not TOKEN_FILE.exists():
        print(f"❌ Token file not found: {TOKEN_FILE}")
        return None
    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
        return build('youtube', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return None

def analyze_profile():
    youtube = get_authenticated_service()
    if not youtube: return

    print("🔍 Analyzing User Profile (@gonya90gg)...")

    # 1. Get Channel Details
    request = youtube.channels().list(mine=True, part="snippet,contentDetails,statistics")
    response = request.execute()
    
    if not response['items']:
        print("❌ No channel found.")
        return

    channel = response['items'][0]
    title = channel['snippet']['title']
    desc = channel['snippet']['description']
    views = channel['statistics']['viewCount']
    subs = channel['statistics']['subscriberCount']
    likes_playlist_id = channel['contentDetails']['relatedPlaylists']['likes']
    uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

    print(f"👤 Channel: {title}")
    print(f"📊 Stats: {subs} Subs | {views} Views")
    print(f"📝 Description: {desc[:100]}...")

    # 2. Analyze Liked Videos (Strongest Preference Signal)
    print("\n👍 Analyzing LIKED Videos (Last 20):")
    liked_req = youtube.playlistItems().list(
        playlistId=likes_playlist_id,
        part="snippet",
        maxResults=20
    )
    liked_res = liked_req.execute()
    
    liked_keywords = []
    for item in liked_res['items']:
        vid_title = item['snippet']['title']
        vid_desc = item['snippet']['description'][:100].replace('\n', ' ')
        print(f"   - {vid_title}")
        liked_keywords.append(vid_title)

    # 3. Analyze Playlists (Saved Content)
    print("\nDj Analyzing Playlists (Saved Collections):")
    pl_req = youtube.playlists().list(
        mine=True,
        part="snippet,contentDetails",
        maxResults=10
    )
    pl_res = pl_req.execute()
    
    for item in pl_res['items']:
        pl_title = item['snippet']['title']
        count = item['contentDetails']['itemCount']
        print(f"   - [{count} vids] {pl_title}")

    # 4. Generate Strategy
    print("\n🧠 AI STRATEGY INSIGHTS:")
    print("   Based on your 'Likes' and 'Playlists', the system detects these core interests:")
    # Simple keyword extraction
    all_text = " ".join(liked_keywords).lower()
    
    if "ai" in all_text or "gpt" in all_text:
        print("   ✅ High Interest: Artificial Intelligence")
    if "news" in all_text or "war" in all_text or "israel" in all_text:
        print("   ✅ High Interest: Geopolitics / News")
    if "crypto" in all_text or "bitcoin" in all_text:
        print("   ✅ High Interest: Crypto/Finance")
    if "cartoon" in all_text or "animation" in all_text:
        print("   ✅ High Interest: Animation/Visuals")

if __name__ == "__main__":
    analyze_profile()
