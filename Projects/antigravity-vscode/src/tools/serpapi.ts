/**
 * SerpAPI Web Search Provider
 * Adds web search capability to Antigravity AI
 * https://serpapi.com
 */

import * as vscode from 'vscode';

export interface SearchResult {
    title: string;
    link: string;
    snippet: string;
    position: number;
}

export interface SearchResponse {
    query: string;
    results: SearchResult[];
    answerBox?: string;
    error?: string;
}

export class SerpAPISearch {
    private apiKey: string;

    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.tools.serpapi');
        this.apiKey = config.get('apiKey') || '';
    }

    isAvailable(): boolean {
        return !!this.apiKey;
    }

    async search(query: string, numResults: number = 5): Promise<SearchResponse> {
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
            const data = await response.json() as any;

            if (data.error) {
                return { query, results: [], error: data.error };
            }

            const results: SearchResult[] = (data.organic_results || [])
                .slice(0, numResults)
                .map((item: any) => ({
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

        } catch (error) {
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
    formatForLLM(response: SearchResponse): string {
        if (response.error) {
            return `Search failed: ${response.error}`;
        }

        const lines: string[] = [`## Web Search: "${response.query}"\n`];

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
