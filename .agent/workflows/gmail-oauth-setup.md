---
description: Quick Gmail OAuth2 setup for email automation
---

# Gmail OAuth2 Quick Setup

# Быстрая настройка Gmail OAuth2

**Goal:** Enable Gmail automation for <gonya90.gg@gmail.com> in 5 minutes  
**Цель:** Включить автоматизацию Gmail для <gonya90.gg@gmail.com> за 5 минут

---

## Prerequisites | Предварительные требования

1. Google account: **<gonya90.gg@gmail.com>** ✅
2. Python 3 installed ✅
3. Internet connection ✅

---

## Step 1: Install Python Dependencies

```bash
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

**Expected output:** Successfully installed packages

---

## Step 2: Open Google Cloud Console

**URL:** <https://console.cloud.google.com/>

1. Sign in with **<gonya90.gg@gmail.com>**
2. Create new project OR select existing project
3. Project name suggestion: "Unified System Automation"

---

## Step 3: Enable Gmail API

1. In Google Cloud Console, go to: **APIs & Services** → **Library**
2. Search for: **Gmail API**
3. Click: **Enable**

**Wait for:** "API enabled" confirmation (few seconds)

---

## Step 4: Configure OAuth Consent Screen

1. Go to: **APIs & Services** → **OAuth consent screen**
2. Select User Type: **External**
3. Click **Create**

**Fill in:**

- App name: **Unified System Gmail Agent**
- User support email: **<gonya90.gg@gmail.com>**
- Developer contact email: **<gonya90.gg@gmail.com>**

1. Click **Save and Continue**
2. **Scopes:** Click **Add or Remove Scopes**
   - Search: `gmail.readonly`
   - Select: Gmail API - Read all resources
   - Search: `gmail.send`
   - Select: Gmail API - Send email
   - Search: `gmail.modify`
   - Select: Gmail API - Modify labels
3. Click **Update** → **Save and Continue**
4. **Test users:** Click **Add Users**
   - Enter: **<gonya90.gg@gmail.com>**
   - Click **Add**
5. Click **Save and Continue**
6. Review and click **Back to Dashboard**

---

## Step 5: Create OAuth2 Credentials

1. Go to: **APIs & Services** → **Credentials**
2. Click: **Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: **Gmail Automation Agent**
5. Click **Create**

**Important:** Download JSON file immediately!

---

## Step 6: Install Credentials

```bash
# Create credentials directory
mkdir -p /Users/macbook/Documents/Unified_System/Scripts/automation/.credentials

# Move downloaded file (update filename if different)
mv ~/Downloads/client_secret_*.json \
   /Users/macbook/Documents/Unified_System/Scripts/automation/.credentials/gmail_credentials.json
```

**Verify:**

```bash
ls -la /Users/macbook/Documents/Unified_System/Scripts/automation/.credentials/gmail_credentials.json
```

Should see the file listed.

---

## Step 7: First Run - Authentication

```bash
cd /Users/macbook/Documents/Unified_System/Scripts/automation
python3 gmail_agent.py
```

**What happens:**

1. Browser opens automatically
2. You see Google sign-in page
3. Sign in with: **<gonya90.gg@gmail.com>**
4. Google shows: "Unified System Gmail Agent wants to access your Google Account"
5. Review permissions
6. Click: **Allow** (or **Continue**)
7. You may see: "Google hasn't verified this app" - Click **Advanced** → **Go to Unified System Gmail Agent (unsafe)**
8. Click **Allow** again
9. Browser shows: "The authentication flow has completed"
10. Return to terminal

**Expected terminal output:**

```text
✅ Authentication successful!
📧 Fetching recent emails (last 24 hours)...
✅ Found X emails
...
```

---

## Step 8: Verify Setup

```bash
# Check if token was created
ls -la /Users/macbook/Documents/Unified_System/Scripts/automation/.credentials/gmail_token.pickle
```

**Token file should exist!**

---

## Step 9: Test Email Categorization

Run again to see email summary:

```bash
python3 gmail_agent.py
```

**You should see:**

```text
╔══════════════════════════════════════════════════════════════╗
║   Gmail Automation Agent - Email Summary                    ║
╚══════════════════════════════════════════════════════════════╝

📊 Email Statistics:
  📧 info: X
  🐙 github: X
  💼 work: X
  ...

Total: X emails
```

---

## Step 10: Add to Cron (Optional)

```bash
crontab -e
```

**Add line:**

```bash
# Check email every hour
0 * * * * /usr/bin/python3 /Users/macbook/Documents/Unified_System/Scripts/automation/gmail_agent.py >> /Users/macbook/Documents/Unified_System/logs/automation/gmail_agent.log 2>&1
```

**Save and exit.**

---

## ✅ Success Checklist | Контрольный список

- [ ] Python packages installed
- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth consent screen configured
- [ ] Test user added (<gonya90.gg@gmail.com>)
- [ ] OAuth2 credentials created
- [ ] JSON file downloaded
- [ ] JSON file moved to .credentials/
- [ ] First authentication completed
- [ ] Token file created
- [ ] Email categorization working
- [ ] (Optional) Added to cron

---

## 🎉 You're Done! | Готово

**Gmail automation is now active for <gonya90.gg@gmail.com>!**

**Test it works:**

```bash
cd /Users/macbook/Documents/Unified_System/Scripts/automation
./run_all.sh
```

Should now include Gmail processing!

---

## 🔧 Troubleshooting | Устранение неполадок

### "Credentials not found"

```bash
# Verify file exists
ls /Users/macbook/Documents/Unified_System/Scripts/automation/.credentials/gmail_credentials.json

# If missing, re-download from Google Cloud Console
```

### "This app isn't verified"

**This is expected for personal apps!**

1. Click **Advanced**
2. Click **Go to Unified System Gmail Agent (unsafe)**
3. Continue with authentication

This is safe - it's YOUR app for YOUR account.

### "Permission denied"

```bash
# Make sure email is in test users
# Go to: OAuth consent screen → Test users
# Add: gonya90.gg@gmail.com
```

---

**Status:** Ready to automate!  
**Email:** <gonya90.gg@gmail.com>  
**Next:** Run automation and enjoy smart email categorization! 🎉
