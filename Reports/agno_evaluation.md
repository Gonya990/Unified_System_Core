# Agno Framework Evaluation Report

## Overview

Agno (formerly Phidata) is a lightweight Python framework for building agentic AI systems. It provides a standardized interface for various LLM providers and built-in support for tools, memory, and RAG.

## Evaluation Results

### 1. Provider Abstraction (P2)

Agno excels at provider abstraction. You can switch from OpenAI to Gemini or Ollama by changing the `model` parameter:

```python
# OpenAI
agent = Agent(model=OpenAIChat(id="gpt-4o"))

# Gemini
agent = Agent(model=Gemini(id="gemini-1.5-flash"))
```

### 2. Features

- **Tools**: Large library of built-in tools (DuckDuckGo, YFinance, SQL, etc.).
- **Memory**: Persistent session storage in PostgreSQL or SQLite.
- **UI**: Optional playground for testing agents.
- **Speed**: Minimal overhead compared to LangChain.

### 3. Integration with Unified System

- **LLM Council**: Agno can replace the custom provider logic in `longform_producer.py` and other scripts.
- **Content Factory**: Agno agents can handle the multi-step research process more reliably.

### 4. Known Issues

- **Conflict with instagrapi**: Agno uses Pydantic V2, while `instagrapi` is stuck on Pydantic V1. Requiers environment separation or careful dependency management.
- **Gemini SDK version**: Currently requires latest `google-genai`, but some imports are unstable.

## Verdict

**Recommended.** We should migrate Python-based agents to Agno to simplify development and improve reliability.

---
*Status: Evaluation Complete*
