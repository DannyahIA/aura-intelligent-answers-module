"""
Aura Intelligent Answers Module
The brain of Aura's automation for processing voice assistant requests.
"""

__version__ = "0.1.0"
__author__ = "Daniel Tavares"
__license__ = "MIT"

from .core.processor import RequestProcessor
from .core.ai_provider import AIProvider
from .core.logger import InteractionLogger

__all__ = [
    "RequestProcessor",
    "AIProvider",
    "InteractionLogger",
]
