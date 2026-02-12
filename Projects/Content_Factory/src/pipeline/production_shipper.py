#!/usr/bin/env python3
import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add src to path
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir.parent))

# Load root .env
root_env = current_dir.parent.parent.parent.parent / ".env"
load_dotenv(root_env)

import subprocess

from uploaders.insta_uploader import upload_reel
from uploaders.threads_browser import ThreadsBrowser
from uploaders.youtube_uploader import upload_video


def get_video_duration(path):
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return 0


async def task_youtube(video_path, title, description, tags, skip):
    if skip:
        print("⏭ Skipping YouTube (Requested)")
        return

    creds_dir = current_dir.parent / "uploaders" / ".credentials"
    if not (creds_dir / "youtube_token.json").exists():
        print("⏭ Skipping YouTube: No token found.")
        return

    print("📺 Shipping to YouTube...")
    try:
        # Run blocking upload in a thread
        await asyncio.to_thread(
            upload_video, Path(video_path), title, description, tags, "28", "public"
        )
    except Exception as e:
        print(f"⚠️ YouTube failed: {e}")


async def task_instagram(video_path, title, description, skip):
    if skip:
        print("⏭ Skipping Instagram (Requested)")
        return

    print("📸 Shipping to Instagram...")
    ig_video = video_path
    duration = get_video_duration(video_path)

    if duration > 900:
        print(f"⚠️ Video too long for Instagram ({duration:.1f}s). Trimming to 14:59...")
        trimmed_path = video_path.replace(".mp4", "_ig_trimmed.mp4")
        try:
            # ffmpeg is blocking but fast enough or we can use asyncio.subprocess
            # keeping subprocess.run is creating a blocking call but executed in parallel
            # with other tasks if wrapped in to_thread, or just acceptable.
            # safe to execute in this async func as long as it doesn't block others for *too* long
            # but better to separate heavy compute.
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    video_path,
                    "-t",
                    "899",
                    "-c",
                    "copy",
                    trimmed_path,
                ],
                check=True,
                capture_output=True,
            )
            ig_video = trimmed_path
            print(f"✅ Trimmed version created: {trimmed_path}")
        except Exception as e:
            print(f"❌ Trimming failed: {e}")
            return

    try:
        caption = f"{title}\n\n{description}\n\n#AI #Technology #Future #2026"
        # Blocking call to instagrapi
        await asyncio.to_thread(upload_reel, ig_video, caption[:2000])

        if ig_video != video_path and os.path.exists(ig_video):
            os.remove(ig_video)  # Cleanup
    except Exception as e:
        print(f"⚠️ Instagram failed: {e}")


async def task_threads(video_path, title, description, skip):
    if skip:
        print("⏭ Skipping Threads (Requested)")
        return

    print("🧵 Shipping to Threads...")
    try:
        threads = ThreadsBrowser(headless=True)
        await threads.start()
        threads_text = f"🚀 {title}\n\n{description[:300]}..."
        await asyncio.wait_for(threads.post(threads_text, video_path), timeout=300)
        await threads.close()
        print("✅ Threads shipped!")
    except Exception as e:
        print(f"⚠️ Threads failed: {e}")


async def task_community(video_path, title, description, skip):
    if skip:
        print("⏭ Skipping YouTube Community (Requested)")
        return

    print("📢 Posting to YouTube Community...")
    try:
        from uploaders.youtube_community import YouTubeCommunity

        yt_comm = YouTubeCommunity(headless=True)
        comm_text = f"🎥 NEW DOCUMENTARY: {title}\n\n👇 Watch the full video here:\nhttps://www.youtube.com/@TheU-AI/videos\n\n{description[:100]}...\n\n#AI #Future"

        await yt_comm.start()
        await yt_comm.post_community_update(comm_text)
        await yt_comm.close()
        print("✅ YouTube Community Post Published")
    except Exception as e:
        print(f"⚠️ Community Post failed: {e}")


async def ship_production(
    video_path: str,
    data_path: str,
    skip_youtube=False,
    skip_instagram=False,
    skip_threads=False,
    skip_community=False,
):
    print(f"📦 Starting shipping for {video_path}")

    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return

    with open(data_path) as f:
        data = json.load(f)

    title = data.get("title", "AI Documentary 2026")
    description = data.get("description", "A deep dive into the future of AI.")
    tags = data.get("youtube_tags", ["AI", "Technology"])

    # Add chapters to description for YouTube
    chapters = ""
    chapters_path = (
        Path(video_path).parent
        / f"{Path(video_path).stem.replace('_final', '_chapters')}.txt"
    )
    if chapters_path.exists():
        with open(chapters_path) as f:
            chapters = "\n\nChapters:\n" + f.read()

    full_description = description + chapters

    # Execute all tasks in parallel
    await asyncio.gather(
        task_youtube(video_path, title, full_description, tags, skip_youtube),
        task_instagram(video_path, title, description, skip_instagram),
        task_threads(video_path, title, description, skip_threads),
        task_community(video_path, title, description, skip_community),
    )

    print("✅ Shipping complete!")


if __name__ == "__main__":
    # Parse args for selective shipping
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("video_path")
    parser.add_argument("data_path")
    parser.add_argument("--skip-youtube", action="store_true")
    parser.add_argument("--skip-instagram", action="store_true")
    parser.add_argument("--skip-threads", action="store_true")
    parser.add_argument("--skip-community", action="store_true")
    args = parser.parse_args()

    # Apply Pydantic Fix for Instagrapi (Already patched on disk, but safe to keep)
    try:
        pass
    except Exception:
        pass

    asyncio.run(
        ship_production(
            args.video_path,
            args.data_path,
            skip_youtube=args.skip_youtube,
            skip_instagram=args.skip_instagram,
            skip_threads=args.skip_threads,
            skip_community=args.skip_community,
        )
    )
