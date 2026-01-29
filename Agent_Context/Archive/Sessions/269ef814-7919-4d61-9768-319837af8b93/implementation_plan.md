# Project Omni-Tool Implementation Plan

## Goal Description

Build a unified "Omni-Tool" MCP Server (`omni_server.py`) that acts as a central intelligence hub.
Unifies:

1. **AI Council**: Parallel consensus from GPT-4, Claude, and Gemini (via OpenRouter).
2. **Google Workspace**: RAG access to Drive/Docs.
3. **App Store Connect**: Automation for asset uploads.
4. **Multi-Interface**: Supports MCP (IDE), CLI (Termius), and Siri (Voice/Shortcuts).

## Architecture

- **Language**: Python 3.11+
- **Core Libs**: `mcp[fastmcp]`, `httpx`, `asyncio`, `google-api-python-client`, `pyjwt`, `cryptography`
- **Location**: `/Users/macbook/.gemini/antigravity/playground/solar-curie/omni-tool`

## Proposed Changes

### 1. Project Setup

- Create directory `omni-tool`.
- Create `requirements.txt` with optimized dependencies (lazy loading where possible).
- Create `.env.example` for keys (OPENROUTER, GOOGLE_CREDS, APPLE_KEYS).

### 2. `omni_server.py`

The monolith script handling all logic.

- **Modes**:
  - `python omni_server.py`: Starts MCP Server (FastMCP).
  - `python omni_server.py "query"`: Runs CLI mode (Markdown output).
  - `python omni_server.py "query" --siri`: Runs Siri mode (Plain text output).

- **Modules**:
  - **AI Council**:
    - `consult_council`: Async calls to OpenRouter.
    - `System Prompt`: Context-aware (iOS/Swift).
    - `Tiering`: Cheap vs Pro based on keywords.
    - `Timeout`: 15s hard limit using `asyncio.wait_for`.
  - **Google Workspace**:
    - `search_drive`: Cached search.
    - `read_doc`: Cached content retrieval.
    - Auth: Service Account.
  - **App Store Connect**:
    - `upload_asset`: 3-step upload protocol (Reserve -> Upload Binary -> Commit).
    - Auth: JWT generation with `.p8` key.

### 3. Usage Artifacts

- **Termius**: One-liner bash snippet for SSH execution.
- **MCP Config**: JSON snippet for Antigravity registration.
- **Siri**: Markdown guide for iOS Shortcuts setup.

## Verification Plan

- **Mock Testing**: Since I don't have user's actual API keys, I will implement the logic and ensure it runs/compiles.
- **Mode Verification**:
  - Run server mode (dry run).
  - Run CLI mode with dummy query (expect Markdown).
  - Run Siri mode with dummy query (expect Plain Text).
