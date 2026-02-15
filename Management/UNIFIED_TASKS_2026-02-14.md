# Unified Tasks - System Wide

Triaged: 2026-02-15

Scope: Content Factory pipeline + infra. Legacy/irrelevant items removed.

## Active Tasks

- [x] Prioritize ElevenLabs TTS and add provider/voice rotation in orchestrators.
- [x] Sync ElevenLabs key into TokenBroker (local + remote).
- [x] Start Flux/SDXL servers under PM2 on `unified-home-core-cloud`.
- [ ] Accept gated access for `black-forest-labs/FLUX.1-schnell` (HF token set), then verify `http://localhost:8081/`.
- [x] SDXL model ready and `http://localhost:8188/` responding.
- [x] Add HF Inference fallback + model rotation (daily_researcher).
- [x] Install `huggingface_hub` on remote.
- [x] Set HF env for Content Factory (HF_TOKEN/HF_PROVIDER/HF_FLUX_MODELS/ALLOW_HF_REMOTE).
- [x] Set PM2 env for Content Factory:
  `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_IDS`, `ELEVENLABS_VOICE_ROTATION=random`,
  `TTS_ROTATION=elevenlabs,edge`, `ALLOW_OPENAI_TTS=false`.
- [x] Restart `content-factory` + `content-factory-turbo` to apply env.
- [ ] Confirm new run uses ElevenLabs first (no OpenAI TTS calls). `TTS_ROTATE_ORDER=false` applied.
- [x] Set `YOUTUBE_TOKEN_FILES` in PM2 env (Unified System + Gonya Goncharenko).
- [ ] Verify uploads go to both channels in parallel (code supports; pending live upload).
- [ ] Verify HF Inference path produces images (current 403 from HF provider; needs permissions).
- [ ] Fix Flux local model gating + disk space (~24 GB required; ~14.5 GB free).
