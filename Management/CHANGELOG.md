# Changelog

All notable changes to the Unified AI Bot project.

## [2.0.0] - 2025-12-27 - MEGA UPDATE 🚀

### 🎉 Major Features Added (7 in one session!)

#### 1. Notification Manager

- Smart quiet hours (23:00-08:00) - no disturbing notifications at night
- Priority levels: CRITICAL, HIGH, NORMAL, LOW
- Configurable via `/notify` command
- Automatic batching of low-priority messages

#### 2. Dashboard v2 (Web UI)

- Real-time token usage charts (Chart.js)
- Infrastructure status monitoring
- Live system logs viewer
- Quick action buttons (Backup, Restart)
- Accessible at `http://<server-ip>:8096`

#### 3. Cost Tracking Pro

- Detailed breakdown by models (Gemini, OpenAI, Ollama)
- Provider-level statistics
- Per-user analytics (admin only)
- `/costs` command for comprehensive reports
- Historical data (30 days)

#### 4. Linear API Integration

- Professional task management
- Create issues: `/linear create <title>`
- View assigned tasks: `/linear me`
- Priority indicators (🔴🟠🟡🟢)
- Team management: `/linear teams`

#### 5. Daily Digest

- Automated morning summary (09:00 AM)
- Yesterday's token usage stats
- Active tasks (local + Linear)
- Calendar events for today
- Infrastructure health status
- Motivational quotes
- Manual trigger: `/digest`

#### 6. Google Calendar Integration

- Today's events: `/calendar today`
- Weekly view: `/calendar week`
- Automatic inclusion in daily digest
- Timezone-aware (Europe/Kiev)

#### 7. HomeKit Bridge

- Full Apple Home integration
- Auto-discovery of HA devices
- Supported accessories:
  - Lights (with state sync)
  - Switches
  - Temperature sensors
- Setup code: 123-45-678
- Commands: `/homekit start|stop|status`

### 🔧 Improvements

#### SerpApi Integration

- Replaced DuckDuckGo with Google Search
- Knowledge Graph support
- Structured search results
- Fallback to DDG if API fails

#### Home Assistant Enhancements

- `/ha sensors` - view all sensor readings
- `/ha script <name>` - run HA scripts
- `/ha scene <name>` - activate scenes
- Improved error handling

#### Alice Skill Automation

- Cloudflare Tunnel auto-setup script
- Systemd service for persistent tunnel
- Quick setup guide (ALICE_QUICK_SETUP.md)
- One-command deployment

### 📚 Documentation

- Updated README with all features
- Created ALICE_QUICK_SETUP.md
- Enhanced ALICE_SETUP.md
- Added inline code documentation

### 🐛 Bug Fixes

- Fixed Gemini API message format
- Corrected config loading precedence
- Resolved markdown linting warnings
- Fixed `/todo list` command logic

### 🔐 Security

- Admin-only commands (`/update`, `/backup`, `/costs` analytics)
- NOPASSWD sudo for bot restart
- API key validation
- User authentication on all commands

### 📦 Dependencies Added

- `apscheduler` - job scheduling
- `psutil` - system metrics
- `PyYAML` - config parsing
- `fastapi` + `uvicorn` - web dashboard
- `jinja2` - HTML templates
- `linear-sdk` - Linear API
- `google-api-python-client` - Calendar
- `google-search-results` - SerpApi
- `HAP-python[QRCode]` - HomeKit

### 🎯 Performance

- Optimized database queries
- Async/await throughout
- Background task scheduling
- Efficient state synchronization

---

## [1.5.0] - 2025-12-26

### Added

- Voice message transcription (OpenAI Whisper)
- Reminder system with APScheduler
- Enhanced `/status` dashboard
- Infrastructure monitoring (`/infra`)
- Vision capabilities (photo analysis)
- Watchdog service for self-healing
- Self-update command (`/update`)
- Database backup system (`/backup`)

### Changed

- Improved error reporting
- Better logging system
- Consolidated task management

---

## [1.0.0] - 2025-12-25

### Initial Release

- Multi-model AI chat (Gemini, OpenAI, Ollama)
- Image generation (DALL-E 3)
- Home Assistant control
- Web search (DuckDuckGo)
- Task management (`/todo`)
- Usage tracking
- Alice Skill integration
- User authentication
- Conversation history

---

## Statistics

**Total Features**: 25+
**Lines of Code**: ~5,000+
**Commands**: 20+
**Integrations**: 10+ (Telegram, HA, Linear, Calendar, HomeKit, Alice, etc.)
**Deployment**: Fully automated with systemd

---

## Roadmap

### Planned Features

- [ ] BIOS Update automation for Proxmox
- [ ] Text-to-Speech for Alice responses
- [ ] Notion integration for notes
- [ ] Apple Health / Google Fit monitoring
- [ ] Advanced analytics dashboard
- [ ] Multi-user support with roles
- [ ] Plugin system for extensions

### Under Consideration

- [ ] WhatsApp integration
- [ ] Slack bot
- [ ] Email automation
- [ ] Smart home scenes builder
- [ ] Voice commands in Telegram
