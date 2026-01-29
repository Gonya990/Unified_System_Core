#!/usr/bin/env python3
"""
Telegram Channel Analysis Script
Fetches and analyzes all messages from a channel starting from a specific post.

Requirements:
    pip install telethon python-dotenv

Setup:
    1. Get API_ID and API_HASH from https://my.telegram.org/apps
    2. Add to .env file:
       TELEGRAM_API_ID=your_api_id
       TELEGRAM_API_HASH=your_api_hash
"""

import asyncio
import json
import sys
from datetime import datetime

try:
    from telethon import TelegramClient
    from telethon.errors import FloodWaitError
    from telethon.tl.functions.messages import GetHistoryRequest
except ImportError:
    print("❌ Error: telethon not installed")
    print("   Run: pip install telethon")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  Warning: python-dotenv not installed (optional)")
    print("   Run: pip install python-dotenv")

import os

# Configuration
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
SESSION_NAME = 'telegram_channel_analyzer'
CHANNEL_USERNAME = os.getenv('TELEGRAM_CHANNEL', 'vitalycontentcreate')
START_MESSAGE_ID = int(os.getenv('START_MESSAGE_ID', '1'))

async def fetch_channel_messages(client, channel, start_id=0, limit=None):
    """Fetch all messages from a channel starting from start_id"""
    messages = []
    offset_id = 0
    total_count = 0

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=100,
            max_id=0,
            min_id=start_id,
            hash=0
        ))

        if not history.messages:
            break

        for msg in history.messages:
            if msg.id >= start_id:
                messages.append({
                    'id': msg.id,
                    'date': msg.date.isoformat() if msg.date else None,
                    'text': msg.message,
                    'views': msg.views,
                    'forwards': msg.forwards,
                    'replies': msg.replies.replies if msg.replies else 0,
                    'media': str(type(msg.media).__name__) if msg.media else None,
                    'entities': [type(e).__name__ for e in msg.entities] if msg.entities else []
                })
                total_count += 1

                if limit and total_count >= limit:
                    return messages

        offset_id = history.messages[-1].id
        await asyncio.sleep(1)  # Rate limiting

    return messages

async def analyze_channel():
    """Main analysis function"""
    print(f"🔍 Starting Telegram channel analysis: @{CHANNEL_USERNAME}")
    print(f"📍 Starting from message ID: {START_MESSAGE_ID}")

    # Initialize client
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    try:
        await client.start()
        print("✅ Connected to Telegram")

        # Get channel entity
        channel = await client.get_entity(CHANNEL_USERNAME)
        print(f"📢 Channel: {channel.title}")
        print(f"👥 Subscribers: {channel.participants_count if hasattr(channel, 'participants_count') else 'N/A'}")

        # Fetch messages
        print("\n📥 Fetching messages...")
        messages = await fetch_channel_messages(client, channel, START_MESSAGE_ID)

        print(f"✅ Fetched {len(messages)} messages")

        # Save raw data
        output_file = f'/Users/macbook/Documents/Unified_System/Reports/{CHANNEL_USERNAME}_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'channel': CHANNEL_USERNAME,
                'analysis_date': datetime.now().isoformat(),
                'start_message_id': START_MESSAGE_ID,
                'total_messages': len(messages),
                'messages': messages
            }, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Saved to: {output_file}")

        # Quick analysis
        print("\n📊 Quick Analysis:")
        print(f"   Total messages: {len(messages)}")
        print(f"   Date range: {messages[0]['date']} to {messages[-1]['date']}")

        total_views = sum(m['views'] or 0 for m in messages)
        total_forwards = sum(m['forwards'] or 0 for m in messages)
        avg_views = total_views / len(messages) if messages else 0

        print(f"   Total views: {total_views:,}")
        print(f"   Avg views per post: {avg_views:.0f}")
        print(f"   Total forwards: {total_forwards}")

        media_types = {}
        for m in messages:
            if m['media']:
                media_types[m['media']] = media_types.get(m['media'], 0) + 1

        if media_types:
            print("\n   Media distribution:")
            for media, count in media_types.items():
                print(f"      {media}: {count}")

        return output_file

    finally:
        await client.disconnect()
        print("\n✅ Disconnected")

if __name__ == '__main__':
    if not API_ID or not API_HASH:
        print("❌ Error: TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables required")
        print("   Get them from https://my.telegram.org/apps")
        exit(1)

    output = asyncio.run(analyze_channel())
    print(f"\n🎉 Analysis complete! Check: {output}")
