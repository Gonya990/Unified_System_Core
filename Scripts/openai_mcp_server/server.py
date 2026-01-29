#!/usr/bin/env python3
"""
OpenAI MCP Server | MCP Сервер OpenAI
English: MCP server providing access to OpenAI ChatGPT API
Russian: MCP сервер, предоставляющий доступ к API OpenAI ChatGPT
"""

import json
import os
from datetime import datetime
from typing import Any, Optional

import openai
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("openai-gateway",
              host="127.0.0.1",
              port=8766)

# Configure OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

@mcp.tool()
def list_conversations(limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
    """
    List ChatGPT conversations from OpenAI account.

    English: Retrieve a list of recent conversations.
    Russian: Получить список недавних разговоров.

    Args:
        limit: Maximum number of conversations to return
        offset: Number of conversations to skip

    Returns:
        List of conversation objects with id, title, created_at
    """
    try:
        # Note: This endpoint might need to use the Chat API or custom endpoint
        # OpenAI's official API doesn't directly expose conversation history yet
        # This is a placeholder for when the feature becomes available

        return {
            "status": "note",
            "message": "OpenAI API doesn't yet expose conversation history directly. Use export method or wait for official API support.",
            "alternative": "Consider using the manual export method from ChatGPT UI → Settings → Data Controls → Export",
            "conversations": []
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }


@mcp.tool()
def send_message(message: str, conversation_id: Optional[str] = None,
                model: str = "gpt-4") -> dict[str, Any]:
    """
    Send a message to ChatGPT and get response.

    English: Send a message to OpenAI's ChatGPT model.
    Russian: Отправить сообщение модели ChatGPT от OpenAI.

    Args:
        message: The message to send
        conversation_id: Optional conversation ID to continue (not yet supported)
        model: OpenAI model to use (gpt-4, gpt-3.5-turbo, etc.)

    Returns:
        Response from ChatGPT
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return {
            "status": "success",
            "response": response.choices[0].message.content,
            "model": model,
            "tokens_used": response.usage.total_tokens,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def get_models() -> list[str]:
    """
    Get list of available OpenAI models.

    English: Retrieve list of models you have access to.
    Russian: Получить список моделей, к которым у вас есть доступ.

    Returns:
        List of available model IDs
    """
    try:
        models = openai.models.list()
        return {
            "status": "success",
            "models": [model.id for model in models.data]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def get_account_info() -> dict[str, Any]:
    """
    Get OpenAI account information.

    English: Retrieve your OpenAI account details and API usage.
    Russian: Получить детали вашей учетной записи OpenAI и использование API.

    Returns:
        Account information
    """
    try:
        # Get available models as a proxy for account access
        models = openai.models.list()

        return {
            "status": "success",
            "api_key_valid": True,
            "models_accessible": len(models.data),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "api_key_valid": False
        }


@mcp.tool()
def chat_with_context(messages: list[dict[str, str]],
                     model: str = "gpt-4",
                     temperature: float = 0.7,
                     max_tokens: int = 4000) -> dict[str, Any]:
    """
    Send messages with full conversation context to ChatGPT.

    English: Have a multi-turn conversation with ChatGPT.
    Russian: Провести многоходовой разговор с ChatGPT.

    Args:
        messages: List of message objects with 'role' and 'content'
        model: OpenAI model to use
        temperature: Creativity level (0.0-1.0)
        max_tokens: Maximum tokens in response

    Returns:
        ChatGPT response with usage statistics
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return {
            "status": "success",
            "response": response.choices[0].message.content,
            "model": model,
            "tokens_used": {
                "prompt": response.usage.prompt_tokens,
                "completion": response.usage.completion_tokens,
                "total": response.usage.total_tokens
            },
            "finish_reason": response.choices[0].finish_reason,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.resource("openai://status")
def get_server_status() -> str:
    """
    Get MCP server status and configuration.

    Returns server health and configuration information.
    """
    try:
        # Test API key
        models = openai.models.list()
        api_status = "connected"
        model_count = len(models.data)
    except Exception:
        api_status = "disconnected"
        model_count = 0

    status = {
        "server": "openai-gateway",
        "status": "running",
        "openai_api": api_status,
        "models_available": model_count,
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "send_message": "Send individual messages",
            "chat_with_context": "Multi-turn conversations",
            "get_models": "List available models",
            "get_account_info": "Account information"
        }
    }

    return json.dumps(status, indent=2)


@mcp.prompt()
def ask_chatgpt_prompt(question: str) -> str:
    """
    Pre-built prompt to ask ChatGPT a question.

    English: Template for querying ChatGPT via OpenAI API.
    Russian: Шаблон для запроса ChatGPT через API OpenAI.
    """
    return f"""You are querying OpenAI's ChatGPT through the MCP server.

Question: {question}

The response will be returned from OpenAI's API.
"""


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   OpenAI MCP Gateway Server | MCP Gateway Сервер OpenAI     ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("English: Starting MCP server on http://127.0.0.1:8766")
    print("Russian: Запуск MCP сервера на http://127.0.0.1:8766")
    print()

    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING | ПРЕДУПРЕЖДЕНИЕ:")
        print("   OPENAI_API_KEY not found in environment")
        print("   OPENAI_API_KEY не найден в окружении")
        print()
        print("   Please set it in .env file:")
        print("   Пожалуйста, установите его в файле .env:")
        print("   OPENAI_API_KEY=sk-proj-...")
        print()
    else:
        print("✅ OpenAI API key found | API ключ OpenAI найден")
        print()

    print("Available tools | Доступные инструменты:")
    print("  - send_message")
    print("  - chat_with_context")
    print("  - get_models")
    print("  - get_account_info")
    print("  - list_conversations (placeholder)")
    print()
    print("Press Ctrl+C to stop | Нажмите Ctrl+C для остановки")
    print()

    mcp.run()
