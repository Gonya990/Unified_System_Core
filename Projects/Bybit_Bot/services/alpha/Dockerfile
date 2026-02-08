FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/alpha/ ./services/alpha/
COPY common/ ./common/

ENV PYTHONPATH=/app
ENTRYPOINT ["python", "services/alpha/strategy.py"]
