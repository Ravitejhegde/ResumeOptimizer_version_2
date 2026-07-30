"""
Resume analysis exceptions.
"""

from __future__ import annotations

from app.core.exceptions.base import DomainError


class AnalysisError(DomainError):
    """
    Base exception for all analysis-related errors.
    """


class DocumentAnalysisError(AnalysisError):
    """
    Raised when document analysis fails.
    """


class ResumeAnalysisError(AnalysisError):
    """
    Raised when resume analysis fails.
    """


class JobDescriptionAnalysisError(AnalysisError):
    """
    Raised when job description analysis fails.
    """


class ParsingError(AnalysisError):
    """
    Raised when document parsing fails.
    """


class ExtractionError(AnalysisError):
    """
    Raised when required information cannot be extracted.
    """


class ClassificationError(AnalysisError):
    """
    Raised when classification of content fails.
    """


class SkillAnalysisError(AnalysisError):
    """
    Raised when skill analysis fails.
    """


class ExperienceAnalysisError(AnalysisError):
    """
    Raised when experience analysis fails.
    """


class EducationAnalysisError(AnalysisError):
    """
    Raised when education analysis fails.
    """


class ATSAnalysisError(AnalysisError):
    """
    Raised when ATS scoring or evaluation fails.
    """