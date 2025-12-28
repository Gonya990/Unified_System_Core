# 🚀 Distributed AI Inference Setup Guide

## 🎯 Goal

Offload heavy AI tasks (DeepSeek R1, Llama 3) from `igor-gaming-1` to `pve-antigravity-1` to improve production server stability and response time.

## 🏗️ Architecture

- **Master:** `igor-gaming-1` (Telegram Bot, Home Assistant, Controller)
- **Worker:** `pve-antigravity-1` (Ollama Server, Heavy Inference)

## 🛠️ Step 1: Setup Worker (pve-antigravity-1)

*Run these commands on pve-antigravity-1:*

```bash
# 1. Update & Install Docker (if needed)
curl -fsSL https://get.docker.com | sh
usermod -aG docker param0 # or root

# 2. Run Ollama with GPU support (if available) or CPU
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# 3. Pull required models
docker exec ollama ollama pull llama3
docker exec ollama ollama pull mistral
```

## 🔗 Step 2: Configure Master (igor-gaming-1)

*Update `.env` on igor-gaming-1:*

```ini
# INFERENCE PROVIDER CONFIGURATION
# Set remote Ollama instance
OLLAMA_BASE_URL=http://100.127.194.111:11434
INFERENCE_PROVIDER=ollama
MODEL_NAME=llama3
```

## 🔒 Step 3: Network Security (Tailscale)

Ensure both nodes are on Tailscale mesh for secure communication (`100.x.x.x` IPs).

```bash
# Check connection
ping 100.127.194.111
curl http://100.127.194.111:11434/api/tags
```

## 🚦 Verification

Restart the bot on Master:

```bash
sudo systemctl restart ai-bot
```

Monitor logs to confirm remote inference:

```bash
journalctl -u ai-bot -f
```
