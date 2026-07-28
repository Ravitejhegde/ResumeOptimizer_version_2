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
from app.engine.intelligence.intelligence_engine import (
    IntelligenceEngine,
)
from app.engine.models.analysis_result import (
    AnalysisResult,
)
from app.engine.models.document import (
    Document,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class DocumentAnalyzer:
    """
    Coordinates all document analyzers.

    Responsibilities
    ----------------
    • Keyword analysis
    • Structure analysis
    • ATS analysis
    • Build optimization intelligence

    Never performs analysis itself.
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._keyword_analyzer = KeywordAnalyzer(
            knowledge,
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

        keywords = (
            self._keyword_analyzer.analyze(
                document,
            )
        )

        structure = (
            self._structure_analyzer.analyze(
                document,
            )
        )

        ats = (
            self._ats_analyzer.analyze(
                document,
            )
        )

        analysis = AnalysisResult(

            keywords=keywords,

            structure=structure,

            ats=ats,

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