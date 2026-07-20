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
class Risk:

    title: str

    level: str

    description: str


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