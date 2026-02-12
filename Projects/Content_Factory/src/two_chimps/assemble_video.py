import time
from pathlib import Path

import PIL.Image
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Patch Pillow for MoviePy 1.x
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import AudioFileClip, CompositeVideoClip, ImageClip

# Paths
ROOT = Path(__file__).parent
ASSETS_DIR = ROOT / "assets"
CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
AUDIO_DIR = CONTEXT_DIR / "audio_output"
VIDEO_DIR = CONTEXT_DIR / "final_videos"
CREDENTIALS_FILE = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/config/gmail_credentials.json")
TOKEN_FILE = ROOT / "youtube_token.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

if not VIDEO_DIR.exists():
    VIDEO_DIR.mkdir()

def get_authenticated_service():
    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception:
            print("⚠️ Token invalid, refreshing...")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"❌ Refresh failed: {e}. Re-authenticating...")
                creds = None

        if not creds:
            if not CREDENTIALS_FILE.exists():
                print(f"❌ Credentials not found at {CREDENTIALS_FILE}")
                return None

            print(f"🔐 Initiating Login using: {CREDENTIALS_FILE.name}")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES)
            # Use a fixed port to avoid random port issues if specific redirect URIs are set
            creds = flow.run_local_server(port=8080)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(video_path, title, description):
    print(f"🚀 Uploading to YouTube: {title}")
    youtube = get_authenticated_service()
    if not youtube:
        print("❌ YouTube auth failed.")
        return

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['AI', 'DinoTalk', 'Podcast', 'TwoDinos'],
            'categoryId': '28' # Science & Tech
        },
        'status': {
            'privacyStatus': 'unlisted', # Safer for testing
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(str(video_path),
                          chunksize=4*1024*1024,
                          resumable=True,
                          mimetype='video/mp4')

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
                print(f"☁️ Uploading: {int(status.progress() * 100)}%")
        except Exception as e:
             if "50" in str(e): # 500/502/503
                 time.sleep(5)
                 continue
             else:
                 print(f"❌ Upload Error: {e}")
                 return

    print(f"✅ Upload Complete! URL: https://youtu.be/{response['id']}")

def make_video(audio_path):
    print(f"🎬 Assembling Dino Talk for: {audio_path.name}...")

    try:
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration

        # Load Dino Assets
        img_skeptic = ImageClip(str(ASSETS_DIR / "dino_skeptic.png")).set_duration(duration)
        img_enthusiast = ImageClip(str(ASSETS_DIR / "dino_enthusiast.png")).set_duration(duration)
        bg = ImageClip(str(ASSETS_DIR / "dino_studio_background.png")).set_duration(duration)

        # Layout
        img_skeptic = img_skeptic.resize(height=450).set_position(("left", "bottom"))
        img_enthusiast = img_enthusiast.resize(height=450).set_position(("right", "bottom"))

        final_video = CompositeVideoClip(
            [bg, img_skeptic, img_enthusiast],
            size=bg.size
        )

        final_video = final_video.set_audio(audio)

        output_path = VIDEO_DIR / f"{audio_path.stem}.mp4"
        final_video.write_videofile(
            str(output_path),
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        print(f"✅ Video saved: {output_path.name}")

        # Auto-Upload
        title = f"Dino Talk: {audio_path.stem.replace('_', ' ').title()}"
        description = "AI-generated podcast hosted by T-Rex and Triceratops.\n\nCreated by Unified System Core."
        upload_to_youtube(output_path, title, description)

    except Exception as e:
        print(f"❌ Error assembling/uploading video: {e}")

if __name__ == "__main__":
    if not AUDIO_DIR.exists():
        print("❌ Audio output directory not found.")
        exit()

    for audio_file in AUDIO_DIR.glob("*.mp3"):
        # We generally expect one file for the test run
        make_video(audio_file)
