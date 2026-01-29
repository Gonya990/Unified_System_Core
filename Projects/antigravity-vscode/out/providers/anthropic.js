"use strict";
/**
 * Anthropic Claude Provider
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
exports.AnthropicProvider = void 0;
const vscode = __importStar(require("vscode"));
class AnthropicProvider {
    name = 'Claude';
    id = 'anthropic';
    model;
    apiKey;
    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.providers.anthropic');
        this.apiKey = config.get('apiKey') || '';
        this.model = config.get('model') || 'claude-sonnet-4-20250514';
    }
    isAvailable() {
        return !!this.apiKey;
    }
    async complete(options) {
        // Extract system message
        const systemMsg = options.messages.find(m => m.role === 'system');
        const chatMessages = options.messages.filter(m => m.role !== 'system');
        const response = await fetch('https://api.anthropic.com/v1/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.apiKey,
                'anthropic-version': '2023-06-01'
            },
            body: JSON.stringify({
                model: this.model,
                max_tokens: options.maxTokens || 4096,
                system: systemMsg?.content || '',
                messages: chatMessages.map(m => ({
                    role: m.role,
                    content: m.content
                }))
            })
        });
        const data = await response.json();
        return {
            content: data.content[0].text,
            usage: {
                promptTokens: data.usage?.input_tokens || 0,
                completionTokens: data.usage?.output_tokens || 0
            }
        };
    }
    async streamComplete(options, onEvent) {
        const systemMsg = options.messages.find(m => m.role === 'system');
        const chatMessages = options.messages.filter(m => m.role !== 'system');
        const response = await fetch('https://api.anthropic.com/v1/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': this.apiKey,
                'anthropic-version': '2023-06-01'
            },
            body: JSON.stringify({
                model: this.model,
                max_tokens: options.maxTokens || 4096,
                system: systemMsg?.content || '',
                messages: chatMessages.map(m => ({
                    role: m.role,
                    content: m.content
                })),
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
                    try {
                        const parsed = JSON.parse(data);
                        if (parsed.type === 'content_block_delta') {
                            const content = parsed.delta?.text;
                            if (content) {
                                onEvent({ type: 'content', content });
                            }
                        }
                        else if (parsed.type === 'message_stop') {
                            onEvent({ type: 'done' });
                            return;
                        }
                    }
                    catch {
                        // Skip malformed JSON
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
exports.AnthropicProvider = AnthropicProvider;
//# sourceMappingURL=anthropic.js.map