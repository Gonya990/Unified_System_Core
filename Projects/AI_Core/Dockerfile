FROM python:3.12-slim

# Install UV for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping \
    curl \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Install dependencies using uv
# Install dependencies using uv
COPY Projects/AI_Core/requirements.txt .
# Compile bytecode for faster startup, install to system since we are in a container
# Use --prerelease=allow in case any transitive deps need it
RUN uv pip install --system --no-cache --prerelease=allow -r requirements.txt

# Copy source code
COPY Projects/AI_Core/src/ ./src/
# Copy External Tools (Agent Mail SDK)
COPY External_Tools/Stack/agent_mail_sdk /app/External_Tools/Stack/agent_mail_sdk

# config/credential templates if needed (actual files mounted via volume)

# Environment variables
ENV PYTHONPATH=/app:/app/src:/app/External_Tools/Stack/agent_mail_sdk/src
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "-m", "src.ai_telegram_bot_v2"]
