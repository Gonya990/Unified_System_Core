# CLIProxyAPI Deployment & Initialization Guide

This guide details how to deploy and initialize the centralized CLIProxyAPI on a Docker host.

## 📋 Prerequisites
- Docker Engine installed
- Docker Compose installed (or `docker compose` plugin)
- Internet access (to pull images)

## 🚀 Installation & Initialization

### 1. Prepare Directory
Ensure you are in the directory containing the `docker-compose.yml` and `config.yaml`:
```bash
cd infra/cliproxyapi
```

### 2. Create Network
Create the shared network for your AI services if it doesn't exist:
```bash
docker network create centralized_net || true
```

### 3. Initialize Authentication (CRITICAL STEP)
Before starting the server for the first time, you must authenticate your accounts (OpenAI, Claude, Gemini, etc.).
Run the login wizard using an ephemeral container that mounts your local `auth_db` folder. This prevents database locking issues.

```bash
# Ensure auth directory exists
mkdir -p auth_db

# Run the interactive login wizard
docker run --rm -it \
  -v $(pwd)/auth_db:/root/.cli-proxy-api \
  eceasy/cli-proxy-api:latest \
  /CLIProxyAPI/CLIProxyAPI --login
```
*Follow the on-screen prompts to paste your cookies/tokens.*

### 4. Start the Service
Once authenticated, start the proxy server in the background:

```bash
docker-compose up -d
```

### 5. Verify Operation
Check logs to ensure the server started and loaded the auths:
```bash
docker-compose logs -f cliproxy
```

## 🔄 Updates
**Automatic:** The `watchtower` service is included and will automatically update the proxy image every hour.

**Manual:**
```bash
docker-compose pull
docker-compose up -d
```

## 🔌 Connection Info
- **Internal URL:** `http://cliproxyapi:8317` (for containers on `centralized_net`)
- **External URL:** `http://<host-ip>:8317` (if ports are exposed)
