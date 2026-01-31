# Task: Troubleshooting AI Bot & HA Integration

## Phase 1: Diagnose & Fix AI Core (Ollama) <!-- id: 100 -->

- [x] Check Ollama service status on remote node (igor-gaming-1) <!-- id: 101 -->
- [x] Resolve "port 11434 occupied" conflict <!-- id: 102 -->
- [x] Fix container environment variables (OLLAMA_BASE_URL) <!-- id: 103 -->
- [x] Verify connectivity from bot container to host <!-- id: 104 -->

## Phase 2: Fix Home Assistant Integration <!-- id: 200 -->

- [x] Diagnose "ImportError: No module named ha_client" inside container <!-- id: 201 -->
- [x] Create and apply `ha_controller_fix.py` to handle import paths correctly <!-- id: 202 -->
- [x] Verify HA client initialization success in logs <!-- id: 203 -->
- [x] Apply fix to local repository for persistence <!-- id: 204 -->

## Phase 3: Network & Stability <!-- id: 300 -->

- [x] Resolve "Telegram Conflict 409" by killing zombie processes <!-- id: 301 -->
- [x] Install `iputils-ping` in Docker container to fix `/status` command <!-- id: 302 -->
- [x] Update `Dockerfile` locally to include network tools for future builds <!-- id: 303 -->
- [x] Verify full system status (AI + HA + Network) <!-- id: 304 -->

<!-- CURRENT FOCUS -->
