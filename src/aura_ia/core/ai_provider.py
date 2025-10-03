"""Base AI provider interface and configuration."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class AIProviderConfig:
    """Configuration for AI providers."""
    
    api_key: str
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    additional_params: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.additional_params is None:
            self.additional_params = {}


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    def __init__(self, config: AIProviderConfig):
        """
        Initialize AI provider.
        
        Args:
            config: Provider configuration
        """
        self.config = config
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate provider configuration."""
        if not self.config.api_key:
            raise ValueError(f"{self.__class__.__name__} requires an API key")
        if not self.config.model:
            raise ValueError(f"{self.__class__.__name__} requires a model name")
    
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate response from AI provider.
        
        Args:
            prompt: User prompt/question
            context: Additional context information
            conversation_history: Previous conversation messages
            
        Returns:
            AI-generated response
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the provider.
        
        Returns:
            Provider name
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if provider is available and configured.
        
        Returns:
            True if provider is ready to use
        """
        pass
