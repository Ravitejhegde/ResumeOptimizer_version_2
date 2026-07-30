from __future__ import annotations


class AIProviderError(Exception):
    """
    Base exception for all AI provider failures.
    """



class AIConfigurationError(AIProviderError):
    """
    Raised when AI provider configuration is invalid.

    Examples:
        - Missing API key
        - Unsupported model
        - Invalid provider settings
    """



class AIRequestError(AIProviderError):
    """
    Raised when an AI request fails.

    Examples:
        - Timeout
        - Network failure
        - Rate limit
        - Provider unavailable
    """



class AIResponseError(AIProviderError):
    """
    Raised when AI returns an invalid response.

    Examples:
        - Invalid JSON
        - Missing required fields
        - Malformed output
    """