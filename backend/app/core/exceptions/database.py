"""
Database-related exceptions.
"""

from __future__ import annotations

from app.core.exceptions.base import DomainError


class DatabaseError(DomainError):
    """
    Base exception for all database-related errors.
    """


class DatabaseConnectionError(DatabaseError):
    """
    Raised when a database connection cannot be established.
    """


class DatabaseInitializationError(DatabaseError):
    """
    Raised when the database fails to initialize.
    """


class DatabaseMigrationError(DatabaseError):
    """
    Raised when a database migration fails.
    """


class TransactionError(DatabaseError):
    """
    Raised when a database transaction fails.
    """


class RepositoryError(DatabaseError):
    """
    Raised when a repository operation fails.
    """


class EntityNotFoundError(DatabaseError):
    """
    Raised when a requested database entity does not exist.
    """


class DuplicateEntityError(DatabaseError):
    """
    Raised when attempting to create a duplicate entity.
    """


class ConstraintViolationError(DatabaseError):
    """
    Raised when a database constraint is violated.
    """