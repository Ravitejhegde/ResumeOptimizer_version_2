"""
Resume optimization exceptions.
"""

from __future__ import annotations

from app.core.exceptions.base import DomainError


class OptimizationError(DomainError):
    """
    Base exception for all resume optimization errors.
    """


class PlannerError(OptimizationError):
    """
    Raised when optimization planning fails.
    """


class SkillMatchingError(OptimizationError):
    """
    Raised when skill matching fails.
    """


class OptimizationStrategyError(OptimizationError):
    """
    Raised when an optimization strategy cannot be created or executed.
    """


class PromptGenerationError(OptimizationError):
    """
    Raised when AI prompt generation fails.
    """


class OptimizationExecutionError(OptimizationError):
    """
    Raised when optimization execution fails.
    """


class ValidationFailureError(OptimizationError):
    """
    Raised when optimized content fails validation.
    """


class WriterError(OptimizationError):
    """
    Raised when writing the optimized document fails.
    """


class LayoutPreservationError(OptimizationError):
    """
    Raised when the original document layout cannot be preserved.
    """


class ContentReplacementError(OptimizationError):
    """
    Raised when optimized content cannot replace the original content safely.
    """


class OptimizationLimitExceededError(OptimizationError):
    """
    Raised when optimization exceeds configured limits.
    """