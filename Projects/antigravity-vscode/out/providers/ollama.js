"use strict";
/**
 * Ollama Local Provider
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
exports.OllamaProvider = void 0;
const vscode = __importStar(require("vscode"));
class OllamaProvider {
    name = 'Ollama';
    id = 'ollama';
    model;
    endpoint;
    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.providers.ollama');
        this.endpoint = config.get('endpoint') || 'http://localhost:11434';
        this.model = config.get('model') || 'llama3.2';
    }
    isAvailable() {
        // Ollama is always "available" - we check connection on use
        return true;
    }
    async complete(options) {
        const response = await fetch(`${this.endpoint}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: this.model,
                messages: options.messages,
                stream: false
            })
        });
        const data = await response.json();
        return {
            content: data.message?.content || '',
            usage: {
                promptTokens: data.prompt_eval_count || 0,
                completionTokens: data.eval_count || 0
            }
        };
    }
    async streamComplete(options, onEvent) {
        try {
            const response = await fetch(`${this.endpoint}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: this.model,
                    messages: options.messages,
                    stream: true
                })
            });
            const reader = response.body?.getReader();
            const decoder = new TextDecoder();
            if (!reader) {
                onEvent({ type: 'error', error: 'No response stream' });
                return;
            }
            while (true) {
                const { done, value } = await reader.read();
                if (done)
                    break;
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n').filter(Boolean);
                for (const line of lines) {
                    try {
                        const parsed = JSON.parse(line);
                        if (parsed.done) {
                            onEvent({ type: 'done' });
                            return;
                        }
                        const content = parsed.message?.content;
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
            onEvent({ type: 'error', error: `Ollama not running: ${error}` });
        }
    }
}
exports.OllamaProvider = OllamaProvider;
//# sourceMappingURL=ollama.js.map