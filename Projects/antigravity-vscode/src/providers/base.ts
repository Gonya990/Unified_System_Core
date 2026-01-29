/**
 * Base interface for AI providers
 */

export interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
}

export interface CompletionOptions {
    messages: Message[];
    stream?: boolean;
    maxTokens?: number;
    temperature?: number;
}

export interface CompletionResult {
    content: string;
    usage?: {
        promptTokens: number;
        completionTokens: number;
    };
}

export interface StreamEvent {
    type: 'content' | 'done' | 'error';
    content?: string;
    error?: string;
}

export interface AIProvider {
    name: string;
    id: string;
    model: string;
    isAvailable(): boolean;

    complete(options: CompletionOptions): Promise<CompletionResult>;

    streamComplete(
        options: CompletionOptions,
        onEvent: (event: StreamEvent) => void
    ): Promise<void>;
}
