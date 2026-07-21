from dataclasses import dataclass, field


@dataclass
class SkillGap:

    name: str

    priority: int

    required: bool

    reason: str


@dataclass
class Recommendation:

    title: str

    description: str

    priority: int


@dataclass
class SkillGap:
    """
    Represents one missing or partially matched
    technology discovered during gap analysis.
    """

    # Technology
    name: str

    # Technology category
    category: str

    # Importance (0–100)
    priority: int

    # Confidence in this gap (0–100)
    confidence: int

    # Is it explicitly required by the JD?
    required: bool

    # Why is it considered a gap?
    reason: str

    # ExactMatch / AliasMatch / SynonymMatch / RelatedTechnology
    matched_by: str

    # Similar technologies already present
    related_skills: list[str] = field(default_factory=list)

    # Recommendation for the planner / AI
    recommendation: str = ""


@dataclass
class ReasoningResult:

    matched: list[str] = field(
        default_factory=list
    )

    missing: list[SkillGap] = field(
        default_factory=list
    )

    extra: list[str] = field(
        default_factory=list
    )

    recommendations: list[Recommendation] = field(
        default_factory=list
    )

    risks: list[Risk] = field(
        default_factory=list
    )