/**
 * Anthropic Claude Provider
 */

import * as vscode from 'vscode';
import { AIProvider, CompletionOptions, CompletionResult, StreamEvent } from './base';

export class AnthropicProvider implements AIProvider {
    name = 'Claude';
    id = 'anthropic';
    model: string;
    private apiKey: string;

    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.providers.anthropic');
        this.apiKey = config.get('apiKey') || '';
        this.model = config.get('model') || 'claude-sonnet-4-20250514';
    }

    isAvailable(): boolean {
        return !!this.apiKey;
    }

    async complete(options: CompletionOptions): Promise<CompletionResult> {
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

        const data = await response.json() as any;

        return {
            content: data.content[0].text,
            usage: {
                promptTokens: data.usage?.input_tokens || 0,
                completionTokens: data.usage?.output_tokens || 0
            }
        };
    }

    async streamComplete(
        options: CompletionOptions,
        onEvent: (event: StreamEvent) => void
    ): Promise<void> {
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
                if (done) break;

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
                        } else if (parsed.type === 'message_stop') {
                            onEvent({ type: 'done' });
                            return;
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
