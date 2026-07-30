from __future__ import annotations


class AIError(Exception):
    """
    Base AI provider exception.
    """



class AIConfigurationError(AIError):
    """
    Raised when AI configuration is invalid.
    """



class AIRequestError(AIError):
    """
    Raised when provider request fails.
    """



class AIResponseError(AIError):
    """
    Raised when AI returns invalid response.
    """