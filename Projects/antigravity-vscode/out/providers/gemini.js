"use strict";
/**
 * Google Gemini Provider
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
exports.GeminiProvider = void 0;
const vscode = __importStar(require("vscode"));
class GeminiProvider {
    name = 'Gemini';
    id = 'gemini';
    model;
    apiKey;
    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.providers.gemini');
        this.apiKey = config.get('apiKey') || '';
        this.model = config.get('model') || 'gemini-2.0-flash';
    }
    isAvailable() {
        return !!this.apiKey;
    }
    formatMessages(messages) {
        return messages.map(m => ({
            role: m.role === 'assistant' ? 'model' : 'user',
            parts: [{ text: m.content }]
        }));
    }
    async complete(options) {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${this.model}:generateContent?key=${this.apiKey}`;
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: this.formatMessages(options.messages),
                generationConfig: {
                    maxOutputTokens: options.maxTokens || 4096,
                    temperature: options.temperature || 0.7
                }
            })
        });
        const data = await response.json();
        return {
            content: data.candidates?.[0]?.content?.parts?.[0]?.text || '',
            usage: {
                promptTokens: data.usageMetadata?.promptTokenCount || 0,
                completionTokens: data.usageMetadata?.candidatesTokenCount || 0
            }
        };
    }
    async streamComplete(options, onEvent) {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${this.model}:streamGenerateContent?key=${this.apiKey}&alt=sse`;
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: this.formatMessages(options.messages),
                generationConfig: {
                    maxOutputTokens: options.maxTokens || 4096,
                    temperature: options.temperature || 0.7
                }
            })
        });
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        if (!reader) {
            onEvent({ type: 'error', error: 'No response stream' });
            return;
        }
        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done)
                    break;
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n').filter(line => line.startsWith('data: '));
                for (const line of lines) {
                    const data = line.slice(6);
                    try {
                        const parsed = JSON.parse(data);
                        const content = parsed.candidates?.[0]?.content?.parts?.[0]?.text;
                        if (content) {
                            onEvent({ type: 'content', content });
                        }
                    }
                    catch {
                        // Skip
                    }
                }
            }
            onEvent({ type: 'done' });
        }
        catch (error) {
            onEvent({ type: 'error', error: String(error) });
        }
    }
}
exports.GeminiProvider = GeminiProvider;
//# sourceMappingURL=gemini.js.map