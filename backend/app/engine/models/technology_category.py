from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TechnologyCategory:
    """
    Represents one technology category
    and the technologies that belong to it.
    """

    name: str

    technologies: list[str] = field(
        default_factory=list
    )




