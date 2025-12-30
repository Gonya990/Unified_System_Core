FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psutil
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY metrics_collector.py .

# Environment variables (override at runtime)
ENV GCP_PROJECT=""
ENV INSTANCE_NAME="igor-gaming-1"
ENV COLLECTION_INTERVAL="60"
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_IDS=""

# Health check - simple process check
HEALTHCHECK --interval=60s --timeout=10s --start-period=10s --retries=3 \
    CMD pgrep -f "metrics_collector.py" || exit 1

CMD ["python", "metrics_collector.py"]
