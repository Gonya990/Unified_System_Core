/**
 * NVIDIA NIM / RTX Provider
 * For running AI models locally on RTX GPUs via NVIDIA NIM
 * https://build.nvidia.com/explore/run-on-rtx
 */

import * as vscode from 'vscode';
import { AIProvider, CompletionOptions, CompletionResult, StreamEvent } from './base';

export class NvidiaRTXProvider implements AIProvider {
    name = 'NVIDIA RTX';
    id = 'nvidia-rtx';
    model: string;
    private endpoint: string;
    private apiKey: string;

    // Available NIM models for RTX
    static readonly MODELS = {
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

    isAvailable(): boolean {
        return true; // Local endpoint, check on use
    }

    async complete(options: CompletionOptions): Promise<CompletionResult> {
        const headers: Record<string, string> = {
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

        const data = await response.json() as any;

        return {
            content: data.choices?.[0]?.message?.content || '',
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
        const headers: Record<string, string> = {
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
                        // Skip
                    }
                }
            }
            onEvent({ type: 'done' });
        } catch (error) {
            onEvent({
                type: 'error',
                error: `NVIDIA NIM not running. Start with: docker run --gpus all -p 8000:8000 nvcr.io/nim/${this.model}`
            });
        }
    }
}
