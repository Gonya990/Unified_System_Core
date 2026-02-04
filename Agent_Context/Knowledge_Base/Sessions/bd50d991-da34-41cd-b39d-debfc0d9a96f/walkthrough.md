# Walkthrough: Telegram Bot Recovery & API Key Sync

> **Date:** 2026-02-04
> **Session:** bd50d991-da34-41cd-b39d-debfc0d9a96f

## Summary

Successfully restored the AI Telegram Bot (v2) to operational status by
resolving token invalidation and environment configuration issues. Verified
connectivity to all core services and synchronized the shared codebase across
all active nodes.

## Changes Made

1. **Environment Configuration**:
   - Updated `.env` in `AI_Core` with verified tokens for Telegram, Gemini,
     OpenRouter, and Pexels.
   - Set `DISABLE_FIRESTORE=true` to bypass failing Google Cloud JWT
     authentication, falling back to stable local SQLite.

2. **Project Structure**:
   - Updated `pyproject.toml` to include 12+ missing dependencies (fastapi,
     google-cloud-firestore, etc.).
   - Verified that `uv sync` correctly installs the environment on the cloud server.

3. **Orchestration**:
   - Ran `vibranium-sync.sh` to propagate changes.
   - Restarted `bot-v2` and `crypto-bot` on `unified-home-core-cloud` using PM2.

4. **Cleanup**:
   - Terminated legacy Chromium/Playwright processes that were consuming
     resources on the cloud node.

## Verification

- [x] Bot is "ONLINE" in PM2.
- [x] Logs show successful `getUpdates` and command registration.
- [x] Health server is reachable on port 8095.

## Next Steps

- Investigate the root cause of the Google Cloud JWT signature failure
  (likely service account key rotation).
- Address the 134 linting warnings reported by the sync script.
