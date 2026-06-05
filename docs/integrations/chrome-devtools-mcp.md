# Chrome DevTools MCP (Cursor / Unified Core)

Official MCP server: [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp). Gives agents live Chrome control via DevTools (network, console, performance traces, Puppeteer automation).

**DevTools 147 (RU):** [Что нового в DevTools 147](https://developer.chrome.com/blog/new-in-devtools-147?utm_source=devtools&utm_campaign=stable&hl=ru) — MCP skills, AI assistance panel, trace sharing.

## Install

Requirements: Node.js ≥ 20.19, npm, **Google Chrome** stable (or Chrome for Testing).

Monorepo clone (optional, for skills / pinned dev):

```bash
cd /Users/igorgoncharenko/Documents/Unified_System_Core/tools/chrome-devtools-mcp
git pull
npm ci && npm run build
```

Cursor uses **npx** (no local build required). Version pinned in [`.cursor/mcp.json`](../../.cursor/mcp.json).

Global VS Code MCP (user): `~/.vscode/mcp.json` — entry `io.github.ChromeDevTools/chrome-devtools-mcp` (may differ from project pin; prefer repo `.cursor/mcp.json` for Unified Core work).

## MacBook Air — Chrome apps

| App | Path |
|-----|------|
| Google Chrome (stable) | `/Applications/Google Chrome.app` |
| Chrome for Developers (PWA) | `~/Applications/Chrome Apps.localized/Chrome for Developers.app` |

MCP launches stable Chrome by default. For Canary/dev channel: add `--channel=canary` (or `beta` / `dev`) to `args` in `mcp.json`.

## Cursor reload

After editing `.cursor/mcp.json`:

1. **Cursor Settings → MCP** — confirm `chrome-devtools` is listed and enabled.
2. **Developer: Reload Window** (or restart Cursor).
3. In Agent chat, verify MCP tools (e.g. `navigate_page`, `take_snapshot`) appear for the session.

## Config (project)

See [`.cursor/mcp.json`](../../.cursor/mcp.json) — `chrome-devtools` alongside `unified-openclaw`.

Local alternative (after `npm run build` in `tools/chrome-devtools-mcp`):

```json
"chrome-devtools": {
  "command": "node",
  "args": [
    "/Users/igorgoncharenko/Documents/Unified_System_Core/tools/chrome-devtools-mcp/build/src/index.js",
    "--no-usage-statistics"
  ]
}
```

## When to use vs Playwright MCP

| Use **chrome-devtools-mcp** | Use **@playwright/mcp** |
|-----------------------------|-------------------------|
| Real Chrome + DevTools (traces, CrUX, console source maps) | Cross-browser E2E (Chromium/Firefox/WebKit) |
| Debugging a page you already have open (`--autoConnect`, port 9222) | CI-style flows, test codegen |
| Performance insights (LCP, network waterfall in DevTools) | Fixture-based automation without DevTools UI |

Playwright MCP is configured in `~/.vscode/mcp.json` as `microsoft/playwright-mcp`; Unified Core Cursor project does not enable it by default.

## Sovereign / privacy note

- MCP clients receive **browser contents** (URLs, DOM, cookies context, network bodies). Treat as **local dev only** — no production accounts, banking, or personal tabs.
- Usage statistics to Google are **disabled** in project config (`--no-usage-statistics`, `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS`).
- Performance tools may still contact **CrUX** unless `--no-performance-crux` is set; disable if traces must not leave the machine.
- Registered in [cloud_vendors.yaml](../../Agent_Context/Knowledge_Base/identity/cloud_vendors.yaml) under `dev_tools`.

## Test

```bash
npx -y chrome-devtools-mcp@0.16.0 --no-usage-statistics --help
```

Smoke (stdio, 5s timeout — expect no crash):

```bash
timeout 5 npx -y chrome-devtools-mcp@0.16.0 --no-usage-statistics 2>&1 | head -5 || true
```

## Related docs

- Legacy walkthrough (Russian): [docs/Tools/CHROME_DEVTOOLS_MCP.md](../Tools/CHROME_DEVTOOLS_MCP.md)
- Skills path: `tools/chrome-devtools-mcp/skills/chrome-devtools/`
- OpenClaw bridge: [docs/architecture/cursor-openclaw-mcp.md](../architecture/cursor-openclaw-mcp.md)
