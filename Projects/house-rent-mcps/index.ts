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
const USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36";

interface Yad2Listing {
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

async function searchYad2Rentals(params: {
  city?: string;
  priceMin?: number;
  priceMax?: number;
  roomsMin?: number;
  roomsMax?: number;
  page?: number;
}): Promise<{ listings: Yad2Listing[]; totalItems: number; totalPages: number; currentPage: number }> {
  const queryParams: Record<string, string> = {
    page: String(params.page || 1),
  };

  // City mapping (Yad2 uses city codes)
  if (params.city) {
    queryParams.city = params.city;
  }
  if (params.priceMin !== undefined) {
    queryParams.price = `${params.priceMin}-${params.priceMax || ""}`;
  } else if (params.priceMax !== undefined) {
    queryParams.price = `-${params.priceMax}`;
  }
  if (params.roomsMin !== undefined || params.roomsMax !== undefined) {
    queryParams.rooms = `${params.roomsMin || ""}-${params.roomsMax || ""}`;
  }

  try {
    const response = await axios.get<Yad2ApiResponse>(YAD2_API_BASE, {
      params: queryParams,
      headers: {
        "User-Agent": USER_AGENT,
        Accept: "application/json",
        "Accept-Language": "he-IL,he;q=0.9,en;q=0.8",
      },
      timeout: 30000,
    });

    const feed = response.data.feed;
    const listings: Yad2Listing[] = feed.feed_items
      .filter((item) => item.id && !item.merchant) // Filter out promoted/merchant items
      .map((item) => ({
        id: item.id,
        token: item.token,
        title: item.title_1 || item.title_2,
        price: parsePrice(item.price),
        city: item.city,
        neighborhood: item.neighborhood,
        street: item.street,
        rooms: parseFloat(item.Rooms_text || "0"),
        floor: parseFloor(item.floor_text),
        squareMeters: parseInt(item.SquareMeter || "0", 10),
        dateAdded: item.date_added || "",
        images: (item.images || []).map((img) => img.src),
        description: item.row_4,
        contactName: item.contact_name,
        url: `https://www.yad2.co.il/realestate/item/${item.token}`,
      }));

    return {
      listings,
      totalItems: feed.total_items,
      totalPages: feed.total_pages,
      currentPage: feed.current_page,
    };
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError;
      throw new Error(
        `Yad2 API error: ${axiosError.response?.status || "Network error"} - ${axiosError.message}`
      );
    }
    throw error;
  }
}

async function getYad2ListingDetails(token: string): Promise<Yad2Listing | null> {
  const detailUrl = `https://gw.yad2.co.il/feed-search-legacy/item/${token}`;

  try {
    const response = await axios.get(detailUrl, {
      headers: {
        "User-Agent": USER_AGENT,
        Accept: "application/json",
      },
      timeout: 15000,
    });

    const item = response.data;
    if (!item) return null;

    return {
      id: item.id,
      token: token,
      title: item.title_1 || item.title_2,
      price: parsePrice(item.price),
      city: item.city,
      neighborhood: item.neighborhood,
      street: item.street,
      rooms: parseFloat(item.Rooms_text || "0"),
      floor: parseFloor(item.floor_text),
      squareMeters: parseInt(item.SquareMeter || "0", 10),
      dateAdded: item.date_added || "",
      images: (item.images || []).map((img: { src: string }) => img.src),
      description: item.info_text || item.row_4,
      contactName: item.contact_name,
      contactPhone: item.phone,
      url: `https://www.yad2.co.il/realestate/item/${token}`,
    };
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      return null;
    }
    throw error;
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
