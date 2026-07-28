from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SectionPlan:
    """
    Planning information for one resume section.

    Produced by the Planner and consumed by
    the Optimizer.
    """

    section: str

    editable: bool = True

    priority: int = 0

    technologies: list[str] = field(
        default_factory=list,
    )

    paragraphs: list[str] = field(
        default_factory=list,
    )

    notes: list[str] = field(
        default_factory=list,
    )
