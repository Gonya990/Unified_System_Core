# Walkthrough: Unified Cloud Node Migration (100.87.208.56)

> **Date:** 2026-01-27
> **Session:** 2026-01-27_cloud_ip_migration

## Summary

The cloud node `unified-home-core-cloud` changed its Tailscale IP to `100.87.208.56`. This session focused on updating all system configurations and documentation to restore orchestration and monitoring capabilities.

## Changes Made

1. **System Config**: Updated `config/nodes.yaml` to point `unified-home-core` to the new IP.
2. **Network Map**: Updated `Agent_Context/Infrastructure/TAILSCALE_NETWORK_MAP.md` with the current IP and validated node roles.
3. **Operations Runbook**: Patched `infra/OPS_RUNBOOK.md` so that all emergency SSH commands and health checks use the active IP.
4. **Agent Status**: Updated `01_Projects/PRJ-007_Digital_Assistant_MVP/01_Docs/AGENTS_STATUS_2026-01-09.md` to restore the correct n8n dashboard link.

## Verification

- **n8n**: Confirmed reachable at `http://100.87.208.56:5678`. Encountered "Secure Cookie" warning, which requires either HTTPS via `tailscale cert` or setting `N8N_SECURE_COOKIE=false`.
- **MCP Mail**: Confirmed reachable on port `8765`. `/health` endpoint returned `Unauthorized` JSON, confirming the service is active and protected.
- **Diagnostics**: Connectivity to the new IP verified via browser subagent.

## Next Steps

- **Certificate Update**: Run `tailscale cert` on the cloud node to enable secure HTTPS access for n8n.
- **SSH Connectivity**: Troubleshoot local "Operation not permitted" errors when initiating SSH from the Mac environment.
- **Gmail Sync**: Proceed with OAuth2 verification as per user request.
