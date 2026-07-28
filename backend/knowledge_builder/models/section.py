from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Section:
    """
    Represents a resume section.

    Examples
    --------
    Skills
    Experience
    Education
    Projects
    """

    id: str

    name: str

    description: str = ""

    aliases: list[str] = field(
        default_factory=list,
    )

    recommended_order: int = 0

    required: bool = False

    multiple_allowed: bool = False