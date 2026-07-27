from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.models.skill_priority import SkillPriority


@dataclass(slots=True)
class SkillGap:

    matched: list[SkillPriority] = field(
        default_factory=list
    )

    missing: list[SkillPriority] = field(
        default_factory=list
    )

    extra: list[str] = field(
        default_factory=list
    )

    ignored: list[str] = field(
        default_factory=list
    )

    score: float = 0.0