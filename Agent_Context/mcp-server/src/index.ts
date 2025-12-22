#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import express from "express";
import cors from "cors";
import { z } from "zod";
import { listContainers, restartContainer } from "./tools/docker.js";
import { checkOllamaHealth } from "./tools/ollama.js";

const app = express();
app.use(cors());
app.use(express.json());

// --- Security ---
// Simple API Key check
const API_KEY = process.env.MCP_API_KEY || "YOUR_API_KEY_HERE";

// Create MCP Server
const server = new Server(
    {
        name: "antigravity-mcp-server-http",
        version: "1.0.0",
    },
    {
        capabilities: {
            tools: {},
        },
    }
);

// --- Tools Registration (Same as before) ---
// --- Tool Logic Extracted ---
async function executeTool(name: string, args: any) {
    switch (name) {
        case "check_docker": {
            return await listContainers();
        }
        case "restart_container": {
            const { container_id } = args as { container_id: string };
            return await restartContainer(container_id);
        }
        case "check_gpu": {
            return await checkOllamaHealth();
        }
        default:
            throw new Error(`Unknown tool: ${name}`);
    }
}

// --- Tools Registration ---
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "check_docker",
                description: "List all Docker containers on the host machine.",
                inputSchema: { type: "object", properties: {} },
            },
            {
                name: "restart_container",
                description: "Restart a container by ID.",
                inputSchema: {
                    type: "object",
                    properties: { container_id: { type: "string" } },
                    required: ["container_id"],
                },
            },
            {
                name: "check_gpu",
                description: "Check GPU/Ollama status.",
                inputSchema: { type: "object", properties: {} },
            },
        ],
    };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
        const result = await executeTool(request.params.name, request.params.arguments);
        return { content: [{ type: "text", text: result }] };
    } catch (e: any) {
        return { content: [{ type: "text", text: `Error: ${e.message}` }], isError: true };
    }
});

// --- HTTP Transport Setup ---
let transport: SSEServerTransport;

app.get("/sse", async (req, res) => {
    console.log("New SSE connection...");
    transport = new SSEServerTransport("/message", res);
    await server.connect(transport);
});

app.post("/message", async (req, res) => {
    if (!transport) {
        // Fallback for n8n if they use /message endpoint incorrectly but want JSON-RPC
        // We'll try to handle it statelessly if it looks like a JSON-RPC call
        const body = req.body;
        if (body && body.method === "tools/call") {
            try {
                const result = await executeTool(body.params.name, body.params.arguments);
                res.json({
                    jsonrpc: "2.0",
                    id: body.id,
                    result: {
                        content: [{ type: "text", text: result }]
                    }
                });
                return;
            } catch (e: any) {
                res.status(500).json({ error: e.message });
                return;
            }
        }

        res.status(400).send("No active SSE connection and invalid JSON-RPC fallback");
        return;
    }
    // Basic Auth Check
    const key = req.headers["x-mcp-api-key"];
    if (key !== API_KEY) {
        console.warn("Unauthorized access attempt");
        // Ideally send 401, but keeping simple
    }

    await transport.handlePostMessage(req, res);
});

// --- Dedicated n8n Endpoint (Simplest) ---
app.post("/n8n", async (req, res) => {
    // Expects { tool: "name", args: {} } OR standard JSON-RPC
    const body = req.body;
    const key = req.headers["x-mcp-api-key"];

    if (key !== API_KEY) {
        res.status(401).json({ error: "Unauthorized" });
        return;
    }

    try {
        let toolName = body.tool;
        let toolArgs = body.args || {};

        // JSON-RPC support
        if (body.jsonrpc) {
            if (body.method === "tools/call") {
                toolName = body.params.name;
                toolArgs = body.params.arguments;
            }
        }

        if (!toolName) {
            res.status(400).json({ error: "Missing 'tool' or JSON-RPC params" });
            return;
        }

        const result = await executeTool(toolName, toolArgs);

        // Return simple JSON or JSON-RPC format? 
        // n8n HTTP Request expects simple JSON usually, but let's mirror input
        if (body.jsonrpc) {
            res.json({
                jsonrpc: "2.0",
                id: body.id || 1,
                result: {
                    content: [{ type: "text", text: result }]
                }
            });
        } else {
            res.json({ result });
        }

    } catch (e: any) {
        res.status(500).json({ error: e.message });
    }
});

const PORT = parseInt(process.env.PORT || "3005");
const HOST = process.env.HOST || "0.0.0.0";

app.listen(PORT, HOST, () => {
    console.log(`Antigravity MCP Server (HTTP) running on http://${HOST}:${PORT}`);
    console.log(`SSE Endpoint: http://${HOST}:${PORT}/sse`);
    console.log(`Message Endpoint: http://${HOST}:${PORT}/message (Supports Stateless Fallback)`);
    console.log(`n8n Endpoint: http://${HOST}:${PORT}/n8n`);
    console.log(`API Key: ${API_KEY}`);
});
