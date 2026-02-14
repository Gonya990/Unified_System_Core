# K8s Resources Checklist

This folder contains deployment manifests that expect several ConfigMaps and Secrets
to exist in the `trading` namespace. Create them before applying the deployments.

## Required ConfigMaps

1. `bot-google-credentials`
   - keys: `credentials.json`, `gcp-service-account.json`

```bash
kubectl -n trading create configmap bot-google-credentials \
  --from-file=credentials.json=/path/to/credentials.json \
  --from-file=gcp-service-account.json=/path/to/gcp-service-account.json
```

2. `bot-gmail-credentials`
   - keys: `gmail_credentials.json`

```bash
kubectl -n trading create configmap bot-gmail-credentials \
  --from-file=gmail_credentials.json=/path/to/gmail_credentials.json
```

## Required Secrets

1. `vibranium-tokens`
   - keys: `tokens.yaml`

```bash
kubectl -n trading create secret generic vibranium-tokens \
  --from-file=tokens.yaml=/path/to/tokens.yaml
```

2. `ai-core-secrets`
   - expected to contain API keys and runtime settings used by `envFrom`
   - recommended: generate from a dedicated env file for the cluster

```bash
kubectl -n trading create secret generic ai-core-secrets \
  --from-env-file=/path/to/ai-core.env
```

3. `bybit-secrets` (used by `telegram_deployment.yaml`)
   - keys: `TELEGRAM_BOT_TOKEN`

```bash
kubectl -n trading create secret generic bybit-secrets \
  --from-literal=TELEGRAM_BOT_TOKEN="REDACTED"
```

## Telegram Polling Conflict

If you run a local instance (PM2) and a GKE instance with the same bot token,
Telegram will return `Conflict: terminated by other getUpdates request`.
Ensure only one polling instance is active at a time (scale one deployment to 0
or stop PM2 locally).
