"""
app.analyzer.contracts.technology_analyzer_contract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contract for technology analyzers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.analyzer.models.document_model import DocumentModel


class TechnologyAnalyzerContract(ABC):
    """
    Base contract for technology analyzers.
    """

    @abstractmethod
    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:
        """
        Detect technologies inside the document.
        """
        raise NotImplementedError