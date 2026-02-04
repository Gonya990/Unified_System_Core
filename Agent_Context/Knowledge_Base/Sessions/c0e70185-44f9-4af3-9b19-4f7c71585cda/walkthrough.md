# Walkthrough: AI Telegram Bot Repair

> **Date:** 2026-02-04
> **Session:** c0e70185-44f9-4af3-9b19-4f7c71585cda

## Summary

Successfully restored the AI Telegram Bot service on `unified-home-core-cloud`.
The bot was failing due to missing dependencies, build context issues, and a
token conflict with a ghost instance.

## Changes Made

1. **Dependencies**: Added `pytz`, `google-auth-oauthlib`, `jinja2`, `uvicorn`,
   `PyYAML`, and others to `requirements.txt`. Relaxed version constraints.
2. **Docker Build**: Updated `Dockerfile` and GitHub Workflow to use the
   repository root context. This ensures `External_Tools/Stack/agent_mail_sdk`
   is correctly copied into the container.
3. **Kubernetes**:
    * Updated `update_k8s_secrets.sh` to use `sudo` for accessing k3s config.
    * Replaced the Telegram Bot Token in Kubernetes Secrets to resolve a conflict.
4. **Access**: Updated Tailscale ACLs to allow SSH access for tagged devices.

## Verification

* [x] **Build**: Docker image builds successfully in GitHub Actions.
* [x] **Deploy**: Kubernetes deployment `ai-telegram-bot` is in `Running` state.
* [x] **Logs**: Logs show `Application started` and successful polling (`getUpdates`).
* [x] **Network**: SSH access to `unified-home-core-cloud` is verified.

## Next Steps

* Monitor bot stability.
* Ensure `External_Tools` remains synced on the build server.
