"use strict";
/**
 * Provider Manager - Handles all AI providers
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
exports.ProviderManager = void 0;
const vscode = __importStar(require("vscode"));
const openai_1 = require("./openai");
const anthropic_1 = require("./anthropic");
const gemini_1 = require("./gemini");
const ollama_1 = require("./ollama");
const openrouter_1 = require("./openrouter");
const nvidia_1 = require("./nvidia");
class ProviderManager {
    providers = new Map();
    currentProviderId;
    constructor() {
        this.initializeProviders();
        const config = vscode.workspace.getConfiguration('antigravity');
        this.currentProviderId = config.get('defaultProvider') || 'openai';
    }
    initializeProviders() {
        this.providers.clear();
        // Register all providers
        this.providers.set('openai', new openai_1.OpenAIProvider());
        this.providers.set('anthropic', new anthropic_1.AnthropicProvider());
        this.providers.set('gemini', new gemini_1.GeminiProvider());
        this.providers.set('ollama', new ollama_1.OllamaProvider());
        this.providers.set('openrouter', new openrouter_1.OpenRouterProvider());
        this.providers.set('nvidia-rtx', new nvidia_1.NvidiaRTXProvider());
    }
    reloadConfiguration() {
        this.initializeProviders();
        const config = vscode.workspace.getConfiguration('antigravity');
        this.currentProviderId = config.get('defaultProvider') || 'openai';
    }
    getCurrentProvider() {
        return this.providers.get(this.currentProviderId);
    }
    setCurrentProvider(id) {
        if (this.providers.has(id)) {
            this.currentProviderId = id;
        }
    }
    getProvider(id) {
        return this.providers.get(id);
    }
    getAvailableProviders() {
        const result = [];
        for (const [id, provider] of this.providers) {
            result.push({
                name: provider.name,
                id: id,
                model: provider.model,
                available: provider.isAvailable()
            });
        }
        return result;
    }
    async complete(options) {
        const provider = this.getCurrentProvider();
        if (!provider) {
            throw new Error('No provider available');
        }
        if (!provider.isAvailable()) {
            throw new Error(`${provider.name} is not configured. Please add API key in settings.`);
        }
        const result = await provider.complete(options);
        return result.content;
    }
    async streamComplete(options, onEvent) {
        const provider = this.getCurrentProvider();
        if (!provider) {
            onEvent({ type: 'error', error: 'No provider available' });
            return;
        }
        if (!provider.isAvailable()) {
            onEvent({ type: 'error', error: `${provider.name} is not configured` });
            return;
        }
        await provider.streamComplete(options, onEvent);
    }
}
exports.ProviderManager = ProviderManager;
//# sourceMappingURL=providerManager.js.map