"""
app.analyzer.exceptions.analyzer_errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom exceptions used by the Resume Analyzer.
"""

from __future__ import annotations


class AnalyzerError(Exception):
    """
    Base exception for all analyzer errors.
    """


class DocumentAnalysisError(AnalyzerError):
    """
    Raised when a document cannot be analyzed.
    """


class UnsupportedDocumentError(DocumentAnalysisError):
    """
    Raised when the document format is unsupported.
    """


class EmptyDocumentError(DocumentAnalysisError):
    """
    Raised when the document contains no readable content.
    """