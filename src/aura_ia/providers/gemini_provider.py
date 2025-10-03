"""Google Gemini AI provider implementation."""

from typing import Dict, Any, Optional, List
from ..core.ai_provider import AIProvider, AIProviderConfig
from ..utils.exceptions import ProviderException


class GeminiProvider(AIProvider):
    """Google Gemini AI provider."""
    
    def __init__(self, config: AIProviderConfig):
        """
        Initialize Gemini provider.
        
        Args:
            config: Provider configuration
        """
        super().__init__(config)
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Gemini API client."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.config.api_key)
            self._client = genai.GenerativeModel(self.config.model)
        except ImportError:
            raise ProviderException(
                "google-generativeai package not installed. "
                "Install it with: pip install google-generativeai"
            )
        except Exception as e:
            raise ProviderException(f"Failed to initialize Gemini client: {str(e)}")
    
    async def generate_response(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate response using Gemini.
        
        Args:
            prompt: User prompt/question
            context: Additional context information
            conversation_history: Previous conversation messages
            
        Returns:
            AI-generated response
        """
        if not self._client:
            raise ProviderException("Gemini client not initialized")
        
        try:
            # Build the full prompt with context
            full_prompt = self._build_prompt(prompt, context, conversation_history)
            
            # Generate response
            response = self._client.generate_content(
                full_prompt,
                generation_config={
                    "temperature": self.config.temperature,
                    "max_output_tokens": self.config.max_tokens,
                }
            )
            
            return response.text
        except Exception as e:
            raise ProviderException(f"Gemini generation failed: {str(e)}")
    
    def _build_prompt(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Build full prompt with context and history."""
        parts = []
        
        # Add context if provided
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            parts.append(f"Context:\n{context_str}\n")
        
        # Add conversation history if provided
        if conversation_history:
            history_str = "\n".join([
                f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                for msg in conversation_history
            ])
            parts.append(f"Previous conversation:\n{history_str}\n")
        
        # Add current prompt
        parts.append(f"User: {prompt}")
        
        return "\n".join(parts)
    
    def get_provider_name(self) -> str:
        """Get provider name."""
        return "gemini"
    
    def is_available(self) -> bool:
        """Check if Gemini provider is available."""
        try:
            import google.generativeai
            return self._client is not None and bool(self.config.api_key)
        except ImportError:
            return False
