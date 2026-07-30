"""
Knowledge platform exceptions.
"""

from __future__ import annotations

from app.core.exceptions.base import DomainError


class KnowledgeError(DomainError):
    """
    Base exception for all knowledge platform errors.
    """


class KnowledgeInitializationError(KnowledgeError):
    """
    Raised when the knowledge platform fails to initialize.
    """


class KnowledgeConfigurationError(KnowledgeError):
    """
    Raised when knowledge configuration is invalid.
    """


class KnowledgeSourceError(KnowledgeError):
    """
    Raised when a knowledge source cannot be accessed.
    """


class KnowledgeLoadingError(KnowledgeError):
    """
    Raised when knowledge data cannot be loaded.
    """


class KnowledgeBuildError(KnowledgeError):
    """
    Raised when knowledge graph or knowledge base construction fails.
    """


class KnowledgeValidationError(KnowledgeError):
    """
    Raised when knowledge integrity validation fails.
    """


class KnowledgeIndexError(KnowledgeError):
    """
    Raised when indexing knowledge fails.
    """


class KnowledgeSearchError(KnowledgeError):
    """
    Raised when a knowledge lookup or search fails.
    """


class KnowledgeCacheError(KnowledgeError):
    """
    Raised when reading from or writing to the knowledge cache fails.
    """


class KnowledgeVersionError(KnowledgeError):
    """
    Raised when an incompatible knowledge version is detected.
    """