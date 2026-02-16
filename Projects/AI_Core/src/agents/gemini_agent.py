"""
Gemini-based Agent Orchestrator

Use Google Gemini API (google.genai SDK) for function calling.
"""

import json
import logging
import os
from dataclasses import dataclass
from typing import Any, Callable, Optional

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """Tool definition for function calling"""

    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable
    requires_approval: bool = False


class GeminiAgentOrchestrator:
    """
    Agent orchestration using Google Gemini with function calling.
    """

    SYSTEM_PROMPT = """You are a helpful AI agent with access to tools.

When given a task:
1. Break it down into clear steps
2. Use available tools to accomplish each step
3. Combine results to give final answer

Always explain your reasoning before using tools.
If a task is ambiguous, ask for clarification before proceeding.
Be concise and direct in your responses."""

    def __init__(self, model: str = "gemini-2.0-flash-exp", api_key: Optional[str] = None):
        """Initialize Gemini Agent"""
        api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY must be set")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model
        self.tools: dict[str, Tool] = {}
        self.conversation_history: list[dict] = []

    def register_tool(self, tool: Tool):
        """Register a tool"""
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def _build_gemini_tools(self) -> list[types.Tool]:
        """Convert tools to Gemini format"""
        if not self.tools:
            return []

        function_declarations = []
        for tool in self.tools.values():
            gemini_params = self._convert_schema_to_gemini(tool.parameters)

            function_declarations.append(
                types.FunctionDeclaration(name=tool.name, description=tool.description, parameters=gemini_params)
            )

        return [types.Tool(function_declarations=function_declarations)]

    def _convert_schema_to_gemini(self, openai_schema: dict[str, Any]) -> types.Schema:
        """Convert OpenAI JSON Schema to Gemini Schema"""
        properties = {}
        required = openai_schema.get("required", [])

        for prop_name, prop_def in openai_schema.get("properties", {}).items():
            prop_type = prop_def.get("type", "STRING").upper()

            # Map JSON types to Gemini types
            type_mapping = {
                "STRING": "STRING",
                "INTEGER": "INTEGER",
                "NUMBER": "NUMBER",
                "BOOLEAN": "BOOLEAN",
                "ARRAY": "ARRAY",
                "OBJECT": "OBJECT",
            }

            gemini_type = type_mapping.get(prop_type, "STRING")

            properties[prop_name] = types.Schema(type=gemini_type, description=prop_def.get("description", ""))

        return types.Schema(type="OBJECT", properties=properties, required=required)

    async def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool"""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"

        tool = self.tools[tool_name]

        try:
            logger.info(f"Executing tool: {tool_name} with args: {arguments}")
            result = await tool.handler(**arguments)

            if isinstance(result, dict):
                return json.dumps(result, indent=2)
            return str(result)

        except Exception as e:
            logger.error(f"Tool execution error: {e}", exc_info=True)
            return f"Error executing {tool_name}: {str(e)}"

    async def run(
        self, user_message: str, on_progress: Optional[Callable[[str], None]] = None, max_iterations: int = 10
    ) -> str:
        """Run agent with Gemini"""

        try:
            config = types.GenerateContentConfig(
                tools=self._build_gemini_tools() if self.tools else None,
                system_instruction=self.SYSTEM_PROMPT,
            )

            chat = self.client.chats.create(model=self.model_name, config=config)

            iterations = 0

            while iterations < max_iterations:
                iterations += 1
                logger.info(f"Iteration {iterations}/{max_iterations}")

                if iterations == 1:
                    response = chat.send_message(user_message)
                else:
                    response = chat.send_message("Continue")

                # Check for function calls
                if hasattr(response, "candidates") and response.candidates:
                    candidate = response.candidates[0]

                    if hasattr(candidate.content, "parts"):
                        function_calls = [part for part in candidate.content.parts if hasattr(part, "function_call") and part.function_call]

                        if function_calls:
                            # Execute function calls
                            for fc_part in function_calls:
                                fc = fc_part.function_call
                                tool_name = fc.name
                                arguments = dict(fc.args)

                                if on_progress:
                                    on_progress(f"🔧 Executing: {tool_name}")

                                result = await self.execute_tool(tool_name, arguments)

                                # Send function response back
                                response = chat.send_message(
                                    types.Content(
                                        parts=[
                                            types.Part(
                                                function_response=types.FunctionResponse(
                                                    name=tool_name, response={"result": result}
                                                )
                                            )
                                        ]
                                    )
                                )
                            continue

                # No more function calls, return final response
                return response.text

            return f"⚠️ Max iterations ({max_iterations}) reached"

        except Exception as e:
            logger.error(f"Gemini error: {e}", exc_info=True)
            return f"❌ Error: {str(e)}"

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        logger.info("Conversation reset")
