FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV SERVICE_NAME={{SERVICE_NAME}}

WORKDIR /app

# Install dependencies first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ src/

# Create a non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8080

CMD ["python", "src/main.py"]
