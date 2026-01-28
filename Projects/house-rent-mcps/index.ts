import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";
import axios, { AxiosError } from "axios";
import { z } from "zod";

// ============================================================================
// Constants & Types
// ============================================================================


const YAD2_API_BASE = "https://gw.yad2.co.il/feed-search-legacy/realestate/rent";

interface Yad2Listing {
  [key: string]: unknown; // Index signature for structuredContent compatibility
  id: string;
  token: string;
  title?: string;
  price: number;
  city: string;
  neighborhood?: string;
  street?: string;
  rooms: number;
  floor: number;
  squareMeters: number;
  dateAdded: string;
  images: string[];
  description?: string;
  contactName?: string;
  contactPhone?: string;
  url: string;
}

interface Yad2ApiResponse {
  feed: {
    feed_items: Yad2FeedItem[];
    total_items: number;
    current_page: number;
    total_pages: number;
  };
}

interface Yad2FeedItem {
  id: string;
  token: string;
  title_1?: string;
  title_2?: string;
  price: string;
  city: string;
  neighborhood?: string;
  street?: string;
  Rooms_text?: string;
  floor_text?: string;
  SquareMeter?: string;
  date_added?: string;
  images?: { src: string }[];
  feed_source?: string;
  row_4?: string;
  contact_name?: string;
  merchant?: boolean;
}

// ============================================================================
// API Client
// ============================================================================

import { addExtra } from 'puppeteer-extra';
import vanillaPuppeteer from 'puppeteer-core';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import { execSync } from 'child_process';

const puppeteer = addExtra(vanillaPuppeteer);
puppeteer.use(StealthPlugin());

// Mobile User Agent for better stealth
const USER_AGENT = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36";

import * as fs from 'fs';

function logToFile(msg: string) {
  fs.appendFileSync('yad2_internal.log', `${new Date().toISOString()} - ${msg}\n`);
}

let globalBrowser: ReturnType<typeof vanillaPuppeteer.launch> | null = null;
let globalPage: any = null;

async function getBrowser() {
  if (globalBrowser) {
    try {
      const b = await globalBrowser;
      if (b.isConnected()) return b;
    } catch (e) {
      logToFile("Browser disconnected, recreating...");
    }
  }

  let chromePath = '';
  try {
    try {
      chromePath = execSync('which chromium').toString().trim();
    } catch {
      chromePath = execSync('which google-chrome-stable').toString().trim();
    }
  } catch (e) {
    logToFile("Could not find chromium or google-chrome-stable " + e);
    throw new Error("Browser executable not found");
  }

  logToFile("Launching persistent browser session...");
  globalBrowser = (puppeteer.launch({
    headless: false,
    executablePath: chromePath,
    userDataDir: './yad2-session-data', // Persist cookies/localstorage
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-blink-features=AutomationControlled'
    ]
  }) as any);

  return globalBrowser;
}

async function getPage() {
  const browser = await getBrowser();
  if (globalPage) {
    try {
      if (!globalPage.isClosed()) return globalPage;
    } catch (e) {
      logToFile("Global page check failed, recreating...");
    }
  }

  globalPage = await (browser as any).newPage();
  await globalPage.setUserAgent(USER_AGENT);
  await globalPage.setViewport({ width: 375, height: 812, isMobile: true, hasTouch: true });

  // Warm up home page once
  logToFile("Warming up session on homepage...");
  await globalPage.goto("https://www.yad2.co.il/", { waitUntil: 'networkidle2', timeout: 30000 });

  return globalPage;
}

// Scrape Listings from Next Data
async function searchYad2Rentals(params: {
  city?: string;
  priceMin?: number;
  priceMax?: number;
  roomsMin?: number;
  roomsMax?: number;
  page?: number;
}): Promise<{ listings: Yad2Listing[]; totalItems: number; totalPages: number; currentPage: number }> {
  logToFile("Starting Yad2 Search via Puppeteer...");
  const page = await getPage();

  try {
    let basePath = "/realestate/rent";
    if (params.city) {
      // Remove spaces for the path or keep them? Yad2 usually replaces spaces with dashes or just uses encoded spaces.
      // Let's try encoded city name in path.
      basePath += `/${encodeURIComponent(params.city)}`;
    }

    const queryParts: string[] = [];
    if (params.priceMin) queryParts.push(`price=${params.priceMin}-1000000`);
    if (params.priceMax) queryParts.push(`price=${params.priceMin || 0}-${params.priceMax}`);
    if (params.roomsMin || params.roomsMax) queryParts.push(`rooms=${params.roomsMin || 1}-${params.roomsMax || 12}`);
    if (params.page && params.page > 1) queryParts.push(`page=${params.page}`);

    const searchUrl = `https://www.yad2.co.il${basePath}${queryParts.length ? '?' + queryParts.join('&') : ''}`;
    logToFile("Navigating to: " + searchUrl);

    await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });

    if (await page.title() === "ShieldSquare Captcha") {
      throw new Error("Blocked by ShieldSquare Captcha");
    }

    // 3. Extract Data
    const data = await page.evaluate(() => {
      const nextData = document.getElementById('__NEXT_DATA__');
      return nextData ? JSON.parse(nextData.innerHTML) : null;
    });

    if (!data) throw new Error("Failed to extract __NEXT_DATA__");

    const props = data.props?.pageProps;

    // Debugging logs
    logToFile("PageProps Keys: " + Object.keys(props || {}).join(', '));
    if (props?.initialState) logToFile("InitialState Keys: " + Object.keys(props.initialState).join(', '));

    let feed = props?.feed ||
      props?.initialState?.feed?.data ||
      props?.initialState?.cat?.feed?.data ||
      props?.search?.results;

    if (!feed) {
      // Try deeper search in typical places
      try {
        if (props?.initialState?.search) {
          logToFile("Search State Keys: " + Object.keys(props.initialState.search).join(', '));
        }
      } catch (e) { }
    }

    let items: any[] = [];
    let totalItems = 0;

    if (feed) {
      logToFile("Feed found. Keys: " + Object.keys(feed).join(', '));

      // Handle the NEW structure (arrays)
      if (Array.isArray(feed.private)) {
        items = [...items, ...feed.private];
      } else if (feed.private && feed.private.items) {
        items = [...items, ...feed.private.items];
      }

      if (Array.isArray(feed.agency)) {
        items = [...items, ...feed.agency];
      } else if (feed.agency && feed.agency.items) {
        items = [...items, ...feed.agency.items];
      }

      // Fallback for flat structure
      if (items.length === 0) {
        if (feed.feed_items) {
          items = feed.feed_items;
        } else if (Array.isArray(feed)) {
          items = feed;
        }
      }

      totalItems = feed.total_items || items.length;
    } else {
      logToFile("FEED OBJECT NOT FOUND IN EXPECTED LOCATIONS");
    }

    logToFile(`Found ${items.length} items`);

    const listings: Yad2Listing[] = items.map((item: any) => {
      // Map based on the NEW structure vs LEGACY structure
      const res: Yad2Listing = {
        id: String(item.id || item.orderId || item.token),
        token: item.token || String(item.id),
        title: item.title_1 || item.title_2 || item.search_text ||
          (item.address ? `${item.additionalDetails?.property?.text || ''} ${item.address.street?.text || ''}` : "Listing"),
        price: item.price ? Number(item.price) : parsePrice(item.price_text),
        city: item.address?.city?.text || item.city || "",
        neighborhood: item.address?.neighborhood?.text || item.neighborhood || "",
        street: item.address?.street?.text || item.street || "",
        rooms: parseFloat(String(item.additionalDetails?.roomsCount || item.Rooms_text || item.rooms || "0")),
        floor: Number(item.address?.house?.floor ?? parseFloor(item.floor_text || item.floor)),
        squareMeters: Number(item.additionalDetails?.squareMeter || item.SquareMeter || item.square_meters || "0"),
        dateAdded: item.date_added || item.published_at || "",
        images: item.metaData?.images || (item.images || []).map((img: any) => typeof img === 'string' ? img : img.src),
        description: item.info_text || item.row_4 || item.text || "",
        contactName: item.contact_name || item.contact?.name,
        url: `https://www.yad2.co.il/realestate/item/${item.token || item.id}`,
      };
      return res;
    });

    return {
      listings,
      totalItems: totalItems,
      totalPages: Math.ceil(totalItems / 40),
      currentPage: params.page || 1
    };

  } catch (error) {
    logToFile("Puppeteer Search Error: " + error);
    throw error;
  } finally {
    // keeping tab open as per user request
    // if (page) await page.close().catch(() => { });
  }
}

async function getYad2ListingDetails(token: string): Promise<Yad2Listing | null> {
  // Simple implementation reusing search logic or just direct navigation
  logToFile("Starting Yad2 Details Fetch via Puppeteer...");
  const page = await getPage();
  try {
    const itemUrl = `https://www.yad2.co.il/realestate/item/${token}`;
    logToFile("Navigating to item: " + itemUrl);
    await page.goto(itemUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });

    const data = await page.evaluate(() => {
      const nextData = document.getElementById('__NEXT_DATA__');
      return nextData ? JSON.parse(nextData.innerHTML) : null;
    });

    if (!data) return null;

    // Try to find listing data in props.pageProps.item or similar
    const item = data.props?.pageProps?.item || data.props?.pageProps?.initialState?.item?.data;

    if (!item) return null;

    return {
      id: item.id,
      token: token,
      title: item.title_1 || item.title_2,
      price: parsePrice(item.price),
      city: item.city,
      neighborhood: item.neighborhood,
      street: item.street,
      rooms: parseFloat(item.Rooms_text || item.rooms || "0"),
      floor: parseFloor(item.floor_text),
      squareMeters: parseInt(item.SquareMeter || item.square_meters || "0", 10),
      dateAdded: item.date_added || "",
      images: (item.images || []).map((img: any) => typeof img === 'string' ? img : img.src),
      description: item.info_text,
      url: itemUrl
    };

  } catch (error) {
    logToFile("Get Details Error: " + error);
    return null;
  } finally {
    // keeping tab open as per user request
    // if (page) await page.close().catch(() => { });
  }
}

// ============================================================================
// Helpers
// ============================================================================

function parsePrice(priceStr: string): number {
  if (!priceStr) return 0;
  const cleaned = priceStr.replace(/[^\d]/g, "");
  return parseInt(cleaned, 10) || 0;
}

function parseFloor(floorStr?: string): number {
  if (!floorStr) return 0;
  const match = floorStr.match(/(\d+)/);
  return match ? parseInt(match[1], 10) : 0;
}

function formatListingsMarkdown(listings: Yad2Listing[]): string {
  if (listings.length === 0) {
    return "No listings found matching your criteria.";
  }

  return listings
    .map(
      (l, i) =>
        `### ${i + 1}. ${l.city}${l.neighborhood ? ` - ${l.neighborhood}` : ""}
- **Price:** ₪${l.price.toLocaleString()}/month
- **Rooms:** ${l.rooms} | **Floor:** ${l.floor} | **Size:** ${l.squareMeters}m²
- **Address:** ${l.street || "Not specified"}
- **Added:** ${l.dateAdded}
- **Link:** ${l.url}
${l.description ? `- **Description:** ${l.description.slice(0, 200)}${l.description.length > 200 ? "..." : ""}` : ""}`
    )
    .join("\n\n");
}

// ============================================================================
// MCP Server Setup
// ============================================================================

const server = new McpServer({
  name: "yad2-mcp-server",
  version: "1.0.0",
});

// Schema definitions
const SearchRentalsSchema = z
  .object({
    city: z
      .string()
      .optional()
      .describe("City name in Hebrew (e.g., 'תל אביב יפו', 'חיפה', 'ירושלים')"),
    price_min: z.number().int().min(0).optional().describe("Minimum monthly rent in NIS"),
    price_max: z.number().int().min(0).optional().describe("Maximum monthly rent in NIS"),
    rooms_min: z.number().min(1).max(12).optional().describe("Minimum number of rooms"),
    rooms_max: z.number().min(1).max(12).optional().describe("Maximum number of rooms"),
    page: z.number().int().min(1).default(1).describe("Page number for pagination"),
    format: z
      .enum(["json", "markdown"])
      .default("json")
      .describe("Response format: 'json' for structured data, 'markdown' for readable text"),
  })
  .strict();

const GetListingSchema = z
  .object({
    token: z.string().min(1).describe("Yad2 listing token (from listing URL or search results)"),
  })
  .strict();

// Register tools
server.registerTool(
  "yad2_search_rentals",
  {
    title: "Search Yad2 Rentals",
    description: `Search for rental apartments on Yad2.co.il - Israel's largest classifieds site.

This tool searches the Yad2 real estate rental listings and returns matching properties.

Args:
  - city (string, optional): City name in Hebrew (e.g., 'תל אביב יפו')
  - price_min (number, optional): Minimum monthly rent in NIS
  - price_max (number, optional): Maximum monthly rent in NIS
  - rooms_min (number, optional): Minimum number of rooms (1-12)
  - rooms_max (number, optional): Maximum number of rooms (1-12)
  - page (number, default: 1): Page number for pagination
  - format ('json' | 'markdown'): Response format

Returns (JSON format):
  {
    "total_items": number,
    "current_page": number,
    "total_pages": number,
    "listings": [{
      "id": string,
      "token": string,
      "price": number,
      "city": string,
      "neighborhood": string,
      "street": string,
      "rooms": number,
      "floor": number,
      "squareMeters": number,
      "dateAdded": string,
      "url": string,
      "images": string[]
    }]
  }

Examples:
  - Search Tel Aviv rentals under 8000 NIS: { "city": "תל אביב יפו", "price_max": 8000 }
  - 3-room apartments in Haifa: { "city": "חיפה", "rooms_min": 3, "rooms_max": 3 }
  - All rentals page 2: { "page": 2 }`,
    inputSchema: SearchRentalsSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async (params) => {
    const result = await searchYad2Rentals({
      city: params.city,
      priceMin: params.price_min,
      priceMax: params.price_max,
      roomsMin: params.rooms_min,
      roomsMax: params.rooms_max,
      page: params.page,
    });

    if (params.format === "markdown") {
      const header = `## Yad2 Rental Search Results\n**Found ${result.totalItems} listings** (Page ${result.currentPage}/${result.totalPages})\n\n`;
      return {
        content: [{ type: "text", text: header + formatListingsMarkdown(result.listings) }],
      };
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              total_items: result.totalItems,
              current_page: result.currentPage,
              total_pages: result.totalPages,
              listings: result.listings,
            },
            null,
            2
          ),
        },
      ],
      structuredContent: {
        total_items: result.totalItems,
        current_page: result.currentPage,
        total_pages: result.totalPages,
        listings: result.listings,
      },
    };
  }
);

server.registerTool(
  "yad2_get_listing",
  {
    title: "Get Yad2 Listing Details",
    description: `Get detailed information about a specific Yad2 rental listing.

Args:
  - token (string): Yad2 listing token (e.g., from search results or URL like yad2.co.il/realestate/item/TOKEN)

Returns:
  Full listing details including contact information, description, and all images.`,
    inputSchema: GetListingSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params) => {
    const listing = await getYad2ListingDetails(params.token);

    if (!listing) {
      return {
        content: [{ type: "text", text: `Listing with token "${params.token}" not found.` }],
      };
    }

    return {
      content: [{ type: "text", text: JSON.stringify(listing, null, 2) }],
      structuredContent: listing,
    };
  }
);

// ============================================================================
// Transport Setup
// ============================================================================

async function runStdio(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Yad2 MCP server running on stdio");
}

async function runHTTP(): Promise<void> {
  const app = express();
  app.use(express.json());

  app.get("/health", (_req, res) => {
    res.json({ status: "ok", server: "yad2-mcp-server" });
  });

  app.post("/mcp", async (req, res) => {
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true,
    });
    res.on("close", () => transport.close());
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  });

  const port = parseInt(process.env.PORT || "3001");
  app.listen(port, () => {
    console.error(`Yad2 MCP server running on http://localhost:${port}/mcp`);
  });
}

// Entry point
const transport = process.env.TRANSPORT || "stdio";
if (transport === "http") {
  runHTTP().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
  });
} else {
  runStdio().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
  });
}
