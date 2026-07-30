"""
Storage-related exceptions.
"""

from __future__ import annotations

from app.core.exceptions.base import DomainError


class StorageError(DomainError):
    """
    Base exception for all storage-related errors.
    """


class StorageConnectionError(StorageError):
    """
    Raised when a storage provider cannot be reached.
    """


class StorageConfigurationError(StorageError):
    """
    Raised when storage configuration is invalid.
    """


class StorageInitializationError(StorageError):
    """
    Raised when the storage service fails to initialize.
    """


class FileNotFoundError(StorageError):
    """
    Raised when a requested file cannot be found.
    """


class FileAlreadyExistsError(StorageError):
    """
    Raised when attempting to create a file that already exists.
    """


class FileReadError(StorageError):
    """
    Raised when a file cannot be read.
    """


class FileWriteError(StorageError):
    """
    Raised when a file cannot be written.
    """


class FileDeleteError(StorageError):
    """
    Raised when a file cannot be deleted.
    """


class FileUploadError(StorageError):
    """
    Raised when a file upload fails.
    """


class FileDownloadError(StorageError):
    """
    Raised when a file download fails.
    """


class InvalidFileTypeError(StorageError):
    """
    Raised when an unsupported file type is provided.
    """


class InvalidFileFormatError(StorageError):
    """
    Raised when a file format is invalid or corrupted.
    """


class FileSizeLimitExceededError(StorageError):
    """
    Raised when a file exceeds the allowed size limit.
    """