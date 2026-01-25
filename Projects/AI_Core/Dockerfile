FROM python:3.12-slim

# Install UV for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Install dependencies using uv
COPY requirements.txt .
# Compile bytecode for faster startup, install to system since we are in a container
RUN uv pip install --system --no-cache -r requirements.txt

# Copy source code
COPY src/ ./src/
# Copy config/credential templates if needed (actual files mounted via volume)

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "-m", "src.ai_telegram_bot_v2"]
