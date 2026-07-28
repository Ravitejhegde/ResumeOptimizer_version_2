from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.intelligence.skill_priority import (
    SkillPriority,
)


@dataclass(slots=True)
class SkillGap:
    """
    Skill gap between resume and
    job description.
    """

    matched: list[SkillPriority] = field(
        default_factory=list,
    )

    missing: list[SkillPriority] = field(
        default_factory=list,
    )

    additional: list[str] = field(
        default_factory=list,
    )

    score: float = 0.0
