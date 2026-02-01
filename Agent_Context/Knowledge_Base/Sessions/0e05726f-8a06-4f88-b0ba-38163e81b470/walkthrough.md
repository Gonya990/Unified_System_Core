# Walkthrough: AntiBridge Backend Troubleshooting & macOS Fixes

> **Date:** 2026-02-01
> **Session:** 0e05726f-8a06-4f88-b0ba-38163e81b470

## Summary

The AntiBridge backend (Web Control for Antigravity) was failing to start on macOS due to missing dependencies and Windows-specific environment variables. This task involved installing packages and patching the source code to be cross-platform.

## Changes Made

### 1. **Backend Dependencies**

- Ran `npm install` in `Projects/AI_Core/antibridge/backend` to resolve `MODULE_NOT_FOUND` (missing `express`, `ws`, etc.).

### 2. **Cross-Platform Compatibility**

- **File:** `services/ConversationWatcher.js`
- **File:** `routes/response.js`
- **File:** `services/AntigravityBridge.js`
- **Action:** Replaced `process.env.USERPROFILE` with `(process.env.HOME || process.env.USERPROFILE)` to ensure the home directory is correctly resolved on macOS.
- **Tools:** Used `sed` for mass-patching the source files.

### 3. **Server Initialization**

- Successfully started the Express & WebSocket server on port `8000`.
- Verified the server is reachable and database is initialized.

## Verification

- [x] `npm run start` completes without errors.
- [x] WebSocket server logs "AntiBridge v1.2.0 - Web Control" and displays local/network IPs.
- [x] Confirmed directory `~/.gemini/antigravity/conversations` exists and is accessible by the watcher.

## Next Steps

- **MacOS Automation Fixes**: Adapt Windows-specific automation commands (`powershell`, `clip`, `mouse_event`) to macOS equivalents (`pbcopy`, `pbpaste`, `AppleScript`).
- **Frontend Integration**: Verify the frontend can connect to the running backend.
- **GPU Council Indexing**: Continue monitoring the 80GB deep scan progress (currently at 30%).
