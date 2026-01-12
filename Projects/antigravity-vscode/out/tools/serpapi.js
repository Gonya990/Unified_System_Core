"use strict";
/**
 * SerpAPI Web Search Provider
 * Adds web search capability to Antigravity AI
 * https://serpapi.com
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.SerpAPISearch = void 0;
const vscode = __importStar(require("vscode"));
class SerpAPISearch {
    apiKey;
    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.tools.serpapi');
        this.apiKey = config.get('apiKey') || '';
    }
    isAvailable() {
        return !!this.apiKey;
    }
    async search(query, numResults = 5) {
        if (!this.apiKey) {
            return {
                query,
                results: [],
                error: 'SerpAPI key not configured. Get one at https://serpapi.com/dashboard'
            };
        }
        const params = new URLSearchParams({
            api_key: this.apiKey,
            engine: 'google',
            q: query,
            num: String(numResults)
        });
        try {
            const response = await fetch(`https://serpapi.com/search?${params}`);
            const data = await response.json();
            if (data.error) {
                return { query, results: [], error: data.error };
            }
            const results = (data.organic_results || [])
                .slice(0, numResults)
                .map((item) => ({
                title: item.title,
                link: item.link,
                snippet: item.snippet || '',
                position: item.position
            }));
            return {
                query,
                results,
                answerBox: data.answer_box?.answer || data.answer_box?.snippet
            };
        }
        catch (error) {
            return {
                query,
                results: [],
                error: String(error)
            };
        }
    }
    /**
     * Format search results for LLM context
     */
    formatForLLM(response) {
        if (response.error) {
            return `Search failed: ${response.error}`;
        }
        const lines = [`## Web Search: "${response.query}"\n`];
        if (response.answerBox) {
            lines.push(`**Quick Answer:** ${response.answerBox}\n`);
        }
        for (const result of response.results) {
            lines.push(`### ${result.position}. ${result.title}`);
            lines.push(`[${result.link}](${result.link})`);
            if (result.snippet) {
                lines.push(result.snippet);
            }
            lines.push('');
        }
        return lines.join('\n');
    }
}
exports.SerpAPISearch = SerpAPISearch;
//# sourceMappingURL=serpapi.js.map