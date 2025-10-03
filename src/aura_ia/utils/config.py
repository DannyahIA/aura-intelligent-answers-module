"""Configuration management for Aura IA."""

import os
import json
from typing import Any, Dict, Optional
from .exceptions import ConfigException


class Config:
    """Configuration manager for Aura IA module."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to configuration file (JSON). If None, uses environment variables.
        """
        self._config: Dict[str, Any] = {}
        if config_path:
            self._load_from_file(config_path)
        else:
            self._load_from_env()
    
    def _load_from_file(self, config_path: str) -> None:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            raise ConfigException(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ConfigException(f"Invalid JSON in configuration file: {e}")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        self._config = {
            "gemini": {
                "api_key": os.getenv("GEMINI_API_KEY"),
                "model": os.getenv("GEMINI_MODEL", "gemini-pro"),
            },
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            },
            "default_provider": os.getenv("DEFAULT_AI_PROVIDER", "gemini"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "log_path": os.getenv("LOG_PATH", "logs/interactions.log"),
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'gemini.api_key')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific AI provider.
        
        Args:
            provider_name: Name of the provider (e.g., 'gemini', 'openai')
            
        Returns:
            Provider configuration dictionary
        """
        provider_config = self.get(provider_name, {})
        if not provider_config:
            raise ConfigException(f"No configuration found for provider: {provider_name}")
        return provider_config
