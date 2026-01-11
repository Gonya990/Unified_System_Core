# Research Scripts

## Telegram Channel Analyzer

Automated analysis tool for Telegram channels using Telethon API.

### Setup

See [TELEGRAM_API_SETUP.md](TELEGRAM_API_SETUP.md) for detailed instructions.

**Quick Start:**

1. Get API credentials from https://my.telegram.org/apps
2. Add to `/Users/macbook/Documents/Unified_System/.env`:
   ```bash
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_CHANNEL=vitalycontentcreate
   START_MESSAGE_ID=1
   ```
3. Run analysis:
   ```bash
   cd /Users/macbook/Documents/Unified_System/Scripts/Research
   python3 analyze_telegram_channel.py
   ```

### Output

Analysis results are saved to:
```
/Users/macbook/Documents/Unified_System/Reports/{channel}_analysis_{timestamp}.json
```

**JSON Structure:**
```json
{
  "channel": "vitalycontentcreate",
  "analysis_date": "2026-01-11T...",
  "start_message_id": 1,
  "total_messages": 116,
  "messages": [
    {
      "id": 88,
      "date": "2026-01-10T14:23:00",
      "text": "Post content...",
      "views": 1520,
      "forwards": 3,
      "replies": 5,
      "media": "MessageMediaPhoto",
      "entities": ["MessageEntityUrl"]
    }
  ]
}
```

### Integration with Content Factory

The analyzer integrates with the Content Factory pipeline in `Scripts/Production_Factory/`:

1. **Research Phase:** Channel analysis identifies trending content patterns
2. **Adaptation Phase:** Foreign content → Russian market translation
3. **Production Phase:** AI-generated video assembly (VEO, FLOW, Nanobanana)
4. **Distribution Phase:** Multi-channel YouTube publishing

See [generic-crafting-leaf.md](../../.claude/plans/generic-crafting-leaf.md) for comprehensive channel research methodology.

### Usage Examples

**Analyze specific channel:**
```bash
TELEGRAM_CHANNEL=channelname python3 analyze_telegram_channel.py
```

**Start from specific message:**
```bash
START_MESSAGE_ID=88 python3 analyze_telegram_channel.py
```

**Analyze with custom config:**
```bash
export TELEGRAM_API_ID=12345678
export TELEGRAM_API_HASH=abcd1234...
export TELEGRAM_CHANNEL=vitalycontentcreate
export START_MESSAGE_ID=1
python3 analyze_telegram_channel.py
```

### Troubleshooting

**FloodWaitError:**
- Telegram rate limiting active
- Wait the specified time before retrying
- Script has built-in 1-second delay between requests

**PhoneNumberInvalidError:**
- Check phone number format: +1234567890
- Include country code

**SessionPasswordNeededError:**
- Account has 2FA enabled
- Enter 2FA password when prompted

**API Key Issues:**
- Verify credentials at https://my.telegram.org/apps
- Check `.env` file syntax
- Ensure no extra spaces in credentials

### Security Notes

- `.env` file is in `.gitignore` (never commit)
- API credentials are personal (don't share)
- Session files (`telegram_channel_analyzer.session`) stored locally
- Keep session files secure (equivalent to logged-in access)

### Dependencies

```bash
pip install telethon python-dotenv
```

Or using the system Python:
```bash
python3 -m pip install --user telethon python-dotenv
```