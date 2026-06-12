#!/usr/bin/env python3
"""
YouTube Daily Analytics Report — UnifiedCore Content Factory
Sends daily report with channel performance metrics to Unified App.
Runs at 22:00 ISR every day via factory_scheduler.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Setup paths
UPLOADERS_DIR = Path(__file__).parent.resolve()
SRC_DIR = UPLOADERS_DIR.parent
FACTORY_DIR = SRC_DIR.parent
ROOT_DIR = FACTORY_DIR.parent.parent

load_dotenv(FACTORY_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=False)


CREDENTIALS_DIR = UPLOADERS_DIR / ".credentials"


def send_app_notification(message: str, parse_mode: str = "HTML") -> bool:
    """Send message to Unified App."""
    try:
        print(f"\n[UNIFIED APP NOTIFICATION]\n{message}\n")
        return True
    except Exception as e:
        print(f"⚠️ App notification error: {e}")
        return False


def get_youtube_service(token_file: str = None):
    """Get authenticated YouTube service."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        token_path = Path(token_file) if token_file else CREDENTIALS_DIR / "youtube_token_megaforma_full.json"

        if not token_path.exists():
            # Try fallback tokens
            for fname in ["youtube_token_megaforma.json", "youtube_token.json"]:
                fp = CREDENTIALS_DIR / fname
                if fp.exists():
                    token_path = fp
                    break

        if not token_path.exists():
            print(f"❌ No YouTube token found in {CREDENTIALS_DIR}")
            return None

        scopes = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/yt-analytics.readonly",
        ]
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save refreshed token
            with open(token_path, "w") as f:
                f.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ YouTube auth error: {e}")
        return None


def get_channel_stats(youtube) -> Optional[dict]:
    """Get overall channel statistics."""
    try:
        response = youtube.channels().list(
            part="statistics,snippet",
            mine=True
        ).execute()

        if not response.get("items"):
            return None

        ch = response["items"][0]
        stats = ch.get("statistics", {})
        snippet = ch.get("snippet", {})

        return {
            "name": snippet.get("title", "Unknown"),
            "subscribers": int(stats.get("subscriberCount", 0)),
            "total_views": int(stats.get("viewCount", 0)),
            "total_videos": int(stats.get("videoCount", 0)),
        }
    except Exception as e:
        print(f"❌ Channel stats error: {e}")
        return None


def get_recent_videos(youtube, max_results: int = 10) -> list:
    """Get recent videos with their stats."""
    try:
        # Get recent uploads
        channels_response = youtube.channels().list(
            part="contentDetails", mine=True
        ).execute()

        if not channels_response.get("items"):
            return []

        uploads_playlist = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Get recent videos from uploads playlist
        playlist_response = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist,
            maxResults=max_results
        ).execute()

        video_ids = [
            item["snippet"]["resourceId"]["videoId"]
            for item in playlist_response.get("items", [])
        ]

        if not video_ids:
            return []

        # Get video statistics
        videos_response = youtube.videos().list(
            part="statistics,snippet,contentDetails",
            id=",".join(video_ids)
        ).execute()

        videos = []
        for item in videos_response.get("items", []):
            stats = item.get("statistics", {})
            snippet = item.get("snippet", {})
            duration = item.get("contentDetails", {}).get("duration", "")

            # Determine if it's a Short
            is_short = "PT" in duration and "M" not in duration or (
                "M" in duration and int(duration.replace("PT", "").replace("M", "").split("S")[0] if "M" in duration else "0") <= 1
            )

            videos.append({
                "id": item["id"],
                "title": snippet.get("title", "")[:60],
                "published": snippet.get("publishedAt", "")[:10],
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0)),
                "is_short": is_short,
            })

        return sorted(videos, key=lambda x: x["views"], reverse=True)
    except Exception as e:
        print(f"❌ Recent videos error: {e}")
        return []


def generate_daily_report() -> str:
    """Generate and send daily analytics report to Unified App."""
    print("📊 Generating YouTube daily report...")

    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    time_str = now.strftime("%H:%M")

    youtube = get_youtube_service()

    if not youtube:
        # Send error notification
        msg = (
            f"⚠️ <b>YouTube Report {date_str}</b>\n\n"
            f"❌ Не удалось подключиться к YouTube API\n"
            f"🔧 Требуется переавторизация OAuth\n\n"
            f"<i>Запусти: python3 setup_youtube_oauth.py</i>"
        )
        send_app_notification(msg)
        return msg

    # Get channel stats
    channel = get_channel_stats(youtube)
    videos = get_recent_videos(youtube, max_results=10)

    if not channel:
        msg = f"⚠️ <b>YouTube Report {date_str}</b>\n❌ Не удалось получить статистику канала"
        send_app_notification(msg)
        return msg

    # Build report
    shorts = [v for v in videos if v["is_short"]]
    longform = [v for v in videos if not v["is_short"]]

    # Top 3 performers
    top_3 = videos[:3]

    # Calculate today's videos (published today)
    today_videos = [v for v in videos if v["published"] == now.strftime("%Y-%m-%d")]

    report_lines = [
        f"📺 <b>YouTube Daily Report</b>",
        f"📅 {date_str} | {time_str} ISR",
        f"━━━━━━━━━━━━━━━━━━━━",
        f"",
        f"📊 <b>Канал: {channel['name']}</b>",
        f"👥 Подписчики: <b>{channel['subscribers']:,}</b>",
        f"👁️ Всего просмотров: <b>{channel['total_views']:,}</b>",
        f"🎬 Всего видео: <b>{channel['total_videos']}</b>",
        f"",
    ]

    if today_videos:
        report_lines.append(f"✅ <b>Опубликовано сегодня: {len(today_videos)}</b>")
        for v in today_videos:
            emoji = "📱" if v["is_short"] else "🎬"
            report_lines.append(f"  {emoji} {v['title']}")
        report_lines.append("")
    else:
        report_lines.append("⚠️ <b>Сегодня видео не публиковались</b>")
        report_lines.append("")

    if top_3:
        report_lines.append(f"🏆 <b>Топ-3 за последнее время:</b>")
        medals = ["🥇", "🥈", "🥉"]
        for i, v in enumerate(top_3):
            emoji = "📱" if v["is_short"] else "🎬"
            report_lines.append(
                f"{medals[i]} {emoji} {v['title'][:40]}...\n"
                f"   👁️ {v['views']:,}  ❤️ {v['likes']:,}  💬 {v['comments']:,}"
            )
        report_lines.append("")

    # Content mix stats
    report_lines.extend([
        f"📈 <b>Статистика контента (последние 10):</b>",
        f"  📱 Shorts: {len(shorts)} видео",
        f"  🎬 Long-form: {len(longform)} видео",
        f"",
        f"━━━━━━━━━━━━━━━━━━━━",
        f"🤖 <i>Megaforma Content Factory</i>",
    ])

    message = "\n".join(report_lines)

    # Send to Unified App
    if send_app_notification(message):
        print(f"✅ Report sent to Unified App!")
    else:
        print("⚠️ App notification failed, but report generated")

    return message


def send_upload_notification(
    video_title: str,
    video_url: str,
    platform: str = "YouTube",
    stats: dict = None,
) -> bool:
    """Send notification when a video is uploaded."""
    emoji_map = {"YouTube": "📺", "YouTube Shorts": "📱", "Instagram": "📸", "UnifiedApp": "📱"}
    emoji = emoji_map.get(platform, "📤")

    msg_lines = [
        f"{emoji} <b>Новое видео опубликовано!</b>",
        f"",
        f"📌 <b>{video_title}</b>",
        f"🔗 {video_url}",
        f"🕐 {datetime.now().strftime('%H:%M ISR')}",
    ]

    if stats:
        msg_lines.extend([
            f"",
            f"📊 <i>Начальные метрики через час</i>",
        ])

    return send_app_notification("\n".join(msg_lines))


# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Analytics Reporter")
    parser.add_argument("--report", action="store_true", help="Generate and send daily report")
    parser.add_argument("--test", action="store_true", help="Test Unified App notification")
    args = parser.parse_args()

    if args.test:
        ok = send_app_notification("🧪 <b>Test message</b>\nUnifiedCore YouTube Reporter is running!")
        print("✅ App Notification OK" if ok else "❌ App Notification FAILED")
    elif args.report:
        generate_daily_report()
    else:
        generate_daily_report()
