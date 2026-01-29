# Antigravity MCP Server
# Docker and GPU control via MCP protocol

FROM node:20-slim

# Install Docker CLI for container management
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --only=production 2>/dev/null || npm install --only=production

# Copy TypeScript config and source
COPY tsconfig.json ./
COPY src/ ./src/

# Build TypeScript
RUN npm run build

# Environment
ENV NODE_ENV=production
ENV PORT=3005

# Expose port
EXPOSE 3005

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3005/health || exit 1

# Run compiled JavaScript
CMD ["node", "dist/index.js"]
