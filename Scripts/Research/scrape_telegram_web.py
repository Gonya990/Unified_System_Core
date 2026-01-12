#!/usr/bin/env python3
"""
Telegram Channel Web Scraper
Fetches public channel data without requiring API credentials.
Uses the public Telegram web interface.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Error: required libraries not installed")
    print("   Run: pip install requests beautifulsoup4")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration
CHANNEL_USERNAME = os.getenv('TELEGRAM_CHANNEL', 'vitalycontentcreate')
START_MESSAGE_ID = int(os.getenv('START_MESSAGE_ID', '1'))
REPORTS_DIR = Path('/Users/macbook/Documents/Unified_System/Reports')

def fetch_channel_page(channel, before=None):
    """Fetch channel page from Telegram web"""
    url = f'https://t.me/s/{channel}'
    if before:
        url += f'?before={before}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_message(msg_div):
    """Parse a single message div"""
    try:
        # Message ID
        msg_id_str = msg_div.get('data-post', '')
        if '/' in msg_id_str:
            msg_id = int(msg_id_str.split('/')[-1])
        else:
            return None

        # Date
        time_elem = msg_div.find('time')
        date = time_elem.get('datetime') if time_elem else None

        # Text
        text_div = msg_div.find('div', class_='tgme_widget_message_text')
        text = text_div.get_text(strip=True) if text_div else ''

        # Views
        views_elem = msg_div.find('span', class_='tgme_widget_message_views')
        views_text = views_elem.get_text(strip=True) if views_elem else '0'
        # Convert "1.5K" to 1500
        if 'K' in views_text:
            views = int(float(views_text.replace('K', '')) * 1000)
        elif 'M' in views_text:
            views = int(float(views_text.replace('M', '')) * 1000000)
        else:
            views = int(views_text) if views_text.isdigit() else 0

        # Media
        media = None
        if msg_div.find('a', class_='tgme_widget_message_photo_wrap'):
            media = 'photo'
        elif msg_div.find('video', class_='tgme_widget_message_video'):
            media = 'video'
        elif msg_div.find('div', class_='tgme_widget_message_document'):
            media = 'document'

        return {
            'id': msg_id,
            'date': date,
            'text': text,
            'views': views,
            'media': media
        }
    except Exception as e:
        print(f"⚠️  Error parsing message: {e}")
        return None

def scrape_channel(channel, start_id=1):
    """Scrape all messages from channel"""
    print(f"🔍 Scraping Telegram channel: @{channel}")
    print(f"📍 Starting from message ID: {start_id}")

    messages = []
    before = None
    page_count = 0

    while True:
        page_count += 1
        print(f"📄 Fetching page {page_count}... ", end='', flush=True)

        try:
            html = fetch_channel_page(channel, before)
            soup = BeautifulSoup(html, 'html.parser')

            # Find all message divs
            msg_divs = soup.find_all('div', class_='tgme_widget_message')

            if not msg_divs:
                print("(no more messages)")
                break

            print(f"found {len(msg_divs)} messages")

            page_messages = []
            for msg_div in msg_divs:
                parsed = parse_message(msg_div)
                if parsed and parsed['id'] >= start_id:
                    page_messages.append(parsed)

            if not page_messages:
                break

            # Add to collection
            messages.extend(page_messages)

            # Get oldest message ID for next page
            oldest_id = min(m['id'] for m in page_messages)

            # Stop if we've reached the start
            if oldest_id <= start_id:
                break

            before = oldest_id

        except Exception as e:
            print(f"\n❌ Error: {e}")
            break

    # Sort by ID
    messages.sort(key=lambda m: m['id'])

    return messages

def analyze_messages(messages):
    """Perform quick analysis"""
    if not messages:
        return {}

    total_views = sum(m['views'] for m in messages)
    avg_views = total_views / len(messages)

    media_count = {}
    for m in messages:
        if m['media']:
            media_count[m['media']] = media_count.get(m['media'], 0) + 1

    return {
        'total_messages': len(messages),
        'date_range': {
            'first': messages[0]['date'],
            'last': messages[-1]['date']
        },
        'total_views': total_views,
        'avg_views': round(avg_views, 1),
        'media_distribution': media_count
    }

def main():
    """Main execution"""
    messages = scrape_channel(CHANNEL_USERNAME, START_MESSAGE_ID)

    if not messages:
        print("❌ No messages found")
        return

    print(f"\n✅ Scraped {len(messages)} messages")

    # Analysis
    analysis = analyze_messages(messages)

    # Save to file
    REPORTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = REPORTS_DIR / f'{CHANNEL_USERNAME}_webscrape_{timestamp}.json'

    output_data = {
        'channel': CHANNEL_USERNAME,
        'scrape_date': datetime.now().isoformat(),
        'start_message_id': START_MESSAGE_ID,
        'analysis': analysis,
        'messages': messages
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Saved to: {output_file}")

    # Print analysis
    print("\n📊 Quick Analysis:")
    print(f"   Total messages: {analysis['total_messages']}")
    print(f"   Date range: {analysis['date_range']['first']} to {analysis['date_range']['last']}")
    print(f"   Total views: {analysis['total_views']:,}")
    print(f"   Avg views per post: {analysis['avg_views']:.0f}")

    if analysis['media_distribution']:
        print("\n   Media distribution:")
        for media, count in analysis['media_distribution'].items():
            print(f"      {media}: {count}")

if __name__ == '__main__':
    main()
