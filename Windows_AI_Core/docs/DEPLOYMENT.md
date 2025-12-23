# AI Telegram Bot - Deployment Guide

> Standard deployment procedures for the AI Telegram Bot service.

---

## Quick Start

### Prerequisites

- Docker and Docker Compose (for local/debug)
- Kubernetes cluster with ArgoCD (for production)
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Access to inference backend (Ollama, OpenAI, etc.)

---

## Local Development (Docker)

```bash
cd Windows_AI_Core

# 1. Configure environment
cp .env.example .env
# Edit .env with your TELEGRAM_BOT_TOKEN

# 2. Start in development mode
docker compose -f docker-compose.dev.yml up --build

# 3. View logs
docker compose logs -f
```

---

## Production Deployment (Kubernetes)

### Option A: ArgoCD (Recommended)

```bash
# 1. Create secrets first
kubectl create namespace telegram-bot
kubectl create secret generic telegram-bot-secrets \
  --from-literal=TELEGRAM_BOT_TOKEN=your-token-here \
  --from-literal=INFERENCE_API_KEY=your-api-key \
  -n telegram-bot

# 2. Apply ArgoCD application
kubectl apply -f k8s/argocd-application.yaml

# 3. ArgoCD will sync automatically from Git
```

### Option B: Direct kubectl

```bash
# 1. Update secrets in k8s/secrets.yaml with real values

# 2. Apply with Kustomize
kubectl apply -k k8s/

# 3. Verify deployment
kubectl get pods -n telegram-bot
kubectl logs -f deploy/ai-telegram-bot -n telegram-bot
```

---

## Updating the Bot

### GitOps Flow (Automatic)

1. Push changes to `main` branch
2. GitHub Actions builds new container image
3. ArgoCD detects change and syncs automatically

### Manual Update

```bash
# Pull latest image
docker compose pull

# Restart with new image
docker compose up -d
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | - | Bot token from BotFather |
| `INFERENCE_BASE_URL` | ❌ | `http://localhost:11434` | Inference API URL |
| `INFERENCE_API_KEY` | ❌ | - | API key for inference |
| `MODEL_NAME` | ❌ | `llama3.2` | Model to use |
| `LOG_LEVEL` | ❌ | `INFO` | Logging verbosity |

### Runtime Configuration via Telegram

Users can configure the bot directly in Telegram:

- `/setendpoint <url>` - Set inference API URL
- `/setapikey <key>` - Set API key (encrypted)
- `/setmodel <name>` - Set model name
- `/status` - View current configuration

---

## Health Checks

The bot exposes HTTP endpoints for monitoring:

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Liveness probe |
| `GET /ready` | Readiness probe |

---

## Rollback

### Kubernetes

```bash
# Rollback to previous revision
kubectl rollout undo deploy/ai-telegram-bot -n telegram-bot

# Or specify revision
kubectl rollout undo deploy/ai-telegram-bot --to-revision=2 -n telegram-bot
```

### Docker

```bash
# Use specific version
VERSION=<previous-sha> docker compose up -d
```
