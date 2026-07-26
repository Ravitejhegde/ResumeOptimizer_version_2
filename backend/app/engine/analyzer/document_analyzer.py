from __future__ import annotations

from app.engine.analyzer.ats_analyzer import ATSAnalyzer
from app.engine.analyzer.keyword_analyzer import KeywordAnalyzer
from app.engine.analyzer.structure_analyzer import (
    StructureAnalyzer,
)
from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.models.document import Document


class DocumentAnalyzer:
    """
    ResumeOptimizer V3

    Central analysis coordinator.

    This class orchestrates all analyzers and
    returns a complete understanding of the resume.

    It NEVER modifies the document.
    """

    def __init__(
        self,
        knowledge: KnowledgeBase,
    ) -> None:

        self._keyword_analyzer = KeywordAnalyzer(
            knowledge
        )

        self._structure_analyzer = (
            StructureAnalyzer()
        )

        self._ats_analyzer = ATSAnalyzer()

    def analyze(
        self,
        document: Document,
    ) -> dict:

        keywords = (
            self._keyword_analyzer.analyze(
                document
            )
        )

        structure = (
            self._structure_analyzer.analyze(
                document
            )
        )

        ats = (
            self._ats_analyzer.analyze(
                document
            )
        )

        return {

            "keywords": keywords,

            "structure": structure,

            "ats": ats,

        }