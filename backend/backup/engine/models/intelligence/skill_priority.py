from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SkillPriority:
    """
    Importance of a technology for a target role.

    Produced by Intelligence Engine.

    Used by:
        - SkillGap
        - Planner
        - Promotion Engine
    """

    technology: str

    category: str

    priority: int

    matched: bool = False

    selected: bool = False

    confidence: float = 0.0

    reason: str | None = None