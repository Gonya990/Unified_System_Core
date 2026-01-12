"use strict";
/**
 * Chat View Provider - Webview panel for the sidebar
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
exports.ChatViewProvider = void 0;
const vscode = __importStar(require("vscode"));
class ChatViewProvider {
    _extensionUri;
    _providerManager;
    static viewType = 'antigravity.chatView';
    _view;
    _messages = [];
    constructor(_extensionUri, _providerManager) {
        this._extensionUri = _extensionUri;
        this._providerManager = _providerManager;
    }
    resolveWebviewView(webviewView, _context, _token) {
        this._view = webviewView;
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };
        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
        // Handle messages from webview
        webviewView.webview.onDidReceiveMessage(async (data) => {
            switch (data.type) {
                case 'sendMessage':
                    await this._handleUserMessage(data.message);
                    break;
                case 'switchProvider':
                    this._providerManager.setCurrentProvider(data.providerId);
                    break;
                case 'clearChat':
                    this.clearConversation();
                    break;
                case 'insertCode':
                    vscode.commands.executeCommand('antigravity.insertCode', data.code);
                    break;
            }
        });
        // Send initial state
        this._updateWebview();
    }
    async sendMessage(message) {
        await this._handleUserMessage(message);
    }
    clearConversation() {
        this._messages = [];
        this._updateWebview();
    }
    async _handleUserMessage(message) {
        // Add user message
        this._messages.push({ role: 'user', content: message });
        this._updateWebview();
        // Get system prompt
        const config = vscode.workspace.getConfiguration('antigravity');
        const systemPrompt = config.get('systemPrompt') || '';
        const streamEnabled = config.get('streamResponses') ?? true;
        // Build messages with system prompt
        const messages = [
            { role: 'system', content: systemPrompt },
            ...this._messages
        ];
        // Add current file context
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const fileName = editor.document.fileName.split('/').pop();
            const language = editor.document.languageId;
            messages[0].content += `\n\nCurrent file: ${fileName} (${language})`;
        }
        // Add empty assistant message for streaming
        this._messages.push({ role: 'assistant', content: '' });
        const assistantIndex = this._messages.length - 1;
        try {
            if (streamEnabled) {
                await this._providerManager.streamComplete({ messages, stream: true }, (event) => {
                    if (event.type === 'content') {
                        this._messages[assistantIndex].content += event.content;
                        this._updateWebview();
                    }
                    else if (event.type === 'error') {
                        this._messages[assistantIndex].content = `Error: ${event.error}`;
                        this._updateWebview();
                    }
                });
            }
            else {
                const response = await this._providerManager.complete({ messages });
                this._messages[assistantIndex].content = response;
            }
        }
        catch (error) {
            this._messages[assistantIndex].content = `Error: ${error}`;
        }
        this._updateWebview();
    }
    _updateWebview() {
        if (this._view) {
            const providers = this._providerManager.getAvailableProviders();
            const current = this._providerManager.getCurrentProvider();
            this._view.webview.postMessage({
                type: 'update',
                messages: this._messages,
                providers: providers,
                currentProvider: current?.id || 'openai'
            });
        }
    }
    _getHtmlForWebview(webview) {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Antigravity AI</title>
    <style>
        :root {
            --bg-primary: var(--vscode-editor-background);
            --bg-secondary: var(--vscode-sideBar-background);
            --text-primary: var(--vscode-editor-foreground);
            --text-muted: var(--vscode-descriptionForeground);
            --accent: var(--vscode-button-background);
            --border: var(--vscode-panel-border);
            --user-bg: var(--vscode-button-background);
            --assistant-bg: var(--vscode-editor-inactiveSelectionBackground);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--vscode-font-family);
            font-size: var(--vscode-font-size);
            background: var(--bg-primary);
            color: var(--text-primary);
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            padding: 8px 12px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .header h3 {
            flex: 1;
            font-size: 12px;
            font-weight: 600;
        }

        .provider-select {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 11px;
            cursor: pointer;
        }

        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .message {
            padding: 10px 14px;
            border-radius: 12px;
            max-width: 90%;
            word-wrap: break-word;
            line-height: 1.5;
        }

        .message.user {
            background: var(--user-bg);
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }

        .message.assistant {
            background: var(--assistant-bg);
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }

        .message pre {
            background: var(--vscode-textCodeBlock-background);
            padding: 10px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 8px 0;
            font-family: var(--vscode-editor-font-family);
            font-size: 12px;
        }

        .message code {
            background: var(--vscode-textCodeBlock-background);
            padding: 2px 5px;
            border-radius: 3px;
            font-family: var(--vscode-editor-font-family);
        }

        .code-block {
            position: relative;
        }

        .copy-btn {
            position: absolute;
            top: 6px;
            right: 6px;
            background: var(--accent);
            border: none;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 10px;
            opacity: 0.8;
        }

        .copy-btn:hover {
            opacity: 1;
        }

        .input-container {
            padding: 12px;
            border-top: 1px solid var(--border);
            display: flex;
            gap: 8px;
        }

        #messageInput {
            flex: 1;
            padding: 10px 14px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 13px;
            resize: none;
            min-height: 40px;
            max-height: 120px;
        }

        #messageInput:focus {
            outline: none;
            border-color: var(--accent);
        }

        .send-btn {
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
            cursor: pointer;
            font-weight: 500;
        }

        .send-btn:hover {
            opacity: 0.9;
        }

        .send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-muted);
        }

        .empty-state h4 {
            margin-bottom: 8px;
        }

        .typing-indicator {
            display: flex;
            gap: 4px;
            padding: 8px;
        }

        .typing-indicator span {
            width: 6px;
            height: 6px;
            background: var(--text-muted);
            border-radius: 50%;
            animation: bounce 1.4s infinite;
        }

        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-6px); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h3>🚀 Antigravity AI</h3>
        <select class="provider-select" id="providerSelect">
            <option value="openai">OpenAI</option>
            <option value="anthropic">Claude</option>
            <option value="gemini">Gemini</option>
            <option value="ollama">Ollama</option>
            <option value="openrouter">OpenRouter</option>
        </select>
        <button class="copy-btn" onclick="clearChat()">Clear</button>
    </div>

    <div class="chat-container" id="chatContainer">
        <div class="empty-state">
            <h4>Start a conversation</h4>
            <p>Ask me anything about your code!</p>
        </div>
    </div>

    <div class="input-container">
        <textarea 
            id="messageInput" 
            placeholder="Ask anything..." 
            rows="1"
        ></textarea>
        <button class="send-btn" id="sendBtn" onclick="sendMessage()">Send</button>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        let isStreaming = false;

        const chatContainer = document.getElementById('chatContainer');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        const providerSelect = document.getElementById('providerSelect');

        // Auto-resize textarea
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        // Send on Enter (Shift+Enter for newline)
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Provider change
        providerSelect.addEventListener('change', function() {
            vscode.postMessage({
                type: 'switchProvider',
                providerId: this.value
            });
        });

        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message || isStreaming) return;

            vscode.postMessage({
                type: 'sendMessage',
                message: message
            });

            messageInput.value = '';
            messageInput.style.height = 'auto';
        }

        function clearChat() {
            vscode.postMessage({ type: 'clearChat' });
        }

        function copyCode(btn) {
            const code = btn.parentElement.querySelector('code').textContent;
            navigator.clipboard.writeText(code);
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = 'Copy', 1500);
        }

        function insertCode(code) {
            vscode.postMessage({
                type: 'insertCode',
                code: code
            });
        }

        function formatMessage(content) {
            // Simple markdown-like formatting
            let html = content
                .replace(/\`\`\`(\w+)?\n([\s\S]*?)\`\`\`/g, (_, lang, code) => {
                    return \`<div class="code-block"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>\${escapeHtml(code.trim())}</code></pre></div>\`;
                })
                .replace(/\`([^\`]+)\`/g, '<code>$1</code>')
                .replace(/\n/g, '<br>');
            return html;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Handle messages from extension
        window.addEventListener('message', event => {
            const data = event.data;
            
            if (data.type === 'update') {
                updateChat(data.messages);
                updateProviders(data.providers, data.currentProvider);
            }
        });

        function updateChat(messages) {
            if (messages.length === 0) {
                chatContainer.innerHTML = \`
                    <div class="empty-state">
                        <h4>Start a conversation</h4>
                        <p>Ask me anything about your code!</p>
                    </div>
                \`;
                return;
            }

            chatContainer.innerHTML = messages.map(msg => \`
                <div class="message \${msg.role}">
                    \${formatMessage(msg.content) || '<div class="typing-indicator"><span></span><span></span><span></span></div>'}
                </div>
            \`).join('');

            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function updateProviders(providers, currentId) {
            providerSelect.innerHTML = providers.map(p => \`
                <option value="\${p.id}" \${p.id === currentId ? 'selected' : ''} \${!p.available ? 'disabled' : ''}>
                    \${p.name} \${p.available ? '' : '(No API key)'}
                </option>
            \`).join('');
        }
    </script>
</body>
</html>`;
    }
}
exports.ChatViewProvider = ChatViewProvider;
//# sourceMappingURL=chatViewProvider.js.map