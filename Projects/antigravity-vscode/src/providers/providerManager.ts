/**
 * Provider Manager - Handles all AI providers
 */

import * as vscode from 'vscode';
import { AIProvider, CompletionOptions, StreamEvent } from './base';
import { OpenAIProvider } from './openai';
import { AnthropicProvider } from './anthropic';
import { GeminiProvider } from './gemini';
import { OllamaProvider } from './ollama';
import { OpenRouterProvider } from './openrouter';
import { NvidiaRTXProvider } from './nvidia';

export interface ProviderInfo {
    name: string;
    id: string;
    model: string;
    available: boolean;
}

export class ProviderManager {
    private providers: Map<string, AIProvider> = new Map();
    private currentProviderId: string;

    constructor() {
        this.initializeProviders();

        const config = vscode.workspace.getConfiguration('antigravity');
        this.currentProviderId = config.get('defaultProvider') || 'openai';
    }

    private initializeProviders() {
        this.providers.clear();

        // Register all providers
        this.providers.set('openai', new OpenAIProvider());
        this.providers.set('anthropic', new AnthropicProvider());
        this.providers.set('gemini', new GeminiProvider());
        this.providers.set('ollama', new OllamaProvider());
        this.providers.set('openrouter', new OpenRouterProvider());
        this.providers.set('nvidia-rtx', new NvidiaRTXProvider());
    }

    reloadConfiguration() {
        this.initializeProviders();
        const config = vscode.workspace.getConfiguration('antigravity');
        this.currentProviderId = config.get('defaultProvider') || 'openai';
    }

    getCurrentProvider(): AIProvider | undefined {
        return this.providers.get(this.currentProviderId);
    }

    setCurrentProvider(id: string) {
        if (this.providers.has(id)) {
            this.currentProviderId = id;
        }
    }

    getProvider(id: string): AIProvider | undefined {
        return this.providers.get(id);
    }

    getAvailableProviders(): ProviderInfo[] {
        const result: ProviderInfo[] = [];

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

    async complete(options: CompletionOptions): Promise<string> {
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

    async streamComplete(
        options: CompletionOptions,
        onEvent: (event: StreamEvent) => void
    ): Promise<void> {
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
