# Gmail Automation Agent Setup Guide

## Руководство по настройке агента автоматизации Gmail

## Overview | Обзор

**English:** Automated email processing agent for <gonya90.gg@gmail.com> with intelligent categorization, monitoring, and ChatGPT integration.

**Russian:** Автоматический агент обработки почты для <gonya90.gg@gmail.com> с интеллектуальной категоризацией, мониторингом и интеграцией с ChatGPT.

---

## Features | Возможности

### ✅ Email Monitoring

- Automatic email fetching every hour
- Last 24 hours monitoring
- Smart categorization (Urgent/Work/GitHub/LinkedIn/Spam)
- Multi-language support (EN/RU/HE)

### ✅ Intelligent Categorization

**Categories:**

- 🔴 **Urgent** - Requires immediate attention
- 💼 **Work** - Job offers, interviews, professional
- 🐙 **GitHub** - Repository activity, PRs, commits
- 💼 **LinkedIn** - Connections, messages, invitations
- ⚪ **Spam** - Promotional, unwanted
- 📧 **Info** - General information

### ✅ Automation

- Auto-categorization using keywords
- Email database with history
- Daily summaries
- Integration with ChatGPT workflows

---

## Setup Instructions | Инструкции по настройке

### Step 1: Install Dependencies

```bash
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 2: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Gmail API:
   - Go to **APIs & Services** → **Library**
   - Search for "Gmail API"
   - Click **Enable**

### Step 3: Create OAuth2 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: **Unified System Gmail Agent**
   - User support email: **<gonya90.gg@gmail.com>**
   - Developer contact: **<gonya90.gg@gmail.com>**
   - Scopes: Add Gmail API scopes
   - Test users: Add **<gonya90.gg@gmail.com>**
4. Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: **Gmail Automation Agent**
5. Download JSON file
   > [!IMPORTANT]
   > **Client Secret Visibility:** Google now hides the Client Secret after creation. You must download the JSON file **immediately** upon creation. If you lose it, you must "Reset Secret" in the Cloud Console to generate a new one.

### Step 4: Install Credentials

```bash
# Create credentials directory
mkdir -p /Users/macbook/Documents/Unified_System/Scripts/automation/.credentials

# Copy downloaded JSON file
cp ~/Downloads/client_secret_*.json \
   /Users/macbook/Documents/Unified_System/Scripts/automation/.credentials/gmail_credentials.json
```

### Step 5: First Run (Authentication)

```bash
cd /Users/macbook/Documents/Unified_System/Scripts/automation
python3 gmail_agent.py
```

**What happens:**

1. Browser opens automatically
2. Sign in with **<gonya90.gg@gmail.com>**
3. Grant permissions to the app
4. Token saved for future use

---

## Usage | Использование

### Manual Run

```bash
cd /Users/macbook/Documents/Unified_System/Scripts/automation
python3 gmail_agent.py
```

### Automated Schedule (Cron)

Add to crontab:

```bash
# Check email every hour
0 * * * * /usr/bin/python3 /Users/macbook/Documents/Unified_System/Scripts/automation/gmail_agent.py >> /Users/macbook/Documents/Unified_System/logs/automation/gmail_agent.log 2>&1
```

---

## Output Example | Пример вывода

```text
╔══════════════════════════════════════════════════════════════╗
║   Gmail Automation Agent - Email Summary                    ║
║   Агент автоматизации Gmail - Сводка писем                  ║
╚══════════════════════════════════════════════════════════════╝

📊 Email Statistics | Статистика писем:

  📧 info: 15
  🐙 github: 8
  💼 work: 3
  💼 linkedin: 2
  🔴 urgent: 1
  ⚪ spam: 5

Total: 34 emails

🔴 URGENT EMAILS:

  From: recruiter@company.com
  Subject: Interview Opportunity - Senior Developer
  Date: Wed, 25 Dec 2024 18:30:00 +0000

💼 WORK-RELATED:

  From: hr@tech-company.com
  Subject: Your Application Status
  
  From: jobs@linkedin.com
  Subject: New Job Matches for You
```

---

## Email Categories | Категории писем

### 🔴 Urgent (Срочно)

**Keywords:**

- English: urgent, asap, important
- Russian: срочно, важно
- Hebrew: דחוף

**Action:** Immediate notification

### 💼 Work (Работа)

**Keywords:**

- interview, job, position, vacancy
- работа, вакансия
- משרה

**Action:** Daily summary, high priority

### 🐙 GitHub

**Keywords:**

- github, pull request, commit, repository

**Action:** Tech activity log

### 💼 LinkedIn

**Keywords:**

- linkedin, connection, invitation, network

**Action:** Professional network tracking

### ⚪ Spam

**Keywords:**

- unsubscribe, lottery, winner, prize, click here

**Action:** Auto-archive

---

## Database | База данных

**Location:** `/Users/macbook/Documents/Unified_System/logs/automation/email_database.json`

**Structure:**

```json
{
  "emails": [
    {
      "id": "18c1234567890",
      "subject": "Subject line",
      "sender": "sender@example.com",
      "date": "Wed, 25 Dec 2024",
      "category": "work",
      "body_preview": "First 200 chars..."
    }
  ],
  "last_check": "2024-12-25T18:30:00"
}
```

---

## ChatGPT Integration | Интеграция с ChatGPT

### Auto-Summary to ChatGPT

The agent can generate email summaries that ChatGPT can read:

```bash
# Generate summary for ChatGPT
python3 gmail_agent.py --export-summary
```

Output saved to: `Agent_Context/Email_Summaries/daily_YYYY-MM-DD.md`

ChatGPT can then:

- Read summaries via GitHub
- Suggest responses
- Track important conversations
- Update your profile based on job offers

---

## Security | Безопасность

### OAuth2 Token

- ✅ Stored locally only
- ✅ Never committed to Git (in `.gitignore`)
- ✅ Auto-refreshed when expired
- ✅ Can be revoked at any time

### Permissions

Requests only necessary scopes:

- `gmail.readonly` - Read emails
- `gmail.send` - Send emails (for auto-replies)
- `gmail.modify` - Label/archive emails

### Revoke Access

1. Go to [Google Account Security](https://myaccount.google.com/permissions)
2. Find "Unified System Gmail Agent"
3. Click **Remove Access**

---

## Troubleshooting | Устранение неполадок

### "Credentials not found"

```bash
# Check if file exists
ls -la /Users/macbook/Documents/Unified_System/Scripts/automation/.credentials/gmail_credentials.json

# If not, re-download from Google Cloud Console
```

### "Deleted Client" or "Client not found" (Error 401)

This means the OAuth2 Client ID you are using has been deleted in the Google Cloud Console.

1. Go to [Google Cloud Console - Credentials](https://console.cloud.google.com/apis/credentials)
2. Check if your "Gmail Automation Agent" client ID exists.
3. If not, create a new one (Desktop app).
4. If it exists but you get this error, check `gmail_credentials.json` to ensure it matches the console.
5. **Fix:** Download the new JSON, replace `gmail_credentials.json`, and delete `gmail_token.pickle` to re-authenticate.

### "Token expired"

```bash
# Delete old token
rm /Users/macbook/Documents/Unified_System/Scripts/automation/.credentials/gmail_token.pickle

# Re-run to re-authenticate
python3 gmail_agent.py
```

### "Gmail API not enabled"

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. **APIs & Services** → **Library**
4. Search "Gmail API" and enable

---

## Advanced Features | Расширенные возможности

### Custom Categories

Edit `gmail_agent.py` to add custom categories:

```python
CATEGORIES = {
    "custom": {
        "keywords": ["keyword1", "keyword2"],
        "icon": "🎯"
    }
}
```

### Auto-Reply

Future feature: Automatic responses to specific email types

### Email Threading

Future feature: Track conversation threads

---

## Logs | Логи

**Location:** `/Users/macbook/Documents/Unified_System/logs/automation/gmail_agent.log`

**View recent activity:**

```bash
tail -f /Users/macbook/Documents/Unified_System/logs/automation/gmail_agent.log
```

---

## Status | Статус

**Current:** ✅ Ready for setup  
**Authentication:** Requires OAuth2 setup  
**Production:** Configure after first successful run  

---

**Email:** <gonya90.gg@gmail.com>  
**Last Updated:** 2025-12-25  
**Maintained by:** Antigravity AI Agent
