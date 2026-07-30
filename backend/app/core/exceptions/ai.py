"""
AI-related exceptions.
"""

from __future__ import annotations

from app.core.exceptions.base import DomainError


class AIError(DomainError):
    """
    Base exception for all AI-related errors.
    """


class AIConfigurationError(AIError):
    """
    Raised when AI provider configuration is invalid.
    """


class AIInitializationError(AIError):
    """
    Raised when an AI provider fails to initialize.
    """


class AIConnectionError(AIError):
    """
    Raised when communication with an AI provider fails.
    """


class AIAuthenticationError(AIError):
    """
    Raised when authentication with an AI provider fails.
    """


class AIRateLimitError(AIError):
    """
    Raised when the AI provider rate limit is exceeded.
    """


class AIRequestError(AIError):
    """
    Raised when an AI request cannot be completed.
    """


class AIResponseError(AIError):
    """
    Raised when an invalid or incomplete AI response is received.
    """


class AIModelError(AIError):
    """
    Raised when the requested AI model is unavailable or unsupported.
    """


class AITimeoutError(AIError):
    """
    Raised when an AI request exceeds the allowed timeout.
    """


class AITokenLimitError(AIError):
    """
    Raised when the token limit is exceeded.
    """


class AIGenerationError(AIError):
    """
    Raised when AI content generation fails.
    """