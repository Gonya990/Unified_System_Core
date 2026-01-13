import sys
from pathlib import Path

# Setup paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
FACTORY_DIR = ROOT_DIR / "Projects/Content_Factory"
SRC_DIR = FACTORY_DIR / "src"
sys.path.append(str(SRC_DIR / "uploaders"))
sys.path.append(str(SRC_DIR / "pipeline"))

from account_manager import AccountManager
from youtube_uploader import upload_video


def main():
    video_path = Path("/Users/macbook/Documents/Unified_System/outputs/weekly_en_20260113_final.mp4")
    if not video_path.exists():
        print(f"❌ Video file not found: {video_path}")
        return

    print("🚀 Starting Manual Rescue Upload...")

    acc_manager = AccountManager()
    yt_accounts = acc_manager.get_accounts("youtube")

    title = "Vertical Farming: Feeding the World (2026)"
    description = "New AI vision: Vertical farming feeding the world.\n\n#AI #Tech #Future #Geopolitics #Megaforma"
    tags = ["AI", "Future", "Tech", "News", "Geopolitics", "Megaforma", "Vertical Farming"]

    for acc in yt_accounts:
        print(f"📡 Uploading to channel: {acc.get('name')}")
        token_file = acc.get("token_file")

        # Resolve token file path relative to uploaders dir if simple name
        if token_file and not Path(token_file).is_absolute():
            # youtube_uploader expects it in .credentials if passed as name, or we pass absolute path
            # Actually youtube_uploader.py lines 35-36 suggest we can pass a path.
            # but get_authenticated_service lines 35 uses it as Path(token_file).
            # If it's just "youtube_token.json", it might be relative to CWD or script.
            # youtube_uploader.py defines TOKEN_FILE in .credentials.
            # Best to try passing full path if we can resolve it, or trust youtube_uploader's default if it's the default file.
            pass

        # We'll just pass the token_file string from config, youtube_uploader should handle it or we adjust if it fails.
        # But wait, youtube_uploader.py logic:
        # CREDENTIALS_DIR = UPLOADERS_DIR / ".credentials"
        # TOKEN_FILE = CREDENTIALS_DIR / "youtube_token.json"
        # if token_file arg is provided, it uses that Path(token_file).
        # So if acc config says "youtube_token.json" and we run from ROOT_DIR, Path("youtube_token.json") won't be found if it's in .credentials.

        real_token_path = SRC_DIR / "uploaders/.credentials" / token_file
        if not real_token_path.exists():
            # Try just the file name as per default logic?
            # If token_file is None, it uses default.
            if token_file == "youtube_token.json":
                real_token_path = None  # Trigger default in upload_video
            else:
                print(f"⚠️ Token file {real_token_path} not found.")

        success = upload_video(
            video_path,
            title=title,
            description=description,
            tags=tags,
            privacy_status="public",
            token_file=real_token_path,
        )

        if success:
            print("✅ Upload Successful!")
        else:
            print("❌ Upload Failed.")


if __name__ == "__main__":
    main()
