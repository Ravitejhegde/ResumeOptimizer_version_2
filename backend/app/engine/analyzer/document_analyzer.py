from __future__ import annotations

from app.engine.analyzer.analyzers.ats_analyzer import (
    ATSAnalyzer,
)
from app.engine.analyzer.analyzers.job_description_analyzer import (
    JobDescriptionAnalyzer,
)
from app.engine.analyzer.analyzers.keyword_analyzer import (
    KeywordAnalyzer,
)
from app.engine.analyzer.analyzers.structure_analyzer import (
    StructureAnalyzer,
)
from app.engine.analyzer.comparators.skill_comparator import (
    SkillComparator,
)
from app.engine.models.analysis.analysis_result import (
    AnalysisResult,
)
from app.engine.models.analysis.comparison_analysis import (
    ComparisonAnalysis,
)
from app.engine.models.analysis.jd_analysis import (
    JDAnalysis,
)
from app.engine.models.document.document import (
    Document,
)
from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class DocumentAnalyzer:
    """
    Central orchestrator for all document analysis.

    This class contains NO business logic.

    It simply coordinates all analyzers.
    """

    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:

        self._knowledge = knowledge

        self._ats = ATSAnalyzer()

        self._structure = StructureAnalyzer()

       

        self._keywords = KeywordAnalyzer(
            knowledge,
        )

        self._jd = JobDescriptionAnalyzer(
            knowledge,
        )

        self._comparator = SkillComparator(
            knowledge,
        )

    # --------------------------------------------------

    def analyze(
        self,
        document: Document,
        job_description: str | None = None,
    ) -> AnalysisResult:

        ats = self._ats.analyze(
            document,
        )

        structure = self._structure.analyze(
            document,
        )

        

        keywords = self._keywords.analyze(
            document,
        )

        if job_description:

            jd = self._jd.analyze(
                job_description,
            )

            comparison = self._comparator.compare(
    keywords,
    jd,
)

        else:

            jd = JDAnalysis()

            comparison = ComparisonAnalysis()

        return AnalysisResult(

            ats=ats,

            keywords=keywords,

            structure=structure,

            job_description=jd,

            comparison=comparison,

            role=None,

            skill_gap=None,

            optimization_strategy=None,

        )
