"use strict";
/**
 * Groq Provider - Ultra fast inference
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
exports.GroqProvider = void 0;
const vscode = __importStar(require("vscode"));
class GroqProvider {
    name = 'Groq';
    id = 'groq';
    model;
    apiKey;
    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.providers.groq');
        this.apiKey = config.get('apiKey') || '';
        this.model = config.get('model') || 'llama-3.3-70b-versatile';
    }
    isAvailable() {
        return !!this.apiKey;
    }
    async complete(options) {
        const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                model: this.model,
                messages: options.messages,
                max_tokens: options.maxTokens || 4096,
                temperature: options.temperature || 0.7
            })
        });
        const data = await response.json();
        return {
            content: data.choices?.[0]?.message?.content || '',
            usage: {
                promptTokens: data.usage?.prompt_tokens || 0,
                completionTokens: data.usage?.completion_tokens || 0
            }
        };
    }
    async streamComplete(options, onEvent) {
        const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                model: this.model,
                messages: options.messages,
                max_tokens: options.maxTokens || 4096,
                temperature: options.temperature || 0.7,
                stream: true
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
                    if (data === '[DONE]') {
                        onEvent({ type: 'done' });
                        return;
                    }
                    try {
                        const parsed = JSON.parse(data);
                        const content = parsed.choices?.[0]?.delta?.content;
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
exports.GroqProvider = GroqProvider;
//# sourceMappingURL=groq.js.map