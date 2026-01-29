# Unified System - Roadmap & Plan

## ✅ Completed Today (2026-01-11)

### Content Factory

- [x] Migrated to "Peace & Tech" theme (no war/politics)
- [x] Switched voice to `alloy` (neutral, no accent)
- [x] Adopted "Nikolashin Style" (Listicle + Warning Hooks)
- [x] Uploaded Russian video: <https://youtu.be/laiFlnGCyRQ>
- [x] Uploaded English video: <https://youtu.be/g7m02YjRlE0>
- [x] Fixed Instagram uploads (patched instagrapi types.py)
- [x] Added unique segment prefixes to prevent parallel run collisions
- [x] Migrated to OpenAI Responses API (with Chat Completions fallback)

### ChatKit Dashboard (In Progress)

- [x] Created Next.js 15 project structure
- [x] Built premium dark theme UI
- [x] Integrated OpenAI Responses API
- [ ] Install dependencies & launch

---

## 🔜 Next Steps

### 1. ChatKit Dashboard Launch

```bash
cd /Users/macbook/Documents/Unified_System/Projects/ChatKit_Dashboard
npm install
npm run dev
# Open http://localhost:3001
```

### 2. Browser Automation for Threads (Playwright)

**Why:** Official Threads API doesn't exist. `threads-api` library is unstable.
**Solution:** Use Playwright for headless browser automation.

**Setup Plan:**

```bash
# Install
pip install playwright
playwright install chromium

# Structure
/Projects/Content_Factory/src/uploaders/
  └── threads_browser.py  # Playwright-based Threads poster
```

**threads_browser.py Logic:**

1. Login via saved browser state (cookies)
2. Navigate to threads.net
3. Compose new post
4. Attach media (optional)
5. Submit post
6. Verify success

**Estimated Time:** 30-45 minutes implementation

### 3. Telegram Notification Integration

- Send YouTube/Instagram links to Telegram after upload
- Use existing `ai_telegram_bot_v2.py` infrastructure

### 4. Automatic Thumbnail Generation

- Generate thumbnails from video frames + title overlay
- Use PIL/Pillow or ffmpeg

---

## 📊 System Status

| Component | Status | Notes |
|-----------|--------|-------|
| Content Factory | ✅ Online | Peace/Tech theme active |
| Instagram Uploads | ✅ Working | Patched instagrapi |
| YouTube Uploads | ✅ Working | OAuth configured |
| Threads | ⚠️ Needs Browser Automation | API blocked by Meta |
| ChatKit Dashboard | 🔄 Building | Next.js 15 |
| Telegram Bot | ✅ Online | Running on server |

---

## 🔧 Technical Debt

1. **Gemini Deprecation Warning** - Migrate from `google.generativeai` to `google.genai`
2. **Cleanup old temp files** on server after video production
3. **Add monitoring/alerting** for failed uploads
