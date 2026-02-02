"""
Base Agent Infrastructure for Unified System AI Core

This module provides the core AgentOrchestrator class that uses OpenAI Function Calling
to enable agentic workflows with tool execution.
"""

import json
import logging
from dataclasses import dataclass
from typing import Any, Callable, Optional

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """Tool definition for OpenAI function calling"""
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable
    requires_approval: bool = False


class AgentOrchestrator:
    """
    Main agent orchestration engine using OpenAI Function Calling.

    This class manages:
    - Tool registration and execution
    - Conversation history
    - Multi-step reasoning with OpenAI models
    - Progress reporting

    Example:
        agent = AgentOrchestrator()
        agent.register_tool(my_tool)
        result = await agent.run("Turn on the lights")
    """

    SYSTEM_PROMPT = """You are a helpful AI agent with access to tools.

When given a task:
1. Break it down into clear steps
2. Use available tools to accomplish each step
3. Combine results to give final answer

Always explain your reasoning before using tools.
If a task is ambiguous, ask for clarification before proceeding.
Be concise and direct in your responses."""

    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        """
        Initialize AgentOrchestrator.

        Args:
            model: OpenAI model to use (default: gpt-4o)
            api_key: OpenAI API key (optional, uses env OPENAI_API_KEY if not provided)
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.tools: dict[str, Tool] = {}
        self.conversation_history: list[dict] = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]

    def register_tool(self, tool: Tool):
        """
        Register a new tool for the agent to use.

        Args:
            tool: Tool instance to register
        """
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def _build_tool_definitions(self) -> list[dict]:
        """Convert registered tools to OpenAI function format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]

    async def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """
        Execute a tool and return result.

        Args:
            tool_name: Name of tool to execute
            arguments: Tool arguments as dict

        Returns:
            Tool execution result as string
        """
        if tool_name not in self.tools:
            error_msg = f"Error: Tool '{tool_name}' not found"
            logger.error(error_msg)
            return error_msg

        tool = self.tools[tool_name]

        try:
            logger.info(f"Executing tool: {tool_name} with args: {arguments}")
            result = await tool.handler(**arguments)

            # Convert result to string if needed
            if isinstance(result, dict):
                return json.dumps(result, indent=2)
            return str(result)

        except Exception as e:
            error_msg = f"Error executing {tool_name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg

    async def run(
        self,
        user_message: str,
        on_progress: Optional[Callable[[str], None]] = None,
        max_iterations: int = 10
    ) -> str:
        """
        Run agent with user message, allowing multiple tool calls.

        Args:
            user_message: User's task/question
            on_progress: Optional callback for progress updates
            max_iterations: Maximum number of agent iterations (default: 10)

        Returns:
            Final agent response
        """

        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        iterations = 0

        while iterations < max_iterations:
            iterations += 1
            logger.info(f"Agent iteration {iterations}/{max_iterations}")

            # Call OpenAI with tools
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    tools=self._build_tool_definitions() if self.tools else None,
                    tool_choice="auto" if self.tools else None
                )
            except Exception as e:
                error_msg = f"OpenAI API error: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"❌ {error_msg}"

            message = response.choices[0].message

            # If no tool calls, we're done
            if not message.tool_calls:
                final_response = message.content or "No response generated"
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                logger.info(f"Agent completed in {iterations} iterations")
                return final_response

            # Add assistant message with tool calls to history
            tool_calls_data = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]

            self.conversation_history.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": tool_calls_data
            })

            # Execute each tool call
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError as e:
                    arguments = {}
                    logger.error(f"Failed to parse tool arguments: {e}")

                if on_progress:
                    on_progress(f"🔧 Executing: {tool_name}")

                result = await self.execute_tool(tool_name, arguments)

                # Add tool result to history
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result
                })

        warning_msg = f"⚠️ Max iterations ({max_iterations}) reached. Task may be too complex."
        logger.warning(warning_msg)
        return warning_msg

    def reset_conversation(self):
        """Clear conversation history (except system prompt)"""
        self.conversation_history = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]
        logger.info("Conversation history reset")

    def get_conversation_history(self) -> list[dict]:
        """Get current conversation history"""
        return self.conversation_history.copy()
