from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.intelligence.skill_priority import (
    SkillPriority,
)


@dataclass(slots=True)
class SkillGap:
    """
    Skill gap between resume and
    target job description.

    Represents intelligence output,
    not optimization execution.
    """

    # --------------------------------------------------
    # Target Context
    # --------------------------------------------------

    target_role: str | None = None

    # --------------------------------------------------
    # Skills
    # --------------------------------------------------

    matched: list[SkillPriority] = field(
        default_factory=list,
    )

    missing: list[SkillPriority] = field(
        default_factory=list,
    )

    additional: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Scoring
    # --------------------------------------------------

    score: float = 0.0

    # --------------------------------------------------
    # Explainability
    # --------------------------------------------------

    explanations: dict[
        str,
        str,
    ] = field(
        default_factory=dict,
    )