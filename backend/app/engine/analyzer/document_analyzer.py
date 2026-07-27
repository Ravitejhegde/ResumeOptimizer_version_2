from __future__ import annotations

from app.engine.analyzer.ats_analyzer import ATSAnalyzer
from app.engine.analyzer.keyword_analyzer import KeywordAnalyzer
from app.engine.analyzer.structure_analyzer import StructureAnalyzer

from app.engine.intelligence.intelligence_engine import (
    IntelligenceEngine,
)

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
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
    Central analysis coordinator.

    Responsibilities
    ----------------
    • Keyword analysis
    • Structure analysis
    • ATS analysis
    • Delegate intelligence building
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._keyword_analyzer = KeywordAnalyzer(
            knowledge
        )

        self._structure_analyzer = (
            StructureAnalyzer()
        )

        self._ats_analyzer = ATSAnalyzer()

        self._intelligence = (
            IntelligenceEngine()
        )

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

        if not isinstance(
            structure_result,
            StructureAnalysisResult,
        ):
            structure_result = (
                StructureAnalysisResult(
                    sections=[]
                )
            )

        ats_result = (
            self._ats_analyzer.analyze(
                document
            )
        )

        analysis = AnalysisResult(

            keywords=keyword_result,

            structure=structure_result,

            ats=ats_result,

            optimization_strategy=None,

            role_profile=None,

            technology_categories=[],

            prioritized_skills=[],

            skill_gap=None,

        )

        analysis.optimization_strategy = (
            self._intelligence.build(
                document=document,
                analysis=analysis,
            )
        )

        return analysis




