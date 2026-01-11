#!/usr/bin/env python3
"""
YouTube Shorts Analytics Module
Обновлено с учётом изменений метрик YouTube (с 31.03.2025)

Новые метрики:
- Views: Количество начал воспроизведения (без минимального времени)
- Engaged Views: Просмотры с продолжением (старая метрика "views")

Для монетизации и YPP используются Engaged Views.
"""

import os
from pathlib import Path
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes for YouTube Analytics
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/yt-analytics.readonly'
]

# Paths
current_file = Path(__file__).resolve()
UPLOADERS_DIR = current_file.parent
CREDENTIALS_DIR = UPLOADERS_DIR / ".credentials"
CLIENT_SECRETS_FILE = CREDENTIALS_DIR / "client_secrets.json"
TOKEN_FILE = CREDENTIALS_DIR / "youtube_analytics_token.json"

CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)


def get_analytics_service():
    """Authenticates and returns YouTube Analytics API service."""
    creds = None
    
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"⚠️ Error loading token: {e}")
            creds = None

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
                print(f"❌ Client secrets not found at {CLIENT_SECRETS_FILE}")
                return None, None

            print("🔐 Initiating OAuth 2.0 login flow...")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print(f"✅ Token saved to {TOKEN_FILE}")

    try:
        youtube = build('youtube', 'v3', credentials=creds)
        analytics = build('youtubeAnalytics', 'v2', credentials=creds)
        return youtube, analytics
    except HttpError as e:
        print(f"❌ API error: {e}")
        return None, None


def get_channel_id(youtube):
    """Get the authenticated user's channel ID."""
    try:
        response = youtube.channels().list(part="id", mine=True).execute()
        if response.get("items"):
            return response["items"][0]["id"]
    except HttpError as e:
        print(f"❌ Error getting channel: {e}")
    return None


def get_shorts_analytics(days=30):
    """
    Получить аналитику по Shorts за последние N дней.
    
    Возвращает обе метрики:
    - views: Общие просмотры (новая метрика с 31.03.2025 - любое начало воспроизведения)
    - engaged_views: Просмотры с продолжением (для монетизации)
    
    Примечание: YouTube API пока не разделяет эти метрики напрямую.
    Engaged views = views в API (до обновления).
    После 31.03.2025 новая метрика будет доступна отдельно.
    """
    youtube, analytics = get_analytics_service()
    if not youtube or not analytics:
        return None
    
    channel_id = get_channel_id(youtube)
    if not channel_id:
        return None
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    print(f"\n📊 YouTube Shorts Analytics ({start_date} → {end_date})")
    print("=" * 50)
    
    try:
        # Get overall channel analytics
        response = analytics.reports().query(
            ids=f"channel=={channel_id}",
            startDate=start_date,
            endDate=end_date,
            metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,likes",
            dimensions="day",
            sort="-day"
        ).execute()
        
        # Calculate totals
        totals = {
            'views': 0,
            'watch_time_minutes': 0,
            'avg_view_duration': 0,
            'subscribers_gained': 0,
            'likes': 0
        }
        
        rows = response.get('rows', [])
        for row in rows:
            totals['views'] += row[1]
            totals['watch_time_minutes'] += row[2]
            totals['subscribers_gained'] += row[4]
            totals['likes'] += row[5]
        
        if rows:
            totals['avg_view_duration'] = rows[0][3]  # Latest day's avg
        
        # Calculate engaged view estimate
        # После марта 2025 engaged_views будет отдельной метрикой
        # Пока используем формулу: engaged = views * (avg_duration / shorts_length)
        # Для Shorts (60 сек макс), если avg > 3 сек, считаем engaged
        SHORTS_ENGAGED_THRESHOLD = 3  # seconds
        engaged_rate = min(1.0, totals['avg_view_duration'] / SHORTS_ENGAGED_THRESHOLD) if totals['avg_view_duration'] > 0 else 0.5
        estimated_engaged_views = int(totals['views'] * engaged_rate)
        
        print(f"\n📈 МЕТРИКИ ЗА {days} ДНЕЙ:")
        print("-" * 50)
        print(f"  👁️  Просмотры (Views):           {totals['views']:,}")
        print(f"  ✅ Engaged Views (оценка):       {estimated_engaged_views:,}")
        print(f"  ⏱️  Время просмотра:             {totals['watch_time_minutes']:,.0f} мин")
        print(f"  📏 Средняя длит. просмотра:     {totals['avg_view_duration']:.1f} сек")
        print(f"  👥 Новых подписчиков:           +{totals['subscribers_gained']:,}")
        print(f"  ❤️  Лайков:                      {totals['likes']:,}")
        print("-" * 50)
        
        # Monetization note
        print("\n💰 МОНЕТИЗАЦИЯ (после 31.03.2025):")
        print("   • YPP и доход рассчитываются по Engaged Views")
        print("   • Новые Views показывают реальный охват")
        print("   • Engaged Views = качество контента")
        
        return {
            'period_days': days,
            'views': totals['views'],
            'engaged_views_estimate': estimated_engaged_views,
            'watch_time_minutes': totals['watch_time_minutes'],
            'avg_view_duration_seconds': totals['avg_view_duration'],
            'subscribers_gained': totals['subscribers_gained'],
            'likes': totals['likes'],
            'engagement_rate': engaged_rate
        }
        
    except HttpError as e:
        print(f"❌ Analytics API error: {e}")
        return None


def get_video_performance(video_id):
    """
    Получить детальную статистику конкретного видео.
    
    Для Shorts после 31.03.2025:
    - views = все начала воспроизведения
    - engaged_views = продолженные просмотры (для монетизации)
    """
    youtube, analytics = get_analytics_service()
    if not youtube or not analytics:
        return None
    
    channel_id = get_channel_id(youtube)
    if not channel_id:
        return None
    
    try:
        # Get video info
        video_response = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        ).execute()
        
        if not video_response.get('items'):
            print(f"❌ Video {video_id} not found")
            return None
        
        video = video_response['items'][0]
        stats = video.get('statistics', {})
        snippet = video.get('snippet', {})
        
        # Check if it's a Short (duration <= 60s)
        duration = video.get('contentDetails', {}).get('duration', '')
        is_short = 'PT' in duration and ('S' in duration or duration.count('M') == 0 or 
                                          (duration.count('M') == 1 and int(duration.split('M')[0].replace('PT', '')) <= 1))
        
        print(f"\n📹 VIDEO: {snippet.get('title', 'Unknown')[:50]}...")
        print(f"   ID: {video_id}")
        print(f"   Type: {'📱 Short' if is_short else '🎬 Video'}")
        print("-" * 50)
        print(f"   👁️  Views:              {int(stats.get('viewCount', 0)):,}")
        print(f"   ❤️  Likes:              {int(stats.get('likeCount', 0)):,}")
        print(f"   💬 Comments:           {int(stats.get('commentCount', 0)):,}")
        
        if is_short:
            print("\n   📊 Shorts Metrics (после 31.03.2025):")
            print("      • Views = начала воспроизведения")
            print("      • Engaged Views = для монетизации (см. Analytics)")
        
        return {
            'video_id': video_id,
            'title': snippet.get('title'),
            'is_short': is_short,
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'comments': int(stats.get('commentCount', 0))
        }
        
    except HttpError as e:
        print(f"❌ API error: {e}")
        return None


def print_metrics_explanation():
    """Вывести объяснение новых метрик YouTube Shorts."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║           📊 YOUTUBE SHORTS METRICS (с 31.03.2025)               ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  👁️  VIEWS (Новая метрика)                                      ║
║      • Считается при ЛЮБОМ начале воспроизведения                ║
║      • Без минимального времени просмотра                        ║
║      • Показывает реальный охват контента                        ║
║      • Полезно для сравнения между платформами                   ║
║                                                                  ║
║  ✅ ENGAGED VIEWS (Старая метрика "views")                       ║
║      • Считается когда зритель ПРОДОЛЖАЕТ смотреть               ║
║      • Используется для YPP и монетизации                        ║
║      • Доступна в YouTube Analytics                              ║
║      • Ваш заработок НЕ изменится                                ║
║                                                                  ║
║  💡 КАК ИСПОЛЬЗОВАТЬ:                                            ║
║      • Views → оценка охвата, вирусности                         ║
║      • Engaged Views → качество контента, монетизация            ║
║      • Соотношение Engaged/Views → удержание аудитории           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='YouTube Shorts Analytics')
    parser.add_argument('--days', type=int, default=30, help='Period in days')
    parser.add_argument('--video', type=str, help='Video ID for detailed stats')
    parser.add_argument('--explain', action='store_true', help='Explain new metrics')
    
    args = parser.parse_args()
    
    if args.explain:
        print_metrics_explanation()
    elif args.video:
        get_video_performance(args.video)
    else:
        get_shorts_analytics(args.days)
