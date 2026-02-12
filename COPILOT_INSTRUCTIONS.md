# GitHub Copilot & AI Integration Instructions

## Overview

This document outlines how to use the advanced AI integrations available in Unified System Core.

### 1. Firebase MCP (Model Context Protocol)

We have enabled the Firebase MCP server to provide AI agents with direct access to Firebase projects.

**Setup in MCP Clients (e.g., Claude Desktop, Cursor):**
The configuration is located in `mcp_config.json` at the root of the repository.
Running `npx -y firebase-tools@latest mcp` starts the server.

**Capabilities:**

- Ask questions about Firebase project structure.
- Deploy functions or hosting sites via natural language (with confirmation).
- Retrieve Firestore data for debugging.

### 2. Gemini Code Assist

The Google Cloud AI Companion API (`cloudaicompanion.googleapis.com`) is enabled.

**IDE Setup:**

- Install the **Gemini Code Assist** extension for VS Code or IntelliJ.
- Sign in with your Google Cloud credentials.
- Select project: `my-home-435112`.

**Features:**

- Code completion and generation.
- Chat with your codebase context.
- Unit test generation (`/tests`).

### 3. VirusTotal Security Scanning

We prioritize security in our AI agent releases.

**Release Workflow:**
Before deploying a new agent version or skill, run the security scanner:

```bash
python3 scripts/security/scan_release.py <path_to_agent_code>
```

**What it does:**

1. Packages the directory into a deterministic ZIP.
2. Computes the SHA-256 hash.
3. Checks VirusTotal for existing scans.
4. Generates a link for manual upload/verification if new.

**Policy:**

- Do NOT deploy if VirusTotal flags any malicious behavior.
- Review "Code Insight" summaries for unexpected capabilities.

### 4. Notion Integration

The `NotionClient` in `Projects/AI_Core/src/notion_service.py` allows the bot to:

- Create task pages.
- Log research notes.
- Search the knowledge base.

**Configuration:**

- `NOTION_API_KEY`: Set in `.env`.
- `NOTION_DATABASE_ID`: Set in `.env`.

**Usage:**
The bot automatically logs complex tasks to Notion if configured.

---
*Last Updated: 2026-02-12*
