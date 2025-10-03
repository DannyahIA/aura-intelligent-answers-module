"""Interaction logging system for Aura IA."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class InteractionLogger:
    """Logger for AI interactions and system events."""
    
    def __init__(self, log_path: str = "logs/interactions.log", log_level: str = "INFO"):
        """
        Initialize interaction logger.
        
        Args:
            log_path: Path to log file
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_path = log_path
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Create log directory if it doesn't exist
        log_dir = Path(log_path).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logger
        self.logger = logging.getLogger("aura_ia")
        self.logger.setLevel(self.log_level)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(self.log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_interaction(
        self,
        request: str,
        response: str,
        provider: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an AI interaction.
        
        Args:
            request: User request/prompt
            response: AI response
            provider: AI provider used
            metadata: Additional metadata
        """
        interaction_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "request": request,
            "response": response,
            "provider": provider,
            "metadata": metadata or {}
        }
        
        self.logger.info(f"Interaction: {json.dumps(interaction_data, ensure_ascii=False)}")
    
    def log_error(
        self,
        error_message: str,
        error_type: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an error.
        
        Args:
            error_message: Error message
            error_type: Type of error
            details: Additional error details
        """
        error_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "details": details or {}
        }
        
        self.logger.error(f"Error: {json.dumps(error_data, ensure_ascii=False)}")
    
    def log_info(self, message: str) -> None:
        """Log an informational message."""
        self.logger.info(message)
    
    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)
    
    def log_debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)
