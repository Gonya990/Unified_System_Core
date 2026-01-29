# Task: Cloud IP Migration & Connectivity Fix

## Phase 1: Diagnostics <!-- id: 100 -->

- [x] Initial check of `unified-home-core-cloud.ayu-altair.ts.net` <!-- id: 101 -->
- [x] Discovery of new IP `100.87.208.56` <!-- id: 102 -->

## Phase 2: Implementation <!-- id: 200 -->

- [x] Update `config/nodes.yaml` with new IP <!-- id: 201 -->
- [x] Update `Agent_Context/Infrastructure/TAILSCALE_NETWORK_MAP.md` <!-- id: 202 -->
- [x] Update `infra/OPS_RUNBOOK.md` <!-- id: 203 -->
- [x] Update `AGENTS_STATUS_2026-01-09.md` <!-- id: 204 -->

## Phase 3: Verification <!-- id: 300 -->

- [x] Verify n8n accessibility via browser <!-- id: 301 -->
- [x] Verify MCP Mail health endpoint via browser <!-- id: 302 -->
- [ ] Stabilize SSH connectivity (Blocked: macOS Sandbox - needs restart) <!-- id: 303 -->
- [ ] Fix n8n Secure Cookie (Blocked: No SSH) <!-- id: 304 -->
- [ ] Sync Git (Blocked: DNS/Net Unreachable) <!-- id: 305 -->
