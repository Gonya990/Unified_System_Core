FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY server.py .
COPY simple_server.py .
COPY config.json .

# Environment variables (override at runtime)
ENV OPENAI_API_KEY=""
ENV MCP_HOST="0.0.0.0"
ENV MCP_PORT="8766"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8766/health')" || exit 1

EXPOSE 8766

CMD ["python", "server.py"]
