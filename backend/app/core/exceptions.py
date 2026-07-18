class ResumeOptimizerError(Exception):
    """Base exception for the application."""

    pass


class FileValidationError(ResumeOptimizerError):
    """Raised when an uploaded file fails validation."""

    pass


class StorageError(ResumeOptimizerError):
    """Raised when storing a file fails."""

    pass


class ResumeParsingError(ResumeOptimizerError):
    """Raised when a resume cannot be parsed."""

    pass


class ResumeOptimizationError(ResumeOptimizerError):
    """Raised when resume optimization fails."""

    pass