from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TechnologyCategory:
    """
    Technologies grouped by category.
    """

    id: str

    name: str

    technologies: list[str] = field(
        default_factory=list,
    )
