"""
Authentication and authorization exceptions.
"""

from __future__ import annotations

from app.core.exceptions.base import DomainError


class AuthenticationError(DomainError):
    """
    Base exception for authentication-related errors.
    """


class AuthorizationError(DomainError):
    """
    Base exception for authorization-related errors.
    """


class InvalidCredentialsError(AuthenticationError):
    """
    Raised when user credentials are invalid.
    """


class InvalidTokenError(AuthenticationError):
    """
    Raised when an access or refresh token is invalid.
    """


class ExpiredTokenError(AuthenticationError):
    """
    Raised when an authentication token has expired.
    """


class TokenGenerationError(AuthenticationError):
    """
    Raised when a token cannot be generated.
    """


class TokenVerificationError(AuthenticationError):
    """
    Raised when token verification fails.
    """


class PermissionDeniedError(AuthorizationError):
    """
    Raised when the current user lacks sufficient permissions.
    """


class AccountDisabledError(AuthenticationError):
    """
    Raised when an account is disabled or inactive.
    """


class AuthenticationConfigurationError(AuthenticationError):
    """
    Raised when authentication configuration is invalid.
    """