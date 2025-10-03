"""Tests for exception classes."""

import pytest
from aura_ia.utils.exceptions import (
    AuraIAException,
    ProviderException,
    ConfigException,
    ValidationException
)


class TestExceptions:
    """Test suite for custom exceptions."""
    
    def test_base_exception(self):
        """Test base AuraIAException."""
        exc = AuraIAException("Test message")
        assert str(exc) == "Test message"
        assert exc.message == "Test message"
        assert exc.details == {}
    
    def test_base_exception_with_details(self):
        """Test AuraIAException with details."""
        details = {"key": "value", "number": 42}
        exc = AuraIAException("Test message", details=details)
        
        assert exc.message == "Test message"
        assert exc.details == details
        assert exc.details["key"] == "value"
        assert exc.details["number"] == 42
    
    def test_provider_exception(self):
        """Test ProviderException."""
        exc = ProviderException("Provider error")
        assert isinstance(exc, AuraIAException)
        assert str(exc) == "Provider error"
    
    def test_config_exception(self):
        """Test ConfigException."""
        exc = ConfigException("Config error")
        assert isinstance(exc, AuraIAException)
        assert str(exc) == "Config error"
    
    def test_validation_exception(self):
        """Test ValidationException."""
        exc = ValidationException("Validation error")
        assert isinstance(exc, AuraIAException)
        assert str(exc) == "Validation error"
    
    def test_exception_inheritance(self):
        """Test exception inheritance chain."""
        assert issubclass(ProviderException, AuraIAException)
        assert issubclass(ConfigException, AuraIAException)
        assert issubclass(ValidationException, AuraIAException)
        assert issubclass(AuraIAException, Exception)
