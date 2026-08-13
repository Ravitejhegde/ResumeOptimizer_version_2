"""
app.analyzer.contracts.section_analyzer_contract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contract for section analyzers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.analyzer.models.document_model import DocumentModel


class SectionAnalyzerContract(ABC):
    """
    Base contract for section analyzers.
    """

    @abstractmethod
    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:
        """
        Detect resume sections and return the updated document.
        """
        raise NotImplementedError