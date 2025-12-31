# AI Telegram Bot - Local Development

Guide for developing and testing the bot locally.

---

## Setup

### 1. Prerequisites

- Python 3.11+
- Docker (optional, for container testing)
- Ollama or access to OpenAI-compatible API

### 2. Clone and Configure

```bash
cd Windows_AI_Core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your TELEGRAM_BOT_TOKEN
```

### 3. Start Local Ollama

```bash
# Start Ollama (if using local inference)
ollama serve

# Pull a model
ollama pull llama3.2
```

---

## Running

### Direct Python

```bash
source venv/bin/activate
export $(cat .env | xargs)
python -m src.main
```

### Docker Development

```bash
# Build and run with mounted source
docker compose -f docker-compose.dev.yml up --build

# Rebuild after changes
docker compose -f docker-compose.dev.yml up --build --force-recreate
```

---

## Testing

### Manual Testing

1. Start the bot
2. Open Telegram and find your bot
3. Test commands:
   - `/start` - Should show welcome message
   - `/status` - Should show configuration
   - Send any text - Should get AI response

### Health Check

```bash
curl http://localhost:8080/health
# Should return: {"status": "healthy", ...}
```

---

## Project Structure

```plaintext
Windows_AI_Core/
├── src/
│   ├── __init__.py
│   ├── main.py            # Entry point, Telegram handlers
│   ├── config_manager.py  # Configuration with encryption
│   ├── inference_client.py # Ollama/OpenAI client
│   ├── health.py          # Health check server
│   └── logging_config.py  # Structured logging
├── k8s/                   # Kubernetes manifests
├── docs/                  # Documentation
├── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── requirements.txt
└── .env.example
```

---

## Making Changes

1. Edit code in `src/`
2. Test locally with Docker:

   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```

3. Run linting:

   ```bash
   pip install ruff
   ruff check src/
   ```

4. Commit and push - CI/CD handles the rest
