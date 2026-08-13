"""
app.knowledge.exceptions.runtime_errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Exceptions used by the Knowledge Runtime.

These exceptions isolate runtime failures from the rest of the
application.
"""

from __future__ import annotations


class KnowledgeRuntimeError(Exception):
    """
    Base exception for all runtime errors.
    """


class KnowledgeNotLoadedError(KnowledgeRuntimeError):
    """
    Raised when runtime knowledge has not been loaded.
    """


class KnowledgeLoadError(KnowledgeRuntimeError):
    """
    Raised when loading the knowledge package fails.
    """


class InvalidKnowledgePackageError(KnowledgeRuntimeError):
    """
    Raised when the exported knowledge package is invalid.
    """