from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.optimization_strategy import (
    OptimizationStrategy,
)
from app.engine.models.role_profile import (
    RoleProfile,
)
from app.engine.models.skill_gap import (
    SkillGap,
)
from app.engine.models.skill_priority import (
    SkillPriority,
)
from app.engine.models.technology_category import (
    TechnologyCategory,
)


@dataclass(slots=True)
class KeywordAnalysisResult:
    """
    Result produced by KeywordAnalyzer.
    """

    detected_skills: list[str] = field(
        default_factory=list
    )

    normalized_skills: list[str] = field(
        default_factory=list
    )

    categorized_skills: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict
    )

    duplicate_skills: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True)
class ATSAnalysisResult:
    """
    Result produced by ATSAnalyzer.
    """

    score: int

    required_sections: list[str]

    missing_sections: list[str]

    has_tables: bool

    paragraph_count: int

    empty_paragraphs: int

    is_ats_friendly: bool


@dataclass(slots=True)
class StructureAnalysisResult:
    """
    Result produced by StructureAnalyzer.
    """

    sections: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True)
class AnalysisResult:
    """
    Complete document analysis.

    Produced by DocumentAnalyzer and
    consumed by the Planner.
    """

    # Existing analyzers

    keywords: KeywordAnalysisResult

    structure: StructureAnalysisResult

    ats: ATSAnalysisResult

    # Intelligence layer

    optimization_strategy: OptimizationStrategy

    role_profile: RoleProfile | None = None

    technology_categories: list[
        TechnologyCategory
    ] = field(
        default_factory=list
    )

    prioritized_skills: list[
        SkillPriority
    ] = field(
        default_factory=list
    )

    skill_gap: SkillGap | None = None