# 🤖 Автоматические задачи AI ассистента

## Описание | Description

**English:** Automated tasks for personal AI assistant - email management, LinkedIn sync, profile updates.

**Russian:** Автоматические задачи для персонального AI ассистента - управление почтой, синхронизация LinkedIn, обновление профиля.

---

## 📧 Task 1: Email Management | Управление почтой

### Цель

- Читать и проверять почту <gar.yk227@yandex.ru>
- Сортировать по категориям
- Отвечать на важные письма
- Архивировать/удалять спам

### Периодичность

- **Проверка:** Каждые 30 минут
- **Глубокий анализ:** 3 раза в день (09:00, 14:00, 19:00)

### Категории сортировки

1. **🔴 Urgent** - Требует немедленного ответа
   - Job offers
   - Client requests
   - Critical notifications

2. **🟡 Important** - Важно, но не срочно
   - GitHub notifications
   - LinkedIn messages
   - Professional contacts

3. **🟢 Info** - Информация к сведению
   - Newsletters
   - Updates
   - Subscriptions

4. **⚪ Spam** - Спам/нежелательное
   - Marketing без запроса
   - Подозрительные адреса
   - Repeated promotions

### Действия

```yaml
on_email_received:
  1. Analyze subject and sender
  2. Check against known contacts
  3. Categorize using AI
  4. If urgent:
     - Notify user immediately
     - Draft response
  5. If important:
     - Mark for review
     - Add to daily summary
  6. If spam:
     - Move to spam folder
     - Update filter rules
```

---

## 💼 Task 2: LinkedIn Profile Management | Управление профилем LinkedIn

### LinkedIn Goals | Цели LinkedIn

- Поддерживать актуальность профиля
- Синхронизировать с CV
- Автоматические посты о достижениях
- Управление связями

### LinkedIn Schedule | Расписание LinkedIn

- **Проверка обновлений:** Ежедневно
- **Синхронизация с CV:** Еженедельно
- **Посты:** По мере появления контента
- **Связи:** При обновлении GitHub

### Синхронизация данных

**Источники:**

1. `Personal_Profile/CV_Igor_Goncharenko_EN.pdf`
2. `Personal_Profile/CV_Igor_Goncharenko_RU.pdf`
3. `Personal_Profile/CV_Igor_Goncharenko_HE_RTL.pdf`
4. `Personal_Profile/PROFILE.md` (из GitHub)
5. GitHub activity (Gonya990)

**Что синхронизировать:**

```yaml
Skills:
  - Extract from CV
  - Add new from GitHub projects
  - Update proficiency levels
  - Add certifications

Experience:
  - Current: Unified_System development
  - Technologies used
  - Projects and achievements
  - Link to GitHub repos

Education:
  - From CV
  - Online courses completion
  - Certifications

Projects:
  - GitHub repos with README
  - Description from commits
  - Technologies used
  - Achievements/stats
```

### Автоматические посты

**When to post:**

1. **GitHub milestone reached**

   ```text
   🚀 Just reached {milestone} in {project}!
   
   {Brief description}
   
   Tech stack: {technologies}
   
   #coding #opensource #ai
   ```

2. **New project launched**

   ```text
   📢 Excited to share my new project: {name}
   
   {What it does}
   {Why it matters}
   
   Check it out: {github_link}
   
   #development #innovation
   ```

3. **Weekly summary** (if significant activity)

   ```text
   📊 This week's learning:
   - {achievement 1}
   - {achievement 2}
   - {achievement 3}
   
   Always growing! 🌱
   
   #learning #development
   ```

---

## 🔄 Task 3: CV/Resume Synchronization | Синхронизация CV/резюме

### CV Sync Goals | Цели синхронизации CV

- Все версии CV актуальны
- Соответствие LinkedIn
- Автоматическое обновление при изменениях

### Файлы для мониторинга

```text
Personal_Profile/
├── CV_Igor_Goncharenko_EN.pdf
├── CV_Igor_Goncharenko_RU.pdf  
├── CV_Igor_Goncharenko_HE_RTL.pdf
├── CV_Igor_Goncharenko_HE_RTL. нов.docx
└── PROFILE.md
```

### Проверка актуальности

**Ежедневная проверка:**

1. Сравнить даты модификации
2. Проверить consistency между версиями
3. Сравнить с GitHub profile
4. Сравнить с LinkedIn

**При обнаружении расхождений:**

1. Создать отчет с различиями
2. Предложить обновления
3. После подтверждения - обновить все версии
4. Sync to LinkedIn

### Источники актуальной информации

```yaml
Primary Source: GitHub activity
  - New repos
  - Technologies used
  - Contributions
  - Stars/followers

Secondary: Personal_Profile/PROFILE.md
  - Manual updates
  - Career changes
  - New skills

Tertiary: Email signatures and contacts
  - Job titles
  - Companies
  - Professional changes
```

---

## 📊 Task 4: Professional Network Management | Управление профессиональной сетью

### LinkedIn Connections

**Автоматическое управление:**

1. **New connection requests**
   - Analyze profile
   - Check mutual connections
   - Relevance to my field
   - Recommend accept/reject

2. **Engagement**
   - Like relevant posts from connections
   - Comment on interesting topics
   - Share valuable content

3. **Follow-up**
   - Thank new connections
   - Periodic check-ins with key contacts
   - Birthday/work anniversary messages

### Contact Database

**Синхронизация:**

- LinkedIn contacts → Local database
- Email contacts → LinkedIn
- GitHub collaborators → Professional network
- Update contact info when changed

---

## 🤖 Implementation | Реализация

### Technology Stack

```yaml
Email Management:
  - API: Yandex Mail API
  - Processing: Python + AI categorization
  - Storage: Local SQLite database
  - Notifications: MCP Agent Mail

LinkedIn Management:
  - API: LinkedIn API (если доступен)
  - Alternative: Browser automation
  - Updates: Scheduled via cron
  - Content: AI-generated from activity

CV Sync:
  - Monitor: File watchers
  - Diff: PDF text extraction + comparison
  - Update: Template-based generation
  - Deploy: Git commits

Network:
  - Database: SQLite/JSON
  - Updates: Daily sync
  - Analytics: Contact growth, engagement
```

### Cron Schedule

```bash
# Email checks
*/30 * * * * /path/to/check_email.sh

# LinkedIn update - daily at 08:00
0 8 * * * /path/to/sync_linkedin.sh

# CV consistency check - weekly on Monday
0 9 * * 1 /path/to/check_cv_consistency.sh

# Network update - daily at 20:00  
0 20 * * * /path/to/update_contacts.sh

# Weekly summary - Sunday at 19:00
0 19 * * 0 /path/to/generate_weekly_summary.sh
```

---

## 📝 Configuration | Конфигурация

### Credentials (stored in .env)

```bash
# Email
YANDEX_EMAIL=gar.yk227@yandex.ru
YANDEX_APP_PASSWORD=<app-specific-password>

# LinkedIn
LINKEDIN_EMAIL=<your-linkedin-email>
LINKEDIN_PASSWORD=<or-use-session>

# GitHub
GITHUB_TOKEN=<already-configured>
GITHUB_USER=Gonya990

# AI Services
OPENAI_API_KEY=<if-using>
GEMINI_API_KEY=<already-configured>
```

### User Preferences

```json
{
  "email": {
    "auto_reply": false,
    "auto_categorize": true,
    "notify_urgent": true,
    "daily_summary": true
  },
  "linkedin": {
    "auto_post": false,
    "require_approval": true,
    "sync_skills": true,
    "auto_accept_connections": false
  },
  "cv": {
    "auto_update": false,
    "check_consistency": true,
    "notify_on_changes": true
  }
}
```

---

## 🎯 Success Metrics | Метрики успеха

### Email

- ✅ 0 unread urgent emails
- ✅ <50 inbox items
- ✅ <5min response time to urgent
- ✅ 99% spam correctly filtered

### LinkedIn

- ✅ Profile updated within 24h of CV change
- ✅ Skills match GitHub activity
- ✅ Weekly engagement rate >5%
- ✅ Network growth >1% monthly

### CV

- ✅ All versions in sync
- ✅ Updated within 1 week of major change
- ✅ 100% accuracy across languages

---

## 🚀 Getting Started | Начало работы

### Immediate Setup

1. **Enable email access**

   ```bash
   # Configure Yandex app password
   # Store in .env
   ```

2. **Verify LinkedIn access**

   ```bash
   # Test login
   # Set up automation
   ```

3. **Initialize profile database**

   ```bash
   cd /Users/macbook/Documents/Unified_System/Scripts/personal_assistant
   ./setup.sh
   ```

4. **Test automation**

   ```bash
   # Run once manually
   ./check_email.sh --dry-run
   ./sync_linkedin.sh --dry-run
   ./check_cv_consistency.sh
   ```

5. **Enable cron jobs**

   ```bash
   crontab -e
   # Add lines from schedule above
   ```

---

## 📚 Next Steps | Следующие шаги

1. ✅ Создать скрипты автоматизации
2. ✅ Настроить API доступы
3. ✅ Протестировать в dry-run режиме
4. ✅ Включить автоматическое выполнение
5. ✅ Мониторить и оптимизировать

---

**Status:** Ready for implementation | Готов к реализации  
**Priority:** High | Высокий  
**Estimated setup time:** 2-3 hours | 2-3 часа на настройку
