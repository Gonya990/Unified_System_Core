"""
Yandex Alice Skill Handler for AI Telegram Bot.
Handles incoming webhook requests from Yandex Dialogs.
"""
import logging
from collections.abc import Awaitable
from typing import Callable

from aiohttp import web

logger = logging.getLogger(__name__)

class AliceSkill:
    def __init__(self, port: int = 8090):
        self.port = port
        self.app = web.Application()
        self.app.router.add_post("/alice", self._handle_webhook)
        self.runner = None
        self.site = None

        # Callback to handle intent execution (hooked to main bot logic)
        self.command_handler: Callable[[str, int], Awaitable[str]] = None

    def set_handler(self, handler: Callable[[str, int], Awaitable[str]]):
        """Set the async function that executes commands."""
        self.command_handler = handler

    async def start(self):
        """Start the web server."""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, "0.0.0.0", self.port)
        await self.site.start()
        logger.info(f"Alice Skill server started on port {self.port}")

    async def cleanup(self):
        """Stop the web server."""
        if self.runner:
            await self.runner.cleanup()

    async def _handle_webhook(self, request: web.Request) -> web.Response:
        """Handle incoming POST request from Yandex."""
        try:
            data = await request.json()
            logger.info(f"Alice request: {data}")

            response = {
                "version": data["version"],
                "session": data["session"],
                "response": {
                    "end_session": False
                }
            }

            req = data.get("request", {})
            command = req.get("command", "")
            original_utterance = req.get("original_utterance", "")
            user_id = data.get("session", {}).get("user", {}).get("user_id", "anonymous")

            # Handle "ping" (used by Yandex to check availability)
            if command == "ping":
                response["response"]["text"] = "pong"
                return web.json_response(response)

            if not command:
                 response["response"]["text"] = "Привет! Я Гоня. Что нужно сделать?"
                 return web.json_response(response)

            # Delegate to main handler
            if self.command_handler:
                try:
                    # Pass a pseudo-user-ID for Alice users (hashed or prefixed)
                    # For now using a fixed ID or similar logic

                    # Execute command
                    result_text = await self.command_handler(command, 0) # 0 = system/alice user
                    response["response"]["text"] = result_text[:1024] # Alice limit
                except Exception as e:
                    logger.error(f"Alice handler error: {e}")
                    response["response"]["text"] = "Произошла ошибка при выполнении команды."
            else:
                response["response"]["text"] = "Обработчик команд не настроен."

            return web.json_response(response)

        except Exception as e:
            logger.error(f"Alice webhook error: {e}")
            return web.Response(status=500)
