#!/bin/bash
# setup_central_hub.sh
# Automates the deployment of mcp_agent_mail on the target host (igor-gaming-1)

set -e

HUB_DIR="$HOME/acfs-hub"
REPO_URL="https://github.com/Dicklesworthstone/mcp_agent_mail.git"
AUTH_TOKEN="${1:-antigravity_secret}"

echo "🚀 Starting Central Hub Setup..."

# 1. Clone/Update repository
if [ ! -d "$HUB_DIR" ]; then
    echo "📦 Cloning mcp_agent_mail..."
    git clone "$REPO_URL" "$HUB_DIR"
else
    echo "🔄 Updating mcp_agent_mail..."
    cd "$HUB_DIR" && git pull
fi

cd "$HUB_DIR"

# 2. Patch Dockerfile for Postgres support
echo "🔧 Patching Dockerfile for Postgres..."
sed -i 's/uv sync --frozen --no-editable/uv sync --frozen --no-editable --extra postgres/g' Dockerfile

# 3. Create optimized docker-compose.yml
echo "📝 Writing docker-compose.yml..."
cat > docker-compose.yml <<EOF
version: '3.8'
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: agent_mail
      POSTGRES_USER: agent
      POSTGRES_PASSWORD: agent_pass
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped
  server:
    build: .
    command: ["python", "-m", "mcp_agent_mail.cli", "serve-http", "--host", "0.0.0.0", "--port", "8765"]
    ports:
      - "8765:8765"
    environment:
      DATABASE_URL: postgresql+asyncpg://agent:agent_pass@db:5432/agent_mail
      STORAGE_ROOT: /data/mailbox
      HTTP_HOST: 0.0.0.0
      HTTP_BEARER_TOKEN: ${AUTH_TOKEN}
    volumes:
      - mailbox_data:/data/mailbox
    depends_on:
      - db
    restart: unless-stopped
volumes:
  pgdata:
  mailbox_data:
EOF

# 3. Setup environment
echo "🔑 Setting up .env..."
echo "AUTH_TOKEN=$AUTH_TOKEN" > .env

# 4. Launch
echo "🐳 Launching with Docker Compose..."
docker compose up -d --build

echo "✅ Central Hub is up! Listening on port 8765."
echo "URL: http://$(hostname -I | awk '{print $1}'):8765"
