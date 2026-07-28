from __future__ import annotations

from dataclasses import dataclass

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

    This object is the only thing passed to the
    Intelligence Engine and Planner.
    """

    ats: ATSAnalysis

    keywords: KeywordAnalysis

    structure: StructureAnalysis

    job_description: JDAnalysis

    comparison: ComparisonAnalysis

    role: RoleProfile | None = None

    skill_gap: SkillGap | None = None

    optimization_strategy: (
        OptimizationStrategy | None
    ) = None
