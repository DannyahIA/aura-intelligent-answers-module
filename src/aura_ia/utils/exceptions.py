"""Custom exceptions for Aura IA module."""


class AuraIAException(Exception):
    """Base exception for Aura IA module."""
    
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ProviderException(AuraIAException):
    """Exception raised when AI provider encounters an error."""
    pass


class ConfigException(AuraIAException):
    """Exception raised for configuration errors."""
    pass


class ValidationException(AuraIAException):
    """Exception raised for input validation errors."""
    pass
