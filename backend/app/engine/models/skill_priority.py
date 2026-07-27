from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SkillPriority:
    """
    Represents one skill together with
    its importance inside the detected role.
    """

    skill: str

    category: str

    priority: int

    selected: bool = False




