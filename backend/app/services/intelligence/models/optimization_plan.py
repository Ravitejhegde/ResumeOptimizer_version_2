from dataclasses import dataclass, field

from .skill_decision import SkillDecision


@dataclass
class OptimizationPlan:
    """
    Final optimization instructions generated
    by the Intelligence Engine.
    """

    source_role: str = ""

    target_role: str = ""

    keep: list[SkillDecision] = field(
        default_factory=list
    )

    remove: list[SkillDecision] = field(
        default_factory=list
    )

    add: list[SkillDecision] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )