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

    # -----------------------------
    # Skills Optimizer
    # -----------------------------

    jd_skills: list[str] = field(
        default_factory=list
    )

    selected_skills: list[str] = field(
        default_factory=list
    )

    max_skill_lines: int = 5