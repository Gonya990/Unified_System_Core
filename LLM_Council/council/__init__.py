"""
LLM Council - Multi-model deliberation system.
"""

from .chairman import Chairman
from .council import LLMCouncil

__all__ = ["LLMCouncil", "Chairman"]
__version__ = "0.1.0"
