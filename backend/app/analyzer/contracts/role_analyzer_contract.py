"""
app.analyzer.contracts.role_analyzer_contract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contract for RoleAnalyzer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.analyzer.models.document_model import (
    DocumentModel,
)


class RoleAnalyzerContract(ABC):
    """
    Contract for role analyzers.
    """

    @abstractmethod
    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:
        """
        Analyze a document and populate roles.
        """
        raise NotImplementedError