"use strict";
/**
 * NVIDIA NIM / RTX Provider
 * For running AI models locally on RTX GPUs via NVIDIA NIM
 * https://build.nvidia.com/explore/run-on-rtx
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
exports.NvidiaRTXProvider = void 0;
const vscode = __importStar(require("vscode"));
class NvidiaRTXProvider {
    name = 'NVIDIA RTX';
    id = 'nvidia-rtx';
    model;
    endpoint;
    apiKey;
    // Available NIM models for RTX
    static MODELS = {
        'llama-3.1-8b': 'meta/llama-3.1-8b-instruct',
        'mistral-7b': 'mistralai/mistral-7b-instruct-v0.3',
        'phi-3-mini': 'microsoft/phi-3-mini-128k-instruct',
        'gemma-2-2b': 'google/gemma-2-2b-it',
        'nemotron-mini': 'nvidia/llama-3.1-nemotron-70b-instruct'
    };
    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.providers.nvidia');
        this.endpoint = config.get('endpoint') || 'http://localhost:8000';
        this.model = config.get('model') || 'meta/llama-3.1-8b-instruct';
        this.apiKey = config.get('apiKey') || ''; // For cloud NIM API
    }
    isAvailable() {
        return true; // Local endpoint, check on use
    }
    async complete(options) {
        const headers = {
            'Content-Type': 'application/json'
        };
        // If using cloud NVIDIA API (build.nvidia.com)
        if (this.apiKey) {
            headers['Authorization'] = `Bearer ${this.apiKey}`;
        }
        const response = await fetch(`${this.endpoint}/v1/chat/completions`, {
            method: 'POST',
            headers,
            body: JSON.stringify({
                model: this.model,
                messages: options.messages,
                max_tokens: options.maxTokens || 4096,
                temperature: options.temperature || 0.7,
                stream: false
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
        const headers = {
            'Content-Type': 'application/json'
        };
        if (this.apiKey) {
            headers['Authorization'] = `Bearer ${this.apiKey}`;
        }
        try {
            const response = await fetch(`${this.endpoint}/v1/chat/completions`, {
                method: 'POST',
                headers,
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
            onEvent({
                type: 'error',
                error: `NVIDIA NIM not running. Start with: docker run --gpus all -p 8000:8000 nvcr.io/nim/${this.model}`
            });
        }
    }
}
exports.NvidiaRTXProvider = NvidiaRTXProvider;
//# sourceMappingURL=nvidia.js.map