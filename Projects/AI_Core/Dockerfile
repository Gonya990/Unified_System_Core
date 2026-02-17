FROM python:3.12-slim

# Install UV for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping \
    curl \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# config/credential templates if needed (actual files mounted via volume)

# Environment variables
ENV PYTHONPATH=/app:/app/src
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "-m", "src.ai_telegram_bot_v2"]
