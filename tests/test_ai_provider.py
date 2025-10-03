"""Tests for AI provider base class."""

import pytest
from aura_ia.core.ai_provider import AIProvider, AIProviderConfig


class MockProvider(AIProvider):
    """Mock provider for testing."""
    
    async def generate_response(self, prompt, context=None, conversation_history=None):
        return f"Mock response to: {prompt}"
    
    def get_provider_name(self):
        return "mock"
    
    def is_available(self):
        return True


class TestAIProviderConfig:
    """Test suite for AIProviderConfig."""
    
    def test_config_creation(self):
        """Test basic config creation."""
        config = AIProviderConfig(
            api_key="test_key",
            model="test_model"
        )
        
        assert config.api_key == "test_key"
        assert config.model == "test_model"
        assert config.temperature == 0.7
        assert config.max_tokens is None
        assert config.additional_params == {}
    
    def test_config_with_optional_params(self):
        """Test config with optional parameters."""
        config = AIProviderConfig(
            api_key="test_key",
            model="test_model",
            temperature=0.9,
            max_tokens=2048,
            additional_params={"param": "value"}
        )
        
        assert config.temperature == 0.9
        assert config.max_tokens == 2048
        assert config.additional_params == {"param": "value"}


class TestAIProvider:
    """Test suite for AIProvider base class."""
    
    def test_provider_initialization(self):
        """Test provider initialization."""
        config = AIProviderConfig(api_key="test_key", model="test_model")
        provider = MockProvider(config)
        
        assert provider.config == config
        assert provider.get_provider_name() == "mock"
        assert provider.is_available() is True
    
    def test_provider_missing_api_key(self):
        """Test provider with missing API key."""
        config = AIProviderConfig(api_key="", model="test_model")
        
        with pytest.raises(ValueError, match="requires an API key"):
            MockProvider(config)
    
    def test_provider_missing_model(self):
        """Test provider with missing model."""
        config = AIProviderConfig(api_key="test_key", model="")
        
        with pytest.raises(ValueError, match="requires a model name"):
            MockProvider(config)
    
    @pytest.mark.asyncio
    async def test_generate_response(self):
        """Test generate_response method."""
        config = AIProviderConfig(api_key="test_key", model="test_model")
        provider = MockProvider(config)
        
        response = await provider.generate_response("Test prompt")
        assert response == "Mock response to: Test prompt"
