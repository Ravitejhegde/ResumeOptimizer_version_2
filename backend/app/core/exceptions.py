from __future__ import annotations


class ResumeOptimizerError(Exception):
    """
    Base exception for the application.
    """



# ======================================================
# Configuration
# ======================================================

class ConfigurationError(ResumeOptimizerError):
    """Raised when configuration is invalid."""


# ======================================================
# Validation
# ======================================================

class ValidationError(ResumeOptimizerError):
    """Raised when validation fails."""


class FileValidationError(ValidationError):
    """Raised when an uploaded file fails validation."""


# ======================================================
# Storage
# ======================================================

class StorageError(ResumeOptimizerError):
    """Raised when storage operations fail."""


# ======================================================
# Reader / Parser
# ======================================================

class ReaderError(ResumeOptimizerError):
    """Raised when document reading fails."""


class ResumeParsingError(ReaderError):
    """Raised when a resume cannot be parsed."""


# ======================================================
# Knowledge
# ======================================================

class KnowledgeError(ResumeOptimizerError):
    """Raised when knowledge loading or lookup fails."""


# ======================================================
# Analysis
# ======================================================

class AnalysisError(ResumeOptimizerError):
    """Raised when resume analysis fails."""


# ======================================================
# AI
# ======================================================

class AIError(ResumeOptimizerError):
    """Raised when AI provider fails."""


# ======================================================
# Optimization
# ======================================================

class ResumeOptimizationError(
    ResumeOptimizerError,
):
    """Raised when resume optimization fails."""


# ======================================================
# Database
# ======================================================

class DatabaseError(ResumeOptimizerError):
    """Raised when database operations fail."""


# ======================================================
# Authentication
# ======================================================

class AuthenticationError(
    ResumeOptimizerError,
):
    """Raised when authentication fails."""


class AuthorizationError(
    ResumeOptimizerError,
):
    """Raised when authorization fails."""




