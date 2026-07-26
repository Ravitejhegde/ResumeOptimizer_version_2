from __future__ import annotations

from app.engine.analyzer.ats_analyzer import (
    ATSAnalyzer,
)
from app.engine.analyzer.keyword_analyzer import (
    KeywordAnalyzer,
)
from app.engine.analyzer.structure_analyzer import (
    StructureAnalyzer,
)
from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.models.analysis_result import (
    AnalysisResult,
    StructureAnalysisResult,
)
from app.engine.models.document import (
    Document,
)


class DocumentAnalyzer:
    """
    ResumeOptimizer V3

    Central analysis coordinator.

    Responsibilities
    ----------------
    - Coordinate analyzers
    - Aggregate analysis results
    - Never modify the document
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
    ) -> AnalysisResult:

        keyword_result = (
            self._keyword_analyzer.analyze(
                document
            )
        )

        structure_result = (
            self._structure_analyzer.analyze(
                document
            )
        )

        ats_result = (
            self._ats_analyzer.analyze(
                document
            )
        )

        if not isinstance(
            structure_result,
            StructureAnalysisResult,
        ):
            structure_result = (
                StructureAnalysisResult(
                    sections=[]
                )
            )

        return AnalysisResult(
            keywords=keyword_result,
            structure=structure_result,
            ats=ats_result,
        )