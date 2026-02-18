import logging
import re
from typing import Optional, Any, Callable

logger = logging.getLogger(__name__)

class VibraniumShield:
    """
    🛡️ Vibranium Shield - Personality Protection & Security Module.
    Inspired by NotebookLM 2026 Analysis.
    
    Prevents:
    1. Indirect Prompt Injection (from untrusted inputs)
    2. Autonomous System Damage (without Admin ACK)
    3. Unauthorized Financial Operations
    """
    
    def __init__(self, admin_id: int):
        self.admin_id = admin_id
        # Suspicious keywords that might indicate prompt injection
        self.injection_patterns = [
            r"ignore previous instructions",
            r"system override",
            r"instead of .* do .*",
            r"you are now .* and must .*",
            r"transfer all funds",
            r"delete all files"
        ]
        
    def validate_prompt(self, text: str) -> bool:
        """Check for common prompt injection patterns."""
        for pattern in self.injection_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"🛡️ SHIELD: Potential prompt injection detected: {pattern}")
                return False
        return True

    async def check_action_safety(self, action_name: str, details: dict, bot: Any, chat_id: int) -> bool:
        """
        Human-in-the-Loop: Requires Admin ACK for critical actions.
        """
        critical_actions = ["transfer", "liquidate", "delete", "shutdown", "reboot", "deploy"]
        
        if any(ca in action_name.lower() for ca in critical_actions):
            logger.info(f"🛡️ SHIELD: Critical action detected: {action_name}. Waiting for ACK.")
            
            # If not admin, block immediately
            if chat_id != self.admin_id:
                await bot.send_message(chat_id, "❌ Error: This action requires Admin privileges.")
                return False
                
            # For Admin, we still want a confirmation step to prevent "accidental" or "hallucinated" orders
            msg = f"⚠️ **CRITICAL ACTION DETECTED**\n\nAction: `{action_name}`\nDetails: `{details}`\n\nDo you confirm? (Reply YES to proceed)"
            await bot.send_message(self.admin_id, msg, parse_mode='Markdown')
            
            # Note: The actual waiting for reply logic would be in the bot's message handler
            # This is a marker for the policy
            return False # Should return false and wait for a second message 'YES'
            
        return True

    def sanitize_output(self, content: str) -> str:
        """Ensure the AI doesn't leak sensitive system info in its responses."""
        # Hide internal paths or specific tokens if they appear by mistake
        sanitized = content.replace("/Users/igorgoncharenko", "~")
        # Add more filters as needed
        return sanitized

shield = None # Singleton instance to be initialized in main.py
