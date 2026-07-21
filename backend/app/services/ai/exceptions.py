class AIProviderError(Exception):
    """Base AI provider exception."""
    pass


class AIConfigurationError(AIProviderError):
    """Raised when AI configuration is invalid."""
    pass


class AIRequestError(AIProviderError):
    """Raised when the AI request fails."""
    pass


class AIResponseError(AIProviderError):
    """Raised when the AI returns an invalid response."""
    pass