from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.analysis.ats_analysis import (
    ATSAnalysis,
)
from app.engine.models.analysis.comparison_analysis import (
    ComparisonAnalysis,
)
from app.engine.models.analysis.jd_analysis import (
    JDAnalysis,
)
from app.engine.models.analysis.keyword_analysis import (
    KeywordAnalysis,
)
from app.engine.models.analysis.structure_analysis import (
    StructureAnalysis,
)
from app.engine.models.intelligence.optimization_strategy import (
    OptimizationStrategy,
)
from app.engine.models.intelligence.role_profile import (
    RoleProfile,
)
from app.engine.models.intelligence.skill_gap import (
    SkillGap,
)


@dataclass(slots=True)
class AnalysisResult:
    """
    Master analysis object produced by the Analyzer.

    This is the contract between:

        Analyzer
            ↓
        Intelligence Engine
            ↓
        Planner
            ↓
        Optimizer

    It contains all semantic understanding
    extracted from a resume and optional
    job description.
    """

    # --------------------------------------------------
    # Source Reference
    # --------------------------------------------------

    document_id: str | None = None

    # --------------------------------------------------
    # Resume Analysis
    # --------------------------------------------------

    ats: ATSAnalysis = field(
        default_factory=ATSAnalysis,
    )

    keywords: KeywordAnalysis = field(
        default_factory=KeywordAnalysis,
    )

    structure: StructureAnalysis = field(
        default_factory=StructureAnalysis,
    )

    # --------------------------------------------------
    # Job Description Analysis
    # --------------------------------------------------

    job_description: JDAnalysis | None = None

    # --------------------------------------------------
    # Skill Comparison
    # --------------------------------------------------

    comparison: ComparisonAnalysis = field(
        default_factory=ComparisonAnalysis,
    )

    # --------------------------------------------------
    # Intelligence Layer
    # --------------------------------------------------

    role: RoleProfile | None = None

    skill_gap: SkillGap | None = None

    optimization_strategy: (
        OptimizationStrategy | None
    ) = None

    # --------------------------------------------------
    # Explainability
    # --------------------------------------------------

    confidence: float = 0.0

    warnings: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @property
    def has_job_description(
        self,
    ) -> bool:

        return self.job_description is not None

    @property
    def matched_skill_count(
        self,
    ) -> int:

        return len(
            self.comparison.matched
        )

    @property
    def missing_skill_count(
        self,
    ) -> int:

        return len(
            self.comparison.missing
        )