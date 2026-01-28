# Rental Finder MCP Servers

MCP-based architecture for finding rental apartments across Israeli platforms: **Yad2**, **Madlan**, and **Facebook Groups**.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    Claude / LLM Agent                            │
│   • Understands your preferences                                 │
│   • Queries all sources in parallel                              │
│   • Deduplicates across platforms (same listing on Yad2+Madlan)  │
│   • Scores and ranks results                                     │
│   • Monitors for new listings                                    │
└──────────────────────────────────────────────────────────────────┘
                              │ MCP Protocol
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  yad2-mcp     │    │  madlan-mcp   │    │ fb-groups-mcp │
│   server      │    │   server      │    │   server      │
│   Port 3001   │    │   Port 3002   │    │   Port 3003   │
└───────────────┘    └───────────────┘    └───────────────┘
```

## Why MCP Instead of Heavy Automation?

1. **Separation of concerns**: MCP servers just fetch data, LLM handles intelligence
2. **Composability**: Easy to add new sources (Homeless, WinWin, etc.)
3. **No brittle selectors**: Use JSON APIs where available, fallback to HTML parsing
4. **LLM-powered deduplication**: Same apartment posted on multiple sites gets merged
5. **Natural language preferences**: "3-room apartment in central Tel Aviv, prefer high floor, budget 8000"

## Quick Start

### Prerequisites
- Node.js 20+
- npm or pnpm

### Installation

```bash
# Yad2 MCP Server
cd yad2-mcp-server
npm install
npm run build

# Madlan MCP Server
cd ../madlan-mcp-server
npm install
npm run build
```

### Running (stdio mode - for Claude Desktop / MCP clients)

```bash
# Yad2
cd yad2-mcp-server && node dist/index.js

# Madlan
cd madlan-mcp-server && node dist/index.js
```

### Running (HTTP mode - for self-hosted agents)

```bash
TRANSPORT=http PORT=3001 node dist/index.js  # Yad2
TRANSPORT=http PORT=3002 node dist/index.js  # Madlan
```

## Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "yad2": {
      "command": "node",
      "args": ["/path/to/yad2-mcp-server/dist/index.js"]
    },
    "madlan": {
      "command": "node", 
      "args": ["/path/to/madlan-mcp-server/dist/index.js"]
    }
  }
}
```

## Available Tools

### yad2-mcp-server

| Tool | Description |
|------|-------------|
| `yad2_search_rentals` | Search Yad2 rental listings with filters |
| `yad2_get_listing` | Get detailed info for a specific listing |

### madlan-mcp-server

| Tool | Description |
|------|-------------|
| `madlan_search_rentals` | Search Madlan rentals with filters |
| `madlan_get_listing` | Get detailed info including Madlan valuations |

## Example Queries (Natural Language to Claude)

```
"Find me 3-room apartments for rent in Tel Aviv under 8000 NIS"

"Search both Yad2 and Madlan for rentals in Haifa, 
 deduplicate results, and show me the best deals"

"Monitor for new 2-room apartments in Ramat Gan, 
 alert me when something under 5000 NIS appears"
```

## Facebook Groups - Approach

Facebook requires authentication and has strong anti-bot measures. Options:

### Option 1: Browser Extension (Recommended for Personal Use)
Use a browser extension that scrapes FB groups while you're logged in and exports to JSON.

### Option 2: Playwright with Persistent Profile
```typescript
// fb-groups-mcp would use Playwright with a saved login session
const browser = await chromium.launchPersistentContext(
  '/path/to/fb-profile',
  { headless: false }
);
```

### Option 3: Facebook Graph API (Limited)
Only works for groups you admin, not general rental groups.

### Implementation Notes

Due to FB's complexity, I recommend:
1. Start with Yad2 + Madlan (covers 80% of listings)
2. For FB groups, use a simple Playwright script that:
   - Opens group in browser with your logged-in profile
   - Scrolls and extracts posts
   - Filters for rental-related keywords
   - Exports to JSON that the MCP server can read

## Extending

### Adding a New Source

1. Create `{source}-mcp-server/` directory
2. Copy package.json and tsconfig.json
3. Implement:
   - `search_rentals` tool with common filter params
   - `get_listing` tool for details
   - Normalize output to common `Listing` interface

### Common Listing Interface

```typescript
interface Listing {
  id: string;
  source: 'yad2' | 'madlan' | 'facebook' | 'homeless';
  price: number;
  city: string;
  neighborhood?: string;
  street?: string;
  rooms: number;
  floor: number;
  squareMeters: number;
  dateAdded: string;
  url: string;
  images: string[];
  description?: string;
}
```

## Deployment Options

### Local (Claude Desktop)
Best for personal use - runs on your machine via stdio.

### Self-Hosted (K3s)
Deploy as HTTP services in your cluster:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yad2-mcp
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: yad2-mcp
        image: your-registry/yad2-mcp-server:latest
        env:
        - name: TRANSPORT
          value: "http"
        - name: PORT
          value: "3001"
        ports:
        - containerPort: 3001
```

### Scheduled Monitoring
Use a cron job or K8s CronJob to periodically:
1. Query all sources
2. Compare against previous results
3. Send notifications for new listings (Telegram, email, etc.)

## API Reverse Engineering Notes

### Yad2
- Main API: `https://gw.yad2.co.il/feed-search-legacy/realestate/rent`
- Detail API: `https://gw.yad2.co.il/feed-search-legacy/item/{token}`
- No auth required, returns JSON directly
- Rate limits: ~60 req/min (be respectful)

### Madlan
- Uses Next.js with SSR
- Data embedded in `__NEXT_DATA__` script tag
- Some API endpoints at `/api2/*`
- More aggressive rate limiting

## Legal Notice

This tool scrapes publicly available data for personal use. Be respectful of rate limits and terms of service. Do not use for commercial purposes without proper licensing.

## Contributing

PRs welcome! Priority areas:
- [ ] Facebook Groups MCP server
- [ ] Homeless.co.il integration
- [ ] WinWin.co.il integration
- [ ] Notification service (Telegram bot)
- [ ] Deduplication heuristics
