"""Request processor for handling voice assistant requests."""

from typing import Dict, Any, Optional, List
from .ai_provider import AIProvider, AIProviderConfig
from .logger import InteractionLogger
from ..utils.config import Config
from ..utils.exceptions import ProviderException, ValidationException
from ..providers.gemini_provider import GeminiProvider
from ..providers.gpt_provider import GPTProvider


class RequestProcessor:
    """Main processor for handling voice assistant requests."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize request processor.
        
        Args:
            config: Configuration object. If None, creates default config.
        """
        self.config = config or Config()
        self.logger = InteractionLogger(
            log_path=self.config.get("log_path", "logs/interactions.log"),
            log_level=self.config.get("log_level", "INFO")
        )
        
        # Initialize providers
        self.providers: Dict[str, AIProvider] = {}
        self._initialize_providers()
        
        # Set default provider
        default_provider_name = self.config.get("default_provider", "gemini")
        self.default_provider = self.providers.get(default_provider_name)
        
        if not self.default_provider:
            self.logger.log_warning(
                f"Default provider '{default_provider_name}' not available. "
                f"Using first available provider."
            )
            self.default_provider = next(iter(self.providers.values()), None)
        
        if not self.default_provider:
            self.logger.log_error(
                "No AI providers available",
                "initialization_error",
                {"configured_providers": list(self.providers.keys())}
            )
    
    def _initialize_providers(self) -> None:
        """Initialize all configured AI providers."""
        # Initialize Gemini provider
        try:
            gemini_config = self.config.get_provider_config("gemini")
            if gemini_config.get("api_key"):
                provider_config = AIProviderConfig(
                    api_key=gemini_config["api_key"],
                    model=gemini_config.get("model", "gemini-pro"),
                    temperature=gemini_config.get("temperature", 0.7),
                    max_tokens=gemini_config.get("max_tokens")
                )
                self.providers["gemini"] = GeminiProvider(provider_config)
                self.logger.log_info("Gemini provider initialized successfully")
        except Exception as e:
            self.logger.log_warning(f"Failed to initialize Gemini provider: {str(e)}")
        
        # Initialize OpenAI provider
        try:
            openai_config = self.config.get_provider_config("openai")
            if openai_config.get("api_key"):
                provider_config = AIProviderConfig(
                    api_key=openai_config["api_key"],
                    model=openai_config.get("model", "gpt-3.5-turbo"),
                    temperature=openai_config.get("temperature", 0.7),
                    max_tokens=openai_config.get("max_tokens")
                )
                self.providers["gpt"] = GPTProvider(provider_config)
                self.logger.log_info("GPT provider initialized successfully")
        except Exception as e:
            self.logger.log_warning(f"Failed to initialize GPT provider: {str(e)}")
    
    async def process_request(
        self,
        request: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        provider_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a voice assistant request.
        
        Args:
            request: User request/question
            context: Additional context (e.g., user info, location, financial data)
            conversation_history: Previous conversation messages
            provider_name: Specific provider to use (defaults to configured default)
            
        Returns:
            Dictionary containing response and metadata
        """
        # Validate input
        if not request or not isinstance(request, str):
            raise ValidationException("Request must be a non-empty string")
        
        # Select provider
        provider = self._select_provider(provider_name)
        
        if not provider:
            error_msg = "No AI provider available"
            self.logger.log_error(error_msg, "provider_error")
            return {
                "success": False,
                "error": error_msg,
                "request": request
            }
        
        try:
            # Generate response
            self.logger.log_info(f"Processing request with {provider.get_provider_name()} provider")
            response = await provider.generate_response(request, context, conversation_history)
            
            # Log interaction
            self.logger.log_interaction(
                request=request,
                response=response,
                provider=provider.get_provider_name(),
                metadata={
                    "context": context,
                    "has_history": bool(conversation_history)
                }
            )
            
            return {
                "success": True,
                "response": response,
                "provider": provider.get_provider_name(),
                "request": request
            }
            
        except ProviderException as e:
            self.logger.log_error(
                str(e),
                "provider_error",
                {"provider": provider.get_provider_name(), "request": request}
            )
            return {
                "success": False,
                "error": str(e),
                "provider": provider.get_provider_name(),
                "request": request
            }
        except Exception as e:
            self.logger.log_error(
                str(e),
                "unexpected_error",
                {"provider": provider.get_provider_name(), "request": request}
            )
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "provider": provider.get_provider_name() if provider else "unknown",
                "request": request
            }
    
    def _select_provider(self, provider_name: Optional[str] = None) -> Optional[AIProvider]:
        """
        Select AI provider to use.
        
        Args:
            provider_name: Specific provider name, or None for default
            
        Returns:
            Selected provider or None
        """
        if provider_name:
            provider = self.providers.get(provider_name)
            if not provider:
                self.logger.log_warning(
                    f"Requested provider '{provider_name}' not available. "
                    f"Falling back to default."
                )
                return self.default_provider
            return provider
        
        return self.default_provider
    
    def get_available_providers(self) -> List[str]:
        """
        Get list of available provider names.
        
        Returns:
            List of provider names
        """
        return list(self.providers.keys())
    
    def switch_default_provider(self, provider_name: str) -> bool:
        """
        Switch the default provider.
        
        Args:
            provider_name: Name of provider to set as default
            
        Returns:
            True if successful, False otherwise
        """
        provider = self.providers.get(provider_name)
        if provider:
            self.default_provider = provider
            self.logger.log_info(f"Default provider switched to: {provider_name}")
            return True
        
        self.logger.log_warning(f"Cannot switch to unavailable provider: {provider_name}")
        return False
