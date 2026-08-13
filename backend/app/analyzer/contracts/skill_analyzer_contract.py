"""
app.analyzer.contracts.skill_analyzer_contract
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contract for skill analyzers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.analyzer.models.document_model import (
    DocumentModel,
)


class SkillAnalyzerContract(ABC):
    """
    Base contract for skill analyzers.
    """

    @abstractmethod
    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:
        """
        Detect engineering skills.
        """
        raise NotImplementedError