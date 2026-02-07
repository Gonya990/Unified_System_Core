# OpenClaw Migration Analysis Report

> **Date:** 2026-02-07
> **Status:** Complete Codebase Audit
> **Decision:** Migrate to OpenClaw as central gateway/orchestrator
> **Content Factory:** Preserved as standalone MCP server

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Current System Inventory](#2-current-system-inventory)
3. [Content Factory → MCP Analysis](#3-content-factory--mcp-analysis)
4. [Telegram Bot → OpenClaw Skills Analysis](#4-telegram-bot--openclaw-skills-analysis)
5. [Data Migration Plan](#5-data-migration-plan)
6. [Infrastructure Analysis](#6-infrastructure-analysis)
7. [Migration Questions — Answered](#7-migration-questions--answered)
8. [Risk & Rollback Plan](#8-risk--rollback-plan)
9. [Migration Phases](#9-migration-phases)
10. [Credentials Inventory](#10-credentials-inventory)
11. [Architecture: Before & After](#11-architecture-before--after)

---

## 1. Executive Summary

The Unified System Core is a **4,900+ line Telegram bot** (`ai_telegram_bot_v2.py`) acting as a monolithic gateway for 55+ commands spanning AI chat, content production, home automation, calendar, email, family tools, infrastructure management, and agent orchestration. The system runs across a Tailscale mesh of 4-6 nodes.

**Current critical issues:**
- Bot STOPPED due to DB path issues and zombie processes
- Content Factory producing 1-second videos (ffmpeg failure)
- Scheduler conflicts (host + container simultaneously)
- Duplicate mail_processor processes
- Google Calendar integration planned but unimplemented
- Instagram upload broken
- No prompt injection mitigations

**Migration to OpenClaw provides:**
- Gateway pattern replacing the monolithic bot
- 100+ community-maintained integrations (Calendar, Gmail, WhatsApp, Discord, HA)
- Proper persistent memory replacing broken SQLite DB
- Multi-channel routing (Telegram + WhatsApp + Discord + Web from one config)
- Built-in health checks, cron, credential management

---

## 2. Current System Inventory

### 2.1 Docker Compose Services (root `docker-compose.yml`)

| Service | Image | Purpose | Status |
|---------|-------|---------|--------|
| `ai-bot` | `ghcr.io/.../ai-telegram-bot` | Telegram bot (ai_telegram_bot_v2.py) | STOPPED |
| `mail-intelligence` | `ghcr.io/.../mail-intelligence` | MCP mail processor | Running (duplicate on host) |
| `content-factory` | `ghcr.io/.../content-factory` | Video pipeline scheduler | Running (degraded — 1s videos) |
| `dashboard` | `ghcr.io/.../dashboard` | ChatKit Dashboard (port 3005) | Running |
| `markitdown-mcp` | `ghcr.io/.../markitdown-mcp` | Document conversion MCP (port 8000) | Running |

### 2.2 Additional Infrastructure

| Component | Location | Purpose |
|-----------|----------|---------|
| MCP Agent Mail | `Deployment/igor-gaming-1/` | Postgres + HTTP mail server (port 8765) |
| CLIProxyAPI | `infra/cliproxyapi/` | CLI proxy (port 8317) + Watchtower |
| N8N | igor-gaming node | Workflow automation (port 5678) |

### 2.3 Tailscale Network Topology

| Node | IP | Role |
|------|-----|------|
| MacBook Air | 100.93.121.47 | Admin / Control Plane |
| igor-gaming (Windows) | 100.127.194.111 | GPU + N8N + Interactive |
| Proxmox | 100.74.194.25 | VM Host (64GB RAM) |
| Smart Linux | 100.118.179.47 | Server / Mail |
| unified-cloud-core | 100.87.208.56 | Primary archive / orchestrator |
| gpu-node-1 | 100.67.107.71 | Secondary GPU / rendering |

### 2.4 Agent Council (MCP Mail)

| Agent | Role | Program |
|-------|------|---------|
| PinkLake | Supreme Orchestrator | antigravity-core |
| OrangeStone | Chief Technical Agent | antigravity |
| FuchsiaCat | Operational Agent | opencode |
| VioletCastle | Assistant | claude-code |

---

## 3. Content Factory → MCP Analysis

### 3.1 Pipeline Architecture

```
Research → Script → Voice → B-Roll → Assembly → Subtitles → Upload
   │          │        │       │         │          │          │
   ▼          ▼        ▼       ▼         ▼          ▼          ▼
Gemini/   Gemini    OpenAI  Pexels    ffmpeg    ASS/SRT    Instagram
RSS/Web   GPT-4     TTS     API       concat    generator  YouTube
feeds     script    + Edge             + burn               Threads
          gen       TTS                subs                 Telegram
```

### 3.2 Entry Points (Critical for MCP Design)

| Entry Point | Trigger | File |
|-------------|---------|------|
| Scheduler (primary) | `--scheduler` flag, runs in Docker | `src/pipeline/factory_scheduler.py` |
| Manual CLI | `--hebrew`, `--english`, `--cartoon`, `--auto` flags | Same file, `__main__` |
| Telegram `/factory` | Bot command → calls `run_factory_production()` | `ai_factory_commands.py` → `factory_scheduler.py` |
| Longform producer | `--longform` flag or Saturday cron | `src/pipeline/longform_producer.py` |
| Production shipper | Post-production upload | `src/pipeline/production_shipper.py` |

### 3.3 Core Function Signature (MCP Tool Candidate)

```python
# From factory_scheduler.py:193
def run_factory_production(
    mode="daily",           # daily | hebrew | english | cartoon | auto
    manual_topic=None,      # Override research topic
    manual_outline=None,    # Override script outline
    style_override=None     # impact | cartoon | sketch | painting
) -> None:                  # Currently returns None, writes to filesystem
```

**MCP wrapper needs to:**
1. Accept these 4 parameters as tool arguments
2. Return the output video path + upload status
3. Report progress (research → assets → production → upload phases)

### 3.4 External Dependencies

| Dependency | Usage | Required From MCP Host |
|-----------|-------|----------------------|
| **ffmpeg** | Video assembly, subtitle burn, trimming | YES — must be installed |
| **ffprobe** | Duration detection | YES |
| OpenAI API | TTS voice generation, GPT-4 scripts | API key only |
| Google Gemini | Research, content generation | API key only |
| Pexels API | B-roll stock footage | API key only |
| ElevenLabs | Premium voice generation | API key only |
| Suno AI | AI music generation | API key only |
| Runway ML / Luma / Kling | AI video clips | API key only |
| `schedule` library | Python scheduler | pip install |
| `feedparser` | RSS parsing | pip install |
| `beautifulsoup4` | Web scraping | pip install |
| `instagrapi` | Instagram upload | pip install (broken currently) |
| Playwright | Threads browser automation | pip install + browser |

### 3.5 Schedule (Current)

| Time (UTC) | Mode | Day |
|-----------|------|-----|
| 07:00 + 0-45min jitter | Daily (Russian) | Every day |
| 12:00 + 0-60min jitter | English | Every day |
| 18:00 + 0-30min jitter | Cartoon | Every day |
| 08:00 Sunday | Hebrew weekly special | Sunday |
| 16:00 Saturday | Longform documentary | Saturday |

### 3.6 Long-Running Job Pattern

**Duration:** 5-30 minutes per production run (research + generation + encoding + upload).

**Progress reporting:** Currently uses `agent_sync()` which sends MCP mail + Telegram notification at each phase. No polling/webhook pattern exists — it's fire-and-forget with notifications.

**MCP implication:** MCP tools are request/response. Options:
1. **Async tool with notification:** Start production, return job ID, send completion notification via OpenClaw's messaging
2. **Background job pattern:** OpenClaw's cron triggers factory, factory notifies on completion
3. **Recommended:** Use OpenClaw cron for scheduling + MCP tool for on-demand triggers. Tool returns immediately with "Job started, will notify when done." Factory calls back to OpenClaw on completion.

### 3.7 Upload Decision

**Keep uploaders IN the Content Factory MCP.** Rationale:
- Uploaders are tightly coupled to video output (format validation, trimming, caption generation)
- Instagram uses `instagrapi` session state that's factory-specific
- YouTube uses OAuth tokens stored with factory credentials
- Threads uses Playwright browser state
- Moving uploaders to separate OpenClaw skills would fragment the pipeline without benefit

**Exception:** Telegram upload could become native (OpenClaw sends message directly).

---

## 4. Telegram Bot → OpenClaw Skills Analysis

### 4.1 Complete Command Inventory (55 commands)

#### Category A: Absorbed by OpenClaw Core (no custom skill needed)

| Command | Function | OpenClaw Equivalent |
|---------|----------|-------------------|
| `/start` | Welcome message | Built-in greeting |
| `/help` | Command list | Built-in help |
| `/clear` | Clear conversation | Built-in context management |
| `/models` | List/switch AI models | Config-level model selection |
| `/setprovider` | Switch AI provider | Config-level provider selection |
| `/settings` | Bot settings | OpenClaw config UI |
| `/search` | Web search | Built-in web search skill |
| `/img`, `/image`, `/imagine` | Image generation | Built-in image generation (DALL-E skill) |
| `/memory` | View/manage memories | OpenClaw persistent memory |
| `/msg` | Send message to agent | OpenClaw native messaging |

**Count: 10 commands → absorbed by OpenClaw core**

#### Category B: Replaced by Community Skills

| Command | Function | OpenClaw Skill |
|---------|----------|---------------|
| `/calendar` | Google Calendar events | `google-calendar` skill |
| `/brief` | Daily briefing (calendar + weather + homework) | Custom skill wrapping calendar + weather API |
| `/mail` | Check email | `gmail` skill (Pub/Sub) |
| `/ha` | Home Assistant control | `home-assistant` skill (Wyoming Protocol) |
| `/say`, `/speak` | Yandex TTS via HA | Part of HA skill |
| `/todo` | Task management | `todoist` or built-in task skill |
| `/linear` | Linear issue tracking | `linear` community skill |
| `/notify`, `/remind` | Notifications/reminders | OpenClaw cron + heartbeat |
| `/digest` | Daily/weekly digest | Custom skill (easy) |

**Count: 9 commands → replaced by community skills**

#### Category C: Custom OpenClaw Skills Required

| Command | Function | Skill Design |
|---------|----------|-------------|
| `/factory` | Trigger Content Factory | MCP tool call to Content Factory server |
| `/generate_video` | Generate video from prompt | MCP tool → factory `run_factory_production()` |
| `/video_status` | Check video generation status | MCP tool → factory job status |
| `/aimusic` | Generate music (Suno) | MCP tool → factory music generator |
| `/aivoice` | Generate voice (ElevenLabs) | MCP tool → factory voice generator |
| `/aisub` | Generate subtitles | MCP tool → factory subtitle generator |
| `/agent` | Run AI agent (code-explorer, reviewer) | Custom skill wrapping agent orchestrator |
| `/pipeline` | Run agent pipeline (feature, bugfix) | Custom skill wrapping pipeline orchestrator |
| `/beads` | Task tracking (Bead system) | Custom skill with SQLite/file backend |
| `/mashov_homework` | Mashov school homework | Custom skill (scrapes Mashov API) |
| `/mashov_find_school` | Find Mashov school | Part of mashov skill |
| `/am` | Agent Mail operations | MCP tool → Agent Mail server |
| `/play` | Start gaming VM (Proxmox) | Custom skill → Proxmox API |
| `/stop_play` | Stop gaming VM | Part of Proxmox skill |
| `/infra` | Infrastructure overview | Custom skill → Tailscale + Docker API |
| `/status` | System status | Custom skill → health checks |
| `/health` | Health check | Part of status skill |
| `/backup` | System backup | Custom skill → backup script |
| `/update` | System update | Custom skill → git pull + docker rebuild |
| `/login` | Google OAuth flow | Part of auth management |
| `/approve` | Approve user | OpenClaw access control |
| `/setrole` | Set user role | OpenClaw access control |
| `/family_stats` | Family usage stats | Custom skill → usage tracker |
| `/share_key` | Share API key to swarm | Custom skill → key management |
| `/scan` | Scan/analyze | Custom skill |
| `/voicemode` | Voice assistant toggle | OpenClaw voice config |
| `/costs`, `/usage` | API usage/costs | Custom skill → usage tracker |
| `/newtask` | Create new task | Part of beads/todo skill |
| `/set_key` | Set API key | OpenClaw credential management |
| `/tl` | Timeline | Custom skill |
| `/note` | Quick note | OpenClaw memory |
| `/dashboard` | Dashboard link | Simple response skill |

**Count: ~33 commands → custom skills (many are simple wrappers)**

#### Category D: Likely Deprecated / Not Needed

| Command | Reason |
|---------|--------|
| `/post_to_telegram` | OpenClaw sends directly to Telegram |
| Zombie host processes | Eliminated by clean architecture |

### 4.2 Rich Telegram UI Elements

The bot uses:
- **InlineKeyboardMarkup** — settings, model selection, confirmation dialogs
- **CallbackQueryHandler** — button press handling
- **Photo/Voice/Document handlers** — multimedia input

**OpenClaw impact:** OpenClaw's Telegram channel adapter supports inline keyboards natively. Callback handlers may need mapping to OpenClaw's action system. Multi-modal input (photos, voice, documents) is supported via OpenClaw's attachment handling.

### 4.3 Proactive Messaging

| Feature | Current Implementation | OpenClaw Equivalent |
|---------|----------------------|-------------------|
| Morning Brief | `DailyScheduler` + `morning_brief.py` | OpenClaw cron → custom skill |
| Homework alerts | `homework_sentinel.py` | OpenClaw cron → mashov skill |
| Notification reminders | `NotifyManager` | OpenClaw cron + heartbeat |
| Digest emails | `DigestService` | OpenClaw cron → digest skill |
| Content Factory alerts | `agent_sync()` → Telegram | Factory MCP → OpenClaw notification |

All proactive messaging is supported by OpenClaw's native cron + heartbeat system.

---

## 5. Data Migration Plan

### 5.1 SQLite Database Schema (`user_context.db`)

**Table: `users`**
```sql
user_id INTEGER PRIMARY KEY,
username TEXT,
full_name TEXT,
is_approved BOOLEAN DEFAULT 0,
is_google_connected BOOLEAN DEFAULT 0,
google_creds TEXT,
branch_id TEXT DEFAULT 'HOME_HQ',
role TEXT DEFAULT 'MEMBER',
last_interaction TIMESTAMP,
created_at TIMESTAMP
```

**Table: `event_contexts`** — Calendar event context (user_id, event_title, description, time)

**Table: `kv_store`** — Generic key-value persistence

**Table: `chat_memories`** — AI-extracted facts (user_id, fact_short, fact_full, date)

**Table: `mashov_homework`** — Cached homework data (user_id, homework_data JSON, fetched_at)

**Table: `user_permissions`** — RBAC (user_id, project, resource, permissions JSON, granted_by)

**Table: `access_audit_log`** — Access audit trail

### 5.2 Migration to OpenClaw Memory

| Current Table | OpenClaw Destination |
|--------------|---------------------|
| `users` | OpenClaw user registry + access control config |
| `chat_memories` | OpenClaw MEMORY.md (persistent memory) |
| `kv_store` | OpenClaw memory or skill-specific storage |
| `event_contexts` | Dropped — OpenClaw has native calendar integration |
| `mashov_homework` | Skill-specific SQLite (kept within mashov skill) |
| `user_permissions` | OpenClaw access control (YAML config) |
| `access_audit_log` | OpenClaw's native audit logging |

### 5.3 Migration Script Required

Export `chat_memories` table → OpenClaw MEMORY.md format:
```
## Facts about User {username}
- {fact_short}: {fact_full} (learned {date})
```

Export `users` whitelist → OpenClaw access config:
```yaml
allowed_users:
  - telegram_id: 708531393
    role: owner
  - telegram_id: 5569219290
    role: member
  - telegram_id: 578363419
    role: member
```

### 5.4 Conversation History

The bot uses `ConversationManager` for in-memory conversation context (not persisted to SQLite). No migration needed — OpenClaw handles this natively with persistent context windows.

### 5.5 Generated Assets

Output videos, B-roll, music, and research data are stored in:
- `outputs/` (factory output videos)
- `assets/{date}/` (downloaded B-roll images)
- `broll/` (cached B-roll clips)

These are **not migrated** — they stay on the filesystem accessible to the Content Factory MCP server.

---

## 6. Infrastructure Analysis

### 6.1 Current Deployment Topology

```
unified-home-core-cloud (bare metal / K3s):
├── Docker Compose (5 services)
│   ├── ai-bot (STOPPED)
│   ├── mail-intelligence
│   ├── content-factory
│   ├── dashboard
│   └── markitdown-mcp
├── K3s cluster (degraded — bot scaled to 0)
│   └── telegram-bot deployment + PVC
├── Host processes (ZOMBIE — should not exist)
│   ├── mail_processor.py (PID 1167871, 1716518)
│   └── factory_scheduler.py (PID 1982458)
└── Tailscale node

igor-gaming (Windows):
├── N8N (port 5678)
├── MCP Agent Mail (Postgres + HTTP)
└── Tailscale node + GPU
```

### 6.2 Target Deployment with OpenClaw

```
unified-home-core-cloud:
├── Docker Compose (new)
│   ├── openclaw (gateway — port 3000)
│   ├── content-factory-mcp (MCP server — port 8100)
│   ├── markitdown-mcp (port 8000)
│   └── agent-mail (Postgres + HTTP — port 8765)
├── Tailscale (no public exposure)
└── Killed: all zombie processes, K3s removed

igor-gaming:
├── N8N (unchanged)
├── GPU inference (if needed by factory)
└── Tailscale node
```

### 6.3 Resource Assessment

OpenClaw requires:
- **Node >= 22** (check host)
- **2GB+ RAM** (host has 64GB via Proxmox — no issue)
- **LLM API key** (Opus 4.6 recommended — already using Anthropic)

Content Factory requires:
- **ffmpeg** (already installed)
- **Python 3.10+** (already installed)
- **ffprobe** (comes with ffmpeg)
- **Various API keys** (see credentials inventory)

**No GPU required on OpenClaw host.** Content Factory's heavy calls are API-based (not local inference). The only local compute is ffmpeg (CPU-bound, low resource).

### 6.4 Network Changes

| Current | After Migration |
|---------|----------------|
| Bot exposed via Telegram Bot API (outbound only) | OpenClaw exposed via Telegram Bot API (outbound only) |
| Dashboard on port 3005 | OpenClaw web UI on port 3000 (Tailscale only) |
| MarkItDown MCP on port 8000 | Same (registered with OpenClaw) |
| Agent Mail on port 8765 | Same (registered with OpenClaw) |
| No WhatsApp/Discord | OpenClaw multi-channel (Tailscale only) |

**No new public exposure.** Everything stays behind Tailscale.

---

## 7. Migration Questions — Answered

### Content Factory → MCP

**Q1. Can the Content Factory run standalone with a clean API boundary?**
YES. The factory is already architecturally independent. `run_factory_production()` in `factory_scheduler.py:193` is a clean entry point. It takes 4 parameters and produces a video. The only coupling to the bot is the `/factory` command calling this function. Wrapping it as an MCP tool is straightforward.

**Q2. What's the minimal interface to trigger a content creation job?**
```python
# MCP Tool Definition
{
    "name": "create_content",
    "description": "Trigger AI Content Factory video production",
    "parameters": {
        "mode": {"type": "string", "enum": ["daily", "hebrew", "english", "cartoon", "auto"]},
        "topic": {"type": "string", "description": "Optional topic override"},
        "outline": {"type": "string", "description": "Optional script outline"},
        "style": {"type": "string", "enum": ["impact", "cartoon", "sketch", "painting"]}
    }
}
```

**Q3. Are there long-running jobs?**
YES. A full production run takes 5-30 minutes (research + voice gen + B-roll download + ffmpeg assembly + multi-platform upload). Currently uses `agent_sync()` for progress notifications. For MCP: return immediately with job ID, use callback/notification pattern for completion.

**Q4. Does the factory need GPU access?**
NO. All AI-heavy operations (voice, music, video clips) are API calls to cloud services (OpenAI, ElevenLabs, Suno, Runway, Pexels). The only local compute is ffmpeg (CPU). The MCP server can run on the same host as OpenClaw.

**Q5. What happens to the uploaders?**
STAY in the Content Factory MCP. Uploaders (Instagram, YouTube, Threads, Telegram) are tightly coupled to the video pipeline (format validation, caption generation, session management). Exception: Telegram sending could be delegated to OpenClaw's native channel.

### Bot → OpenClaw Migration

**Q6. Which commands are just wrappers around external APIs?**
- `/calendar` → Google Calendar API (replace with community skill)
- `/mail` → Gmail API (replace with community skill)
- `/ha` → Home Assistant REST API (replace with community skill)
- `/search` → Web search API (OpenClaw built-in)
- `/img` → OpenAI DALL-E API (OpenClaw built-in)
- `/linear` → Linear API (community skill)
- `/todo` → Simple CRUD (OpenClaw built-in or todoist skill)

**Q7. Which commands have custom logic to preserve?**
- `/factory`, `/generate_video`, `/video_status` → Content Factory MCP (custom logic in pipeline)
- `/agent`, `/pipeline` → Agent Orchestrator (custom PIPELINES dict with multi-step flows)
- `/beads` → Bead task tracking system (custom project management)
- `/mashov_homework`, `/mashov_find_school` → Mashov API scraper (Israeli school system)
- `/play`, `/stop_play` → Proxmox VM management (custom Proxmox API calls)
- `/infra` → Multi-node infrastructure status (custom Tailscale + Docker checks)
- `/brief` → Composite: calendar + weather + homework + motivation quote

**Q8. Is there a user approval/whitelist system?**
YES. Two layers:
1. **Whitelist:** `ALLOWED_USERS` env var (comma-separated Telegram IDs). Auto-approves on first contact.
2. **RBAC:** Full role hierarchy (OWNER > ADMIN > DEVELOPER > MEMBER > FAMILY > GUEST) with project-scoped permissions, audit logging.

OpenClaw mapping: Use OpenClaw's access control config for whitelist. RBAC can be simplified to OpenClaw's built-in user roles since this is a single-family system.

**Q9. Inline keyboards / rich UI?**
YES. The bot uses InlineKeyboardMarkup for:
- Settings menus (model selection, provider switching)
- Confirmation dialogs (approve user, delete data)
- Factory mode selection

OpenClaw's Telegram adapter supports inline keyboards. These will need to be reimplemented as OpenClaw action buttons but the platform supports it.

**Q10. Proactive messaging?**
YES. The bot has:
- `DailyScheduler` — morning brief at 07:00
- `homework_sentinel.py` — homework alerts
- `NotifyManager` — reminder notifications
- `DigestService` — periodic digests
- `agent_sync()` — factory progress alerts

All map to OpenClaw cron + heartbeat system.

### Data Migration

**Q11. Schema of `user_context.db`?**
Documented in Section 5.1 above. 7 tables: users, event_contexts, kv_store, chat_memories, mashov_homework, user_permissions, access_audit_log. Can be exported to OpenClaw MEMORY.md for memories + YAML config for user access.

**Q12. Accumulated assets to preserve?**
YES — output videos in `outputs/`, B-roll in `broll/`, assets in `assets/`. These stay on the filesystem, accessible to the Content Factory MCP server. No migration needed — just ensure volume mounts are correct.

**Q13. Conversation logs worth preserving?**
NO. `ConversationManager` keeps in-memory context only. No persistent conversation history exists. OpenClaw's persistent memory will be a significant upgrade.

### Infrastructure

**Q14. Where will OpenClaw run?**
**Recommended: Same bare metal as current deployment** (`unified-home-core-cloud`). Reasons:
- 64GB RAM via Proxmox — more than enough
- Content Factory needs ffmpeg locally — colocate to avoid network latency
- Tailscale already configured
- K3s can be removed (Docker Compose is sufficient)

Alternative: Cloudflare free tier for OpenClaw gateway only, with factory MCP on the bare metal. But adds network complexity for no real benefit in a single-user setup.

**Q15. Can Content Factory coexist with OpenClaw on same host?**
YES. Content Factory's heavy workloads are:
- ffmpeg encoding (CPU, 1-3 minutes per video, 1-2 cores)
- API calls (network I/O, non-blocking)
- File I/O (minimal)

OpenClaw's workloads are:
- LLM API calls (network I/O)
- Message routing (minimal CPU)

No resource conflicts. Both run comfortably on a single host.

**Q16. Tailscale topology?**
OpenClaw should be a Tailscale node itself (inherit the host's Tailscale identity). This way:
- Web UI accessible from any Tailscale device
- MCP servers accessible via Tailscale IPs
- No public exposure needed
- Existing `100.x.x.x` addresses work unchanged

**Q17. DNS / reverse proxy?**
No existing Caddy/nginx/Traefik config found in the repo. The current setup uses direct port access over Tailscale. For OpenClaw, same approach works: `http://100.x.x.x:3000` for web UI.

If desired later, add Caddy for HTTPS + domain name (e.g., `openclaw.tailnet.ts.net`). Not required for migration.

### Risk & Rollback

**Q18. Parallel operation during transition?**
YES. Use a **different Telegram bot token** for OpenClaw:
1. Create new bot via @BotFather (e.g., `@UnifiedClaw_bot`)
2. Configure OpenClaw with new token
3. Keep old bot image tagged and deployable (`docker-compose.old.yml`)
4. Test OpenClaw features incrementally
5. Once validated, switch the original bot token to OpenClaw
6. Decommission old bot

**Q19. Rollback plan?**
1. Keep current Docker images tagged: `ai-telegram-bot:pre-openclaw`
2. Keep `docker-compose.yml` backed up as `docker-compose.pre-openclaw.yml`
3. Keep SQLite database backed up
4. Rollback = `docker compose -f docker-compose.pre-openclaw.yml up -d`
5. Total rollback time: < 2 minutes

**Q20. What must work from day one vs. acceptable temporary loss?**

**Must work from day one:**
- AI chat (core functionality)
- Content Factory trigger (via MCP)
- Home Assistant control
- Telegram connectivity

**Acceptable temporary loss:**
- Mashov homework integration (niche, can add later)
- Agent orchestrator pipelines (developer tool, not daily use)
- Proxmox VM management (rare use)
- Linear/Notion integrations (unused currently)
- Crypto bot (already degraded)
- Instagram upload (already broken)

---

## 8. Risk & Rollback Plan

### 8.1 Migration Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| OpenClaw instability (3mo old project) | Medium | Run parallel for 2 weeks. Keep old bot deployable. |
| Content Factory MCP integration issues | Medium | Test MCP wrapper standalone before connecting to OpenClaw |
| Lost Telegram UI richness | Low | OpenClaw supports inline keyboards. May need reimplementation. |
| Learning curve for OpenClaw config | Low | Well-documented. Single-user means low complexity. |
| Community skill quality | Medium | Audit all skills with Cisco Skill Scanner before installing |
| Prompt injection via skills | Low | Sandbox enabled, Tailscale-only access, Opus 4.6 resistance |

### 8.2 Rollback Triggers

Initiate rollback if:
- Core chat functionality breaks for > 1 hour
- Content Factory fails to produce videos after integration
- Memory/context corruption detected
- Security incident via community skill

### 8.3 Rollback Procedure

```bash
# 1. Stop OpenClaw
docker compose -f docker-compose.openclaw.yml down

# 2. Restore old stack
docker compose -f docker-compose.pre-openclaw.yml up -d

# 3. Verify
docker compose -f docker-compose.pre-openclaw.yml ps
curl http://localhost:8080/health  # old bot health check

# Total time: < 2 minutes
```

---

## 9. Migration Phases

### Phase 0: Preparation (Day 1)
- [ ] Kill all zombie host processes (mail_processor, factory_scheduler)
- [ ] Remove K3s (Docker Compose only)
- [ ] Backup current SQLite DB
- [ ] Tag current Docker images as `pre-openclaw`
- [ ] Copy `docker-compose.yml` → `docker-compose.pre-openclaw.yml`
- [ ] Create new Telegram bot token via @BotFather
- [ ] Install Node >= 22 on host

### Phase 1: OpenClaw Standalone (Day 2-3)
- [ ] Install OpenClaw via Docker
- [ ] Configure Opus 4.6 as LLM
- [ ] Enable sandbox, disable shell access
- [ ] Connect Telegram (new bot token)
- [ ] Verify basic chat works
- [ ] Configure OpenClaw behind Tailscale only
- [ ] Test: send message → get response

### Phase 2: Community Skills (Day 3-5)
- [ ] Audit and install `google-calendar` skill
- [ ] Audit and install `gmail` skill
- [ ] Audit and install `home-assistant` skill
- [ ] Test each integration
- [ ] Configure OpenClaw cron for morning brief
- [ ] Validate: calendar, email, HA working

### Phase 3: Content Factory MCP (Day 5-8)
- [ ] Create MCP server wrapper for Content Factory
- [ ] Expose `create_content`, `content_status`, `list_outputs` tools
- [ ] Register with OpenClaw via `mcporter`
- [ ] Migrate scheduler to OpenClaw cron (3 daily + 2 weekly)
- [ ] Test: trigger video production from OpenClaw
- [ ] Validate: end-to-end video production + upload

### Phase 4: Custom Skills (Day 8-12)
- [ ] Build mashov_homework skill
- [ ] Build infrastructure_status skill
- [ ] Build proxmox_control skill
- [ ] Build agent_orchestrator skill (if needed)
- [ ] Build beads/task_management skill
- [ ] Test each custom skill

### Phase 5: Data Migration (Day 12-13)
- [ ] Export chat_memories → OpenClaw MEMORY.md
- [ ] Export user whitelist → OpenClaw access config
- [ ] Verify memories accessible in OpenClaw
- [ ] Archive old SQLite DB

### Phase 6: Cutover (Day 13-14)
- [ ] Switch original Telegram bot token to OpenClaw
- [ ] Decommission old bot container
- [ ] Run `openclaw doctor` health check
- [ ] Monitor for 48 hours
- [ ] Remove parallel bot token from @BotFather
- [ ] Update `docker-compose.yml` to final state

### Phase 7: Cleanup (Day 14+)
- [ ] Remove old bot code from repo (archive to branch)
- [ ] Update CLAUDE.md with new architecture
- [ ] Update system_status_report.md
- [ ] Decommission K3s completely
- [ ] Clean up unused Docker images
- [ ] Add WhatsApp/Discord channels (stretch goal)

**Total estimated migration: 14 days**

---

## 10. Credentials Inventory

### 10.1 API Keys (Environment Variables)

| Credential | Current Location | OpenClaw Mapping |
|-----------|-----------------|-----------------|
| `TELEGRAM_BOT_TOKEN` | `.env` | OpenClaw channel config |
| `OPENAI_API_KEY` | `.env` + TokenBroker | OpenClaw LLM config |
| `GEMINI_API_KEY` | `.env` + TokenBroker | OpenClaw LLM config or skill secret |
| `PEXELS_API_KEY` | `.env` | Content Factory MCP env |
| `ELEVENLABS_API_KEY` | `.env` | Content Factory MCP env |
| `SUNO_API_KEY` | `.env` | Content Factory MCP env |
| `RUNWAY_API_KEY` | `.env` | Content Factory MCP env |
| `LUMA_API_KEY` | `.env` | Content Factory MCP env |
| `ANTHROPIC_API_KEY` | `.env` | OpenClaw LLM config (primary) |
| `INSTAGRAM_SESSION_ID` | `.env` / `accounts_config.json` | Content Factory MCP env |
| `TELEGRAM_ADMIN_CHAT_ID` | `.env` | OpenClaw notification config |

### 10.2 OAuth Tokens

| Token | Current Location | OpenClaw Mapping |
|-------|-----------------|-----------------|
| YouTube OAuth | `youtube_token.json` | Content Factory MCP volume |
| Google Calendar | `credentials.json` + token | Google Calendar skill config |
| Gmail | `gmail_credentials.json` + token | Gmail skill config |

### 10.3 Service Tokens

| Token | Current Location | OpenClaw Mapping |
|-------|-----------------|-----------------|
| Agent Mail bearer token | `.env` / hardcoded | OpenClaw MCP connection config |
| Home Assistant token | `ha_client.py` / `.env` | HA skill config |
| Proxmox credentials | `proxmox_manager.py` | Proxmox skill config |
| Linear API token | `.env` | Linear skill config |
| Notion token | `.env` | Notion skill config |
| ByBit API key/secret | `.env` (pending) | Not migrated (crypto bot separate) |

### 10.4 Security Note

The following were found hardcoded in source (should be moved to OpenClaw secrets):
- Agent Mail token in `factory_scheduler.py:82`
- Pexels fallback key in `daily_researcher.py:55`
- Allowed user IDs in `identity_orchestrator.py:64`

---

## 11. Architecture: Before & After

### Before (Current)

```
                        ┌─────────────────────────┐
                        │   ai_telegram_bot_v2.py  │
                        │   (4900+ lines, 55 cmds) │
                        │                          │
                        │  ┌───────────────────┐   │
    Telegram ◄──────────┤  │ InferenceClient   │   │
    (single channel)    │  │ (Gemini/OpenAI)   │   │
                        │  └───────────────────┘   │
                        │  ┌───────────────────┐   │
                        │  │ UserContextDB      │   │
                        │  │ (SQLite, ephemeral)│   │
                        │  └───────────────────┘   │
                        │  ┌───────────────────┐   │
                        │  │ Content Factory    │   │
                        │  │ (direct import)    │   │
                        │  └───────────────────┘   │
                        │  ┌───────────────────┐   │
                        │  │ HA / Calendar /    │   │
                        │  │ Gmail / Mashov     │   │
                        │  │ (all hand-rolled)  │   │
                        │  └───────────────────┘   │
                        └─────────────────────────┘
                              + zombie processes
                              + scheduler conflicts
                              + broken DB persistence
```

### After (OpenClaw)

```
    Telegram ──┐
    WhatsApp ──┤
    Discord ───┤──► ┌──────────────────────┐
    WebChat ───┤    │   OpenClaw Gateway    │
    Slack ─────┘    │   (Opus 4.6 LLM)     │
                    │                       │
                    │  Persistent Memory    │
                    │  Access Control       │
                    │  Cron Scheduler       │
                    │  Health Monitoring    │
                    │                       │
                    ├── Content Factory MCP ─────► ffmpeg + APIs
                    │   (video production)         (YouTube, IG, Threads)
                    │
                    ├── Google Calendar Skill ───► Google API
                    ├── Gmail Skill ────────────► Gmail Pub/Sub
                    ├── Home Assistant Skill ───► HA REST API
                    ├── MarkItDown MCP ─────────► Document conversion
                    ├── Agent Mail MCP ─────────► Postgres mail server
                    │
                    ├── Custom Skills:
                    │   ├── Mashov Homework
                    │   ├── Infrastructure Status
                    │   ├── Proxmox Control
                    │   ├── Morning Brief
                    │   └── Beads Task Manager
                    │
                    └── Behind Tailscale (no public exposure)
                        Sandbox enabled (no shell access)
```

---

## Appendix A: Files Referenced

| File | Path | Purpose |
|------|------|---------|
| Bot main | `Projects/AI_Core/src/ai_telegram_bot_v2.py` | Telegram bot (4900+ lines) |
| Bot DB | `Projects/AI_Core/src/user_context_db.py` | SQLite user database |
| RBAC | `Projects/AI_Core/src/rbac.py` | Role-based access control |
| Identity | `Projects/AI_Core/src/identity_orchestrator.py` | Auth + token management |
| HA controller | `Projects/AI_Core/src/ha_controller.py` | Home Assistant integration |
| Factory scheduler | `Projects/Content_Factory/src/pipeline/factory_scheduler.py` | Content production scheduler |
| Factory orchestrator | `Projects/Content_Factory/src/pipeline/orchestrator_v3_no_face.py` | Video assembly pipeline |
| Factory core | `Projects/Content_Factory/src/pipeline/ai_content_factory.py` | AI content integration layer |
| Researcher | `Projects/Content_Factory/src/researcher/daily_researcher.py` | Topic research + script gen |
| Production shipper | `Projects/Content_Factory/src/pipeline/production_shipper.py` | Multi-platform upload |
| Mail processor | `Scripts/Orchestration/mail_processor.py` | MCP mail intelligence |
| Docker Compose | `docker-compose.yml` | Service definitions |
| Status report | `system_status_report.md` | Known issues (2026-02-05) |
| System inventory | `system_inventory.md` | Hardware/software inventory |
| Network map | `consilium_map.json` | Tailscale node topology |
| Accounts config | `accounts_config.json` | Multi-account upload config |
| Intent ledger | `INTENT_LEDGER.yaml` | Agent coordination |

---

*Generated by migration analysis agent — 2026-02-07*
*Repository: Unified_System_Core @ branch claude/openclaw-migration-analysis-d1BRp*
