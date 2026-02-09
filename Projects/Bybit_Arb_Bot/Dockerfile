# Bybit Funding Arb Bot - Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/
COPY .env /app/.env

# Add src to PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]
