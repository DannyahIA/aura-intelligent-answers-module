"""OpenAI GPT provider implementation."""

from typing import Dict, Any, Optional, List
from ..core.ai_provider import AIProvider, AIProviderConfig
from ..utils.exceptions import ProviderException


class GPTProvider(AIProvider):
    """OpenAI GPT provider."""
    
    def __init__(self, config: AIProviderConfig):
        """
        Initialize GPT provider.
        
        Args:
            config: Provider configuration
        """
        super().__init__(config)
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize OpenAI API client."""
        try:
            from openai import AsyncOpenAI
            self._client = AsyncOpenAI(api_key=self.config.api_key)
        except ImportError:
            raise ProviderException(
                "openai package not installed. "
                "Install it with: pip install openai"
            )
        except Exception as e:
            raise ProviderException(f"Failed to initialize OpenAI client: {str(e)}")
    
    async def generate_response(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate response using GPT.
        
        Args:
            prompt: User prompt/question
            context: Additional context information
            conversation_history: Previous conversation messages
            
        Returns:
            AI-generated response
        """
        if not self._client:
            raise ProviderException("OpenAI client not initialized")
        
        try:
            # Build messages array
            messages = self._build_messages(prompt, context, conversation_history)
            
            # Generate response
            response = await self._client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise ProviderException(f"GPT generation failed: {str(e)}")
    
    def _build_messages(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        """Build messages array for GPT API."""
        messages = []
        
        # Add system message with context
        system_content = "You are Aura, an intelligent financial assistant."
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            system_content += f"\n\nContext:\n{context_str}"
        
        messages.append({"role": "system", "content": system_content})
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        return messages
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "gpt"
    
    def is_available(self) -> bool:
        """Check if GPT provider is available."""
        try:
            import openai
            return self._client is not None and bool(self.config.api_key)
        except ImportError:
            return False
