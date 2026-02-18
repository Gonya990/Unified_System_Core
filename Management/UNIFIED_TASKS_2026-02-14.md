# Unified Tasks - System Wide

Triaged: 2026-02-15

Scope: Content Factory pipeline + infra. Legacy/irrelevant items removed.

## Active Tasks

- [x] Switch longform scripts to Gemini-first with OpenAI fallback.
- [x] Make Gemini/Vertex primary for images (`PREFER_LOCAL_IMAGES=false`).
- [ ] Restore SDXL local fallback: install deps in `/home/gonya/ai_models/.venv`
  (torch/diffusers/fastapi/uvicorn/Pillow) and download SDXL weights (disk
  impact).
- [x] Prioritize ElevenLabs TTS and add provider/voice rotation in
  orchestrators.
- [x] Sync ElevenLabs key into TokenBroker (local + remote).
- [x] Start Flux/SDXL servers under PM2 on `unified-home-core-cloud`
  (PM2 resurrected).
- [ ] Accept gated access for `black-forest-labs/FLUX.1-schnell` (HF token set).
  Flux server still gated.
- [ ] SDXL server currently errored (missing torch/deps in
  `/home/gonya/ai_models/.venv`).
- [x] Add HF Inference fallback + model rotation (daily_researcher).
- [x] Install `huggingface_hub` on remote.
- [x] Set HF env for Content Factory (HF_TOKEN/HF_PROVIDER/HF_FLUX_MODELS/
  ALLOW_HF_REMOTE).
- [x] Set PM2 env for Content Factory:
  `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_IDS`, `ELEVENLABS_VOICE_ROTATION=random`,
  `TTS_ROTATION=elevenlabs,edge`, `ALLOW_OPENAI_TTS=false`.
- [x] Restart `content-factory` + `content-factory-turbo` to apply env.
- [x] Confirm new run uses ElevenLabs first (no OpenAI TTS calls).
  `TTS_ROTATE_ORDER=false` applied; direct ElevenLabs test OK.
- [x] Set `YOUTUBE_TOKEN_FILES` in PM2 env (Unified System + Gonya Goncharenko).
- [ ] Verify uploads go to both channels in parallel (code supports;
  pending live upload).
- [ ] Verify HF Inference path produces images (still 403; HF token needs
  Inference Providers permission).
- [x] Fix Flux local model disk space (freed cache/checkpoints; ~25 GB free now).
- [ ] Fix Flux local model gating (still blocked by HF access approval).

- [x] Fix `ai-bot-igor` Telegram token (PM2). API_PORT moved to 8085 to avoid conflict.
- [x] Fix `ai-telegram-bot` in k8s (pods evicted; node DiskPressure).
- [x] Sync TokenBroker vault (`~/.config/unified-system/tokens.yaml`) to remote.
- [/] Fix cloud server disk space (moving `broll` to `/mnt/data`).
