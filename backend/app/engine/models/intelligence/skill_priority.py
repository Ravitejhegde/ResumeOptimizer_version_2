from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SkillPriority:
    """
    Importance of a technology for the
    target role.
    """

    technology: str

    category: str

    priority: int

    matched: bool = False

    selected: bool = False
