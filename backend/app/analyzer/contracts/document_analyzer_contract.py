"""
app.analyzer.contracts.document_analyzer_contract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contract for document analyzers.

A document analyzer reads a resume document and produces
a structured DocumentModel.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.analyzer.models.document_model import DocumentModel


class DocumentAnalyzerContract(ABC):
    """
    Base contract for all document analyzers.
    """

    @abstractmethod
    def analyze(
        self,
        document: Path | str,
    ) -> DocumentModel:
        """
        Analyze a document and return a parsed model.
        """
        raise NotImplementedError