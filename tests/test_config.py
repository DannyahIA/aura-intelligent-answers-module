"""Tests for configuration management."""

import pytest
import json
import os
from pathlib import Path
from aura_ia.utils.config import Config
from aura_ia.utils.exceptions import ConfigException


class TestConfig:
    """Test suite for Config class."""
    
    def test_config_from_env(self):
        """Test configuration loading from environment variables."""
        # Set environment variables
        os.environ["GEMINI_API_KEY"] = "test_gemini_key"
        os.environ["OPENAI_API_KEY"] = "test_openai_key"
        os.environ["DEFAULT_AI_PROVIDER"] = "gemini"
        
        config = Config()
        
        assert config.get("gemini.api_key") == "test_gemini_key"
        assert config.get("openai.api_key") == "test_openai_key"
        assert config.get("default_provider") == "gemini"
        
        # Cleanup
        del os.environ["GEMINI_API_KEY"]
        del os.environ["OPENAI_API_KEY"]
        del os.environ["DEFAULT_AI_PROVIDER"]
    
    def test_config_get_with_default(self):
        """Test getting config value with default."""
        config = Config()
        
        # Non-existent key should return default
        assert config.get("nonexistent.key", "default_value") == "default_value"
        
        # Existing key should return actual value
        config.set("test.key", "test_value")
        assert config.get("test.key", "default") == "test_value"
    
    def test_config_set(self):
        """Test setting configuration values."""
        config = Config()
        
        config.set("custom.setting", "value")
        assert config.get("custom.setting") == "value"
        
        config.set("nested.deep.setting", 42)
        assert config.get("nested.deep.setting") == 42
    
    def test_config_get_provider_config(self):
        """Test getting provider-specific configuration."""
        os.environ["GEMINI_API_KEY"] = "test_key"
        os.environ["GEMINI_MODEL"] = "gemini-pro"
        
        config = Config()
        provider_config = config.get_provider_config("gemini")
        
        assert provider_config["api_key"] == "test_key"
        assert provider_config["model"] == "gemini-pro"
        
        # Cleanup
        del os.environ["GEMINI_API_KEY"]
        del os.environ["GEMINI_MODEL"]
    
    def test_config_nonexistent_provider(self):
        """Test getting config for non-existent provider."""
        config = Config()
        
        with pytest.raises(ConfigException):
            config.get_provider_config("nonexistent_provider")
    
    def test_config_from_file(self, tmp_path):
        """Test configuration loading from JSON file."""
        # Create temporary config file
        config_file = tmp_path / "config.json"
        config_data = {
            "gemini": {
                "api_key": "file_gemini_key",
                "model": "gemini-pro"
            },
            "default_provider": "gemini"
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        config = Config(config_path=str(config_file))
        
        assert config.get("gemini.api_key") == "file_gemini_key"
        assert config.get("gemini.model") == "gemini-pro"
        assert config.get("default_provider") == "gemini"
    
    def test_config_invalid_json(self, tmp_path):
        """Test configuration with invalid JSON file."""
        config_file = tmp_path / "invalid.json"
        config_file.write_text("{ invalid json }")
        
        with pytest.raises(ConfigException):
            Config(config_path=str(config_file))
    
    def test_config_missing_file(self):
        """Test configuration with missing file."""
        with pytest.raises(ConfigException):
            Config(config_path="/nonexistent/path/config.json")
