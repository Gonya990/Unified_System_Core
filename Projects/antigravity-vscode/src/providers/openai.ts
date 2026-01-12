/**
 * OpenAI Provider
 */

import * as vscode from 'vscode';
import { AIProvider, CompletionOptions, CompletionResult, StreamEvent } from './base';

export class OpenAIProvider implements AIProvider {
    name = 'OpenAI';
    id = 'openai';
    model: string;
    private apiKey: string;

    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.providers.openai');
        this.apiKey = config.get('apiKey') || '';
        this.model = config.get('model') || 'gpt-4o';
    }

    isAvailable(): boolean {
        return !!this.apiKey;
    }

    async complete(options: CompletionOptions): Promise<CompletionResult> {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
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

        const data = await response.json() as any;

        return {
            content: data.choices[0].message.content,
            usage: {
                promptTokens: data.usage?.prompt_tokens || 0,
                completionTokens: data.usage?.completion_tokens || 0
            }
        };
    }

    async streamComplete(
        options: CompletionOptions,
        onEvent: (event: StreamEvent) => void
    ): Promise<void> {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
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
                if (done) break;

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
                    } catch {
                        // Skip malformed JSON
                    }
                }
            }
            onEvent({ type: 'done' });
        } catch (error) {
            onEvent({ type: 'error', error: String(error) });
        }
    }
}
