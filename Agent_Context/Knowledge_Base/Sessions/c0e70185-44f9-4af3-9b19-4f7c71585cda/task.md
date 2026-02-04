# Task: Fixing AI Telegram Bot <!-- id: 100 -->

## Phase 1: Dependency & Build Fixes <!-- id: 200 -->

- [x] Fix `pytz` ModuleNotFoundError <!-- id: 201 -->
- [x] Fix `google-auth-oauthlib`, `jinja2`, `uvicorn` missing dependencies
  <!-- id: 202 -->
- [x] Simplify `requirements.txt` versions to avoid conflicts <!-- id: 203 -->
- [x] Fix Docker build context to include `External_Tools/Stack/agent_mail_sdk`
  <!-- id: 204 -->

## Phase 2: Operations & Access <!-- id: 300 -->

- [x] Update Tailscale ACLs for SSH access <!-- id: 301 -->
- [x] Fix `update_k8s_secrets.sh` permissions (sudo) <!-- id: 302 -->
- [x] Update Kubernetes Secrets with valid tokens <!-- id: 303 -->
- [x] Resolve `Conflict 409` (Revoke/Replace Token) <!-- id: 304 -->
- [x] Verify Bot Status (Running & Polling) <!-- id: 305 -->
