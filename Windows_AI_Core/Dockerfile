FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Create data volume mount point
VOLUME /data

# Environment variables (override at runtime)
ENV TELEGRAM_BOT_TOKEN=""
ENV INFERENCE_BASE_URL="http://localhost:11434"
ENV INFERENCE_API_KEY=""
ENV MODEL_NAME="llama3.2"
ENV LOG_LEVEL="INFO"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
