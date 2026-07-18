from dataclasses import dataclass, field


@dataclass(slots=True)
class OptimizationPlan:
    """
    Tells the AI exactly where selected skills
    should be inserted.
    """

    summary: list[str] = field(default_factory=list)

    skills: list[str] = field(default_factory=list)

    experience: list[str] = field(default_factory=list)

    projects: list[str] = field(default_factory=list)