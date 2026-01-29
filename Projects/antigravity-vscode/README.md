# Antigravity AI for VS Code

🚀 **Multi-provider AI chat sidebar for Visual Studio Code**

## Features

- **Multiple AI Providers** in one extension:
  - OpenAI (GPT-4o, o1, o3)
  - Anthropic (Claude 4 Sonnet/Opus)
  - Google Gemini (2.0 Flash/Pro)
  - Mistral (Large, Codestral)
  - OpenRouter (100+ models)
  - **NVIDIA NIM/RTX** (local GPU inference)
  - Ollama (local models)

- **Sidebar Chat Panel** - Always accessible from activity bar
- **Real-time Streaming** - See responses as they're generated
- **Code Context Aware** - Automatically includes current file info
- **Quick Actions**:
  - Explain selected code
  - Refactor selection
  - Insert generated code at cursor

## Installation

### From Source

```bash
cd Projects/antigravity-vscode
npm install
npm run compile
```

### Install in VS Code

Press `F5` to run Extension Development Host, or:

```bash
npm run package
code --install-extension antigravity-0.1.0.vsix
```

## Configuration

Open VS Code Settings (`Cmd+,`) and search for "Antigravity".

### API Keys

Add your API keys to enable providers:

```json
{
  "antigravity.defaultProvider": "openai",
  "antigravity.providers.openai.apiKey": "sk-...",
  "antigravity.providers.anthropic.apiKey": "sk-ant-...",
  "antigravity.providers.gemini.apiKey": "AIza...",
  "antigravity.providers.openrouter.apiKey": "sk-or-..."
}
```

### Ollama (Local)

For Ollama, just ensure it's running:

```bash
ollama serve
```

Then set the endpoint in settings:

```json
{
  "antigravity.providers.ollama.endpoint": "http://localhost:11434",
  "antigravity.providers.ollama.model": "llama3.2"
}
```

## Usage

1. Click the Antigravity icon in the Activity Bar (left sidebar)
2. Select your preferred AI provider from the dropdown
3. Start chatting!

### Context Menu

Right-click on selected code to:

- **Explain Selection** - Get an explanation
- **Refactor Selection** - Get refactored version

### Commands

- `Cmd+Shift+P` → "Antigravity: New Conversation"
- `Cmd+Shift+P` → "Antigravity: Switch Provider"

## OpenRouter - 100+ Models

With OpenRouter API key, you get access to:

- GPT-4o, GPT-4 Turbo
- Claude 3.5 Sonnet/Opus
- Gemini Pro
- Llama 3.1 70B
- Mistral Large
- DeepSeek V3
- Qwen 2.5
- And many more!

## Development

```bash
npm install          # Install dependencies
npm run watch        # Watch mode for development
npm run compile      # Compile TypeScript
npm run package      # Create .vsix package
```

## License

MIT
