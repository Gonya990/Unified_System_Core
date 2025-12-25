# Shared Knowledge Base

This directory contains files that are indexed and accessible by **all agents** in the Unified System.

## What Belongs Here

- Cross-agent protocols and agreements
- Shared architecture decisions
- Global task board exports
- System-wide configurations (non-sensitive)

## What Does NOT Belong Here

- Agent-specific session data (use `Sessions/<uuid>/`)
- Personal credentials or `.env` files
- Machine-specific configurations (use `machines/<hostname>/`)

## Privacy Rule

Before adding files here, ensure they contain no:
- API keys or tokens
- Personal identifying information
- Machine-specific paths or credentials

See `AGENT_ONBOARDING.md` for full integration guidelines.
