#!/usr/bin/env python3
"""
Telegram Channel Monitoring → Agent Mail Integration
Monitors Telegram channel for new posts and broadcasts to agents via Agent Mail.
"""

import json
from datetime import datetime
from pathlib import Path

from agent_mail_client import AgentMailClient

# Paths
REPORTS_DIR = Path('/Users/macbook/Documents/Unified_System/Reports')
STATE_FILE = REPORTS_DIR / '.telegram_monitor_state.json'

def load_state():
    """Load last scan state"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {'last_scan': None, 'last_message_id': 0}

def save_state(state):
    """Save scan state"""
    STATE_FILE.write_text(json.dumps(state, indent=2))

def get_latest_report():
    """Get most recent Telegram scrape report"""
    reports = sorted(REPORTS_DIR.glob('vitalycontentcreate_webscrape_*.json'))
    if not reports:
        return None
    return reports[-1]

def analyze_new_posts(report_file, last_message_id):
    """Analyze new posts since last scan"""
    data = json.loads(report_file.read_text())
    messages = data['messages']

    # Filter new messages
    new_messages = [m for m in messages if m['id'] > last_message_id]

    if not new_messages:
        return None

    # Sort by views to find trending
    top_posts = sorted(new_messages, key=lambda m: m['views'], reverse=True)[:3]

    return {
        'total_new': len(new_messages),
        'date_range': {
            'first': new_messages[0]['date'],
            'last': new_messages[-1]['date']
        },
        'avg_views': sum(m['views'] for m in new_messages) / len(new_messages),
        'top_posts': top_posts,
        'latest_id': max(m['id'] for m in messages)
    }

def format_report(analysis):
    """Format analysis as markdown"""
    md = f"""# 🔔 Telegram Channel Update Alert

**Channel**: @vitalycontentcreate
**Time**: {datetime.now().isoformat()}

## Summary
- **{analysis['total_new']} new posts** detected
- **Avg views**: {analysis['avg_views']:.0f}
- **Date range**: {analysis['date_range']['first']} to {analysis['date_range']['last']}

## Top 3 Trending Posts

"""

    for i, post in enumerate(analysis['top_posts'], 1):
        text_preview = post['text'][:100] + '...' if len(post['text']) > 100 else post['text']
        media_icon = {'photo': '🖼️', 'video': '🎬', 'document': '📄'}.get(post['media'], '📝')

        md += f"""### {i}. {media_icon} Post #{post['id']} - {post['views']:,} views
{text_preview}

"""

    md += """## Action Items
1. Analyze engagement patterns
2. Identify replicable content strategies
3. Update Content Factory pipeline

**Monitor Status**: Active | **Next Scan**: Scheduled
"""

    return md

def main():
    """Main monitoring loop"""
    print('🔍 Telegram Channel Monitor → Agent Mail Integration')
    print('=' * 60)

    # Load state
    state = load_state()
    print(f"📊 Last scan: {state['last_scan'] or 'Never'}")
    print(f"📍 Last message ID: {state['last_message_id']}")

    # Get latest report
    report_file = get_latest_report()
    if not report_file:
        print('❌ No reports found. Run telegram scraper first.')
        return

    print(f"📄 Latest report: {report_file.name}")

    # Analyze new posts
    analysis = analyze_new_posts(report_file, state['last_message_id'])

    if not analysis:
        print('✅ No new posts detected')
        return

    print(f"\n🆕 {analysis['total_new']} new posts found!")

    # Send to Agent Mail
    client = AgentMailClient()

    if not client.health_check():
        print('❌ Agent Mail server unavailable')
        return

    print('📡 Sending to Agent Mail...')

    report_md = format_report(analysis)

    result = client.broadcast(
        subject=f"🔔 Telegram Update: {analysis['total_new']} new posts from @vitalycontentcreate",
        body_md=report_md,
        importance='normal'
    )

    print(f"✅ Broadcast sent to {result['count']} agents")

    # Update state
    state['last_scan'] = datetime.now().isoformat()
    state['last_message_id'] = analysis['latest_id']
    save_state(state)

    print(f"💾 State updated: last_message_id={analysis['latest_id']}")

if __name__ == '__main__':
    main()
