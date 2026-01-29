/**
 * Ollama Local Provider
 */

import * as vscode from 'vscode';
import { AIProvider, CompletionOptions, CompletionResult, StreamEvent } from './base';

export class OllamaProvider implements AIProvider {
    name = 'Ollama';
    id = 'ollama';
    model: string;
    private endpoint: string;

    constructor() {
        const config = vscode.workspace.getConfiguration('antigravity.providers.ollama');
        this.endpoint = config.get('endpoint') || 'http://localhost:11434';
        this.model = config.get('model') || 'llama3.2';
    }

    isAvailable(): boolean {
        // Ollama is always "available" - we check connection on use
        return true;
    }

    async complete(options: CompletionOptions): Promise<CompletionResult> {
        const response = await fetch(`${this.endpoint}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: this.model,
                messages: options.messages,
                stream: false
            })
        });

        const data = await response.json() as any;

        return {
            content: data.message?.content || '',
            usage: {
                promptTokens: data.prompt_eval_count || 0,
                completionTokens: data.eval_count || 0
            }
        };
    }

    async streamComplete(
        options: CompletionOptions,
        onEvent: (event: StreamEvent) => void
    ): Promise<void> {
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
                if (done) break;

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
                    } catch {
                        // Skip
                    }
                }
            }
            onEvent({ type: 'done' });
        } catch (error) {
            onEvent({ type: 'error', error: `Ollama not running: ${error}` });
        }
    }
}
