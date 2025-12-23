# AI Telegram Bot - Troubleshooting Guide

Common issues and solutions for the AI Telegram Bot.

---

## Connection Issues

### Bot Not Responding

**Symptoms:** Messages sent to bot get no reply.

**Check:**

1. Verify bot is running:

   ```bash
   # Kubernetes
   kubectl get pods -n telegram-bot
   kubectl logs -f deploy/ai-telegram-bot -n telegram-bot
   
   # Docker
   docker compose ps
   docker compose logs -f
   ```

2. Check bot token:

   ```bash
   # Test token validity
   curl "https://api.telegram.org/bot<TOKEN>/getMe"
   ```

3. Check health endpoint:

   ```bash
   curl http://localhost:8080/health
   ```

---

### Inference Connection Failed

**Symptoms:** Bot responds with "Connection Error" or "Cannot reach inference server".

**Solutions:**

1. **Verify Ollama is running:**

   ```bash
   curl http://<OLLAMA_HOST>:11434/api/tags
   ```

2. **Check network connectivity:**

   ```bash
   # From inside container
   kubectl exec -it deploy/ai-telegram-bot -n telegram-bot -- curl http://ollama:11434/api/tags
   ```

3. **Update endpoint via Telegram:**

   ```
   /setendpoint http://correct-host:11434
   /status
   ```

---

## Configuration Issues

### API Key Not Working

**Symptoms:** "Unauthorized" or "Invalid API key" errors.

1. Set new API key:

   ```
   /setapikey <new-key>
   ```

2. Verify storage:

   ```bash
   kubectl exec -it deploy/ai-telegram-bot -n telegram-bot -- cat /data/bot_config.json
   ```

### Wrong Model

**Symptoms:** Unexpected responses or "model not found" errors.

1. List available models:

   ```bash
   curl http://<OLLAMA_HOST>:11434/api/tags
   ```

2. Set correct model:

   ```
   /setmodel llama3.2
   ```

---

## Container Issues

### Pod CrashLoopBackOff

**Check logs:**

```bash
kubectl logs deploy/ai-telegram-bot -n telegram-bot --previous
```

**Common causes:**

- Missing `TELEGRAM_BOT_TOKEN` secret
- Invalid token format
- Network policy blocking egress

### OOMKilled

**Increase memory limits:**

```yaml
# k8s/deployment.yaml
resources:
  limits:
    memory: "1Gi"  # Increase from 512Mi
```

---

## Debug Mode

Enable verbose logging:

```bash
# Docker
LOG_LEVEL=DEBUG docker compose -f docker-compose.dev.yml up

# Kubernetes - edit configmap
kubectl edit configmap telegram-bot-config -n telegram-bot
# Set LOG_LEVEL: "DEBUG"
kubectl rollout restart deploy/ai-telegram-bot -n telegram-bot
```

---

## Getting Help

1. Check logs first
2. Verify configuration with `/status`
3. Test inference endpoint directly
4. Review recent changes in Git history
