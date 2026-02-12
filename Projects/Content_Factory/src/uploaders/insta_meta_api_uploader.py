import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

def upload_reel_meta_api(video_path: str, caption: str) -> bool:
    """
    Upload Instagram Reel using official Meta Graph API.
    
    Requirements:
    - INSTAGRAM_BUSINESS_ACCOUNT_ID
    - META_ACCESS_TOKEN (with business_content_publish permission)
    
    The video must be hosted on a publicly accessible URL.
    """

    ig_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
    access_token = os.getenv('META_ACCESS_TOKEN')

    if not ig_account_id or not access_token:
        print("❌ Missing INSTAGRAM_BUSINESS_ACCOUNT_ID or META_ACCESS_TOKEN")
        print("Please set these in your .env file")
        return False

    print(f"📸 Starting Meta API Reel Upload: {video_path}")

    # Step 1: Upload video to a public URL (or use existing hosted URL)
    # For now, we need the video to be publicly accessible
    # Meta API requires video_url parameter

    # TODO: Implement video hosting (S3, Cloudflare R2, etc.)
    # For now, this is a placeholder showing the API structure

    video_url = "YOUR_PUBLIC_VIDEO_URL_HERE"

    # Step 2: Create Media Container
    container_url = f"https://graph.facebook.com/v21.0/{ig_account_id}/media"

    container_params = {
        'media_type': 'REELS',
        'video_url': video_url,
        'caption': caption,
        'access_token': access_token,
        'share_to_feed': True  # Also post to main feed
    }

    print("📦 Creating media container...")
    container_response = requests.post(container_url, data=container_params)

    if container_response.status_code != 200:
        print(f"❌ Container creation failed: {container_response.text}")
        return False

    creation_id = container_response.json().get('id')
    print(f"✅ Container created: {creation_id}")

    # Step 3: Wait for processing (recommended 15+ seconds)
    print("⏳ Waiting for video processing...")
    time.sleep(20)

    # Step 4: Publish the reel
    publish_url = f"https://graph.facebook.com/v21.0/{ig_account_id}/media_publish"

    publish_params = {
        'creation_id': creation_id,
        'access_token': access_token
    }

    print("📤 Publishing reel...")
    publish_response = requests.post(publish_url, data=publish_params)

    if publish_response.status_code != 200:
        print(f"❌ Publishing failed: {publish_response.text}")
        return False

    media_id = publish_response.json().get('id')
    print(f"✅ Reel published successfully! Media ID: {media_id}")
    return True

if __name__ == '__main__':
    # Test
    print("Meta Instagram API Uploader Ready")
    print("To use: Set INSTAGRAM_BUSINESS_ACCOUNT_ID and META_ACCESS_TOKEN in .env")
