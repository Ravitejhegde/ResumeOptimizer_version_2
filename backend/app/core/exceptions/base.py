"""
Base exception hierarchy for ResumeOptimizer.

Every domain-specific exception in the application should inherit from
ResumeOptimizerError, either directly or indirectly.

This module provides the foundation for consistent error handling across
the entire backend.
"""

from __future__ import annotations

from typing import Any


class ResumeOptimizerError(Exception):
    """
    Root exception for the ResumeOptimizer backend.

    Attributes:
        message:
            Human-readable error message.

        details:
            Optional structured metadata that can be used for logging,
            debugging, or API responses.
    """

    def __init__(
        self,
        message: str = "An unexpected ResumeOptimizer error occurred.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        return self.message


class DomainError(ResumeOptimizerError):
    """
    Base class for all domain-specific errors.

    Examples:
        - KnowledgeError
        - AnalysisError
        - OptimizationError
        - StorageError
        - AIError
    """


class ValidationError(ResumeOptimizerError):
    """
    Raised when validation of business rules or data fails.
    """


class ConfigurationError(ResumeOptimizerError):
    """
    Raised when application configuration is missing or invalid.
    """


class ResourceNotFoundError(ResumeOptimizerError):
    """
    Raised when a required resource cannot be found.
    """


class DependencyError(ResumeOptimizerError):
    """
    Raised when an external dependency or required service is unavailable.
    """


class InitializationError(ResumeOptimizerError):
    """
    Raised when application startup or component initialization fails.
    """