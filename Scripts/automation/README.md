# Unified System Automation | Автоматизация Unified System

## Overview | Обзор

**English:** Automated workflows for ChatGPT integration, CV synchronization, and GitHub collaboration monitoring.

**Russian:** Автоматические рабочие процессы для интеграции ChatGPT, синхронизации CV и мониторинга коллаборации через GitHub.

---

## Scripts | Скрипты

### 1. `chatgpt_integration.sh`

**What it does:**

- Monitors CV files for changes
- Pulls latest updates from GitHub (from ChatGPT)
- Checks for new OpenAI conversation exports
- Automatically syncs PROFILE.md when CV changes

**Что делает:**

- Мониторит файлы CV на изменения
- Получает последние обновления из GitHub (от ChatGPT)
- Проверяет новые экспорты разговоров OpenAI
- Автоматически синхронизирует PROFILE.md при изменении CV

---

### 2. `cv_sync.sh`

**What it does:**

- Analyzes all CV files (EN/RU/HE)
- Finds most recent version
- Checks if PROFILE.md is in sync
- Auto-updates PROFILE.md (with `--auto-update` flag)

**Что делает:**

- Анализирует все файлы CV (EN/RU/HE)
- Находит самую свежую версию
- Проверяет синхронизацию с PROFILE.md
- Автоматически обновляет PROFILE.md (с флагом `--auto-update`)

---

### 3. `github_chatgpt_monitor.sh`

**What it does:**

- Monitors GitHub repository activity
- Tracks commits from Antigravity, ChatGPT, and manual
- Shows sync status with remote
- Logs collaboration statistics

**Что делает:**

- Мониторит активность в GitHub репозитории
- Отслеживает коммиты от Antigravity, ChatGPT и ручные
- Показывает статус синхронизации с remote
- Логирует статистику коллаборации

---

### 4. `run_all.sh` (Master Controller)

**What it does:**

- Runs all automation scripts in sequence
- Provides unified logging
- Shows complete automation cycle status

**Что делает:**

- Запускает все скрипты автоматизации последовательно
- Обеспечивает единое логирование
- Показывает статус полного цикла автоматизации

---

## Manual Usage | Ручное использование

### Run all automation

```bash
cd /Users/macbook/Documents/Unified_System/Scripts/automation
./run_all.sh
```

### Check specific automation

```bash
# ChatGPT integration only
./chatgpt_integration.sh

# CV sync only
./cv_sync.sh

# GitHub monitor only
./github_chatgpt_monitor.sh
```

---

## Automated Schedule | Автоматическое расписание

### Cron Setup

**Install cron jobs:**

```bash
# Edit crontab
crontab -e

# Add these lines:
0 */6 * * * /Users/macbook/Documents/Unified_System/Scripts/automation/run_all.sh >> /Users/macbook/Documents/Unified_System/logs/automation/cron.log 2>&1
0 * * * * /Users/macbook/Documents/Unified_System/Scripts/automation/github_chatgpt_monitor.sh >> /Users/macbook/Documents/Unified_System/logs/automation/monitor.log 2>&1
0 9 * * * /Users/macbook/Documents/Unified_System/Scripts/automation/cv_sync.sh --auto-update >> /Users/macbook/Documents/Unified_System/logs/automation/cv_sync.log 2>&1
```

**Schedule:**

- **Full automation:** Every 6 hours
- **GitHub monitor:** Every hour
- **CV sync:** Daily at 9 AM

---

## What Gets Automated | Что автоматизируется

### ✅ ChatGPT Collaboration

1. **Pull updates from ChatGPT**
   - ChatGPT updates PROFILE.md via GitHub → Auto-pulled

2. **Push updates to ChatGPT**
   - CV changes → PROFILE.md updated → Pushed to GitHub → ChatGPT sees it

3. **Conversation exports**
   - Detects new OpenAI exports
   - Prompts for processing

### ✅ CV Management

1. **Change detection**
   - Monitors all CV files (EN/RU/HE)
   - Tracks modification dates with SHA256 hashes

2. **Auto-sync**
   - Updates PROFILE.md timestamp
   - Commits to Git
   - Pushes to GitHub

3. **Consistency check**
   - Ensures all CV versions are tracked
   - Reports sync status

### ✅ GitHub Monitoring

1. **Activity tracking**
   - Counts commits by source (Antigravity/ChatGPT/Manual)
   - Logs collaboration statistics

2. **Sync status**
   - Checks if ahead/behind remote
   - Detects pending changes

3. **Health checks**
   - Verifies Git status
   - Reports collaboration health

---

## Logs | Логи

**Location:** `/Users/macbook/Documents/Unified_System/logs/automation/`

**Files:**

- `cron.log` - Full automation runs
- `monitor.log` - GitHub monitoring
- `cv_sync.log` - CV synchronization
- `chatgpt_integration.log` - ChatGPT integration events

**View logs:**

```bash
# Latest full automation run
tail -f /Users/macbook/Documents/Unified_System/logs/automation/cron.log

# GitHub activity
tail -f /Users/macbook/Documents/Unified_System/logs/automation/monitor.log

# CV sync history
cat /Users/macbook/Documents/Unified_System/logs/automation/cv_sync.log
```

---

## Troubleshooting | Устранение неполадок

### Script won't run

```bash
# Make executable
chmod +x /Users/macbook/Documents/Unified_System/Scripts/automation/*.sh
```

### Cron not working

```bash
# Check if cron is running
ps aux | grep cron

# View cron log
grep CRON /var/log/system.log

# Test script manually
cd /Users/macbook/Documents/Unified_System/Scripts/automation
./run_all.sh
```

### Git push failures

```bash
# Check git credentials
git config --global user.name
git config --global user.email

# Test push manually
cd /Users/macbook/Documents/Unified_System
git push origin main
```

---

## Architecture | Архитектура

```text
┌─────────────────────────────────────────────────────────┐
│                   Cron Scheduler                         │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   Every 6h     Every 1h    Daily 9AM
        │           │           │
        │           │           │
┌───────▼─────┐ ┌──▼──────┐ ┌──▼────────┐
│run_all.sh   │ │monitor  │ │cv_sync    │
│             │ │.sh      │ │.sh        │
└──────┬──────┘ └───┬─────┘ └──┬────────┘
       │            │           │
   ┌───┼────────────┼───────────┘
   │   │            │
   ▼   ▼            ▼
┌──────────────────────────────────┐
│   Git Repository (GitHub)         │
│   ├─ Agent_Context/              │
│   │  └─ Personal_Profile/        │
│   │     ├─ PROFILE.md  ◄─────────┤─── ChatGPT
│   │     ├─ CV_*.pdf              │
│   │     └─ ...                   │
│   └─ logs/automation/            │
└──────────────────────────────────┘
```

---

## Benefits | Преимущества

### No Manual Work

- ✅ CV changes auto-detected
- ✅ PROFILE.md auto-updated
- ✅ Git auto-committed
- ✅ GitHub auto-synced

### ChatGPT Integration

- ✅ ChatGPT can update via GitHub
- ✅ Changes auto-pulled to local
- ✅ Both AIs always in sync

### Monitoring

- ✅ Collaboration statistics
- ✅ Sync health checks
- ✅ Activity logging

---

## Status | Статус

**Current:** ✅ Ready to deploy  
**Testing:** Manual testing required  
**Production:** Configure cron for production use  

---

**Last Updated:** 2025-12-25  
**Maintained by:** Antigravity AI Agent
