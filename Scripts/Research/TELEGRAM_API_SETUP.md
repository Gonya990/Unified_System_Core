# Telegram API Setup Guide

## Quick Start

### 1. Get API Credentials

1. Go to https://my.telegram.org/apps
2. Log in with your phone number
3. Click "API development tools"
4. Fill in the form:
   - App title: `Unified System Channel Analyzer`
   - Short name: `unified-analyzer`
   - Platform: `Desktop`
5. Click "Create application"
6. Copy `api_id` and `api_hash`

### 2. Add to .env

Add these lines to `/Users/macbook/Documents/Unified_System/.env`:

```bash
# Telegram API (for channel analysis)
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_CHANNEL=vitalycontentcreate
START_MESSAGE_ID=1
```

### 3. Install Dependencies

```bash
cd /Users/macbook/Documents/Unified_System
pip install telethon python-dotenv
```

### 4. Run Analysis

```bash
cd /Users/macbook/Documents/Unified_System/Scripts/Research
python analyze_telegram_channel.py
```

## First Run

On first run, the script will ask for your phone number for authorization.
This is a one-time setup - session will be saved.

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_API_ID` | API ID from my.telegram.org | `12345678` |
| `TELEGRAM_API_HASH` | API Hash from my.telegram.org | `abcd1234...` |
| `TELEGRAM_CHANNEL` | Channel username (without @) | `vitalycontentcreate` |
| `START_MESSAGE_ID` | Starting message ID | `1` or `88` |

## Output

Analysis results are saved to:
```
/Users/macbook/Documents/Unified_System/Reports/{channel}_analysis_{timestamp}.json
```

## Troubleshooting

### "FloodWaitError"
- You're being rate-limited by Telegram
- Wait the specified time before retrying

### "PhoneNumberInvalidError"
- Check your phone number format: +1234567890

### "SessionPasswordNeededError"
- Your account has 2FA enabled
- Enter your 2FA password when prompted

## Security Notes

- **NEVER commit .env file to git** (already in .gitignore)
- API credentials are personal - don't share
- Session files are stored locally - keep them secure