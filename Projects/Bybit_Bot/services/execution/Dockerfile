# Service: Execution Engine
FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

# Security: Run as non-privileged user
RUN useradd -m botuser && chown -R botuser /app
USER botuser

ENV PYTHONPATH=/app
ENTRYPOINT ["python", "services/execution/orders.py"]
