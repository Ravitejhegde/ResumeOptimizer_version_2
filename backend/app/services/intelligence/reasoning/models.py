from dataclasses import dataclass, field


# -----------------------------------------
# Skill Gap
# -----------------------------------------

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

    # Importance (0-100)
    priority: int

    # Confidence (0-100)
    confidence: int

    # Required by Job Description?
    required: bool

    # Why is it missing?
    reason: str

    # ExactMatch / AliasMatch / SynonymMatch / RelatedTechnology
    matched_by: str

    # Similar technologies already in resume
    related_skills: list[str] = field(
        default_factory=list
    )

    # Planner recommendation
    recommendation: str = ""


# -----------------------------------------
# Recommendation
# -----------------------------------------

@dataclass
class Recommendation:

    title: str

    description: str

    priority: int


# -----------------------------------------
# Risk
# -----------------------------------------

@dataclass
class Risk:
    """
    Represents one weakness in the resume.
    """

    title: str

    description: str

    severity: int

    recommendation: str = ""


# -----------------------------------------
# Reasoning Result
# -----------------------------------------

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