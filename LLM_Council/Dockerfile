FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY council/ ./council/
COPY council_demo.py .

# Environment variables (override at runtime)
ENV OPENAI_API_KEY=""
ENV ANTHROPIC_API_KEY=""
ENV GOOGLE_API_KEY=""
ENV OPENROUTER_API_KEY=""
ENV LOG_LEVEL="INFO"

# Default command - can be overridden
CMD ["python", "council_demo.py", "--interactive"]
