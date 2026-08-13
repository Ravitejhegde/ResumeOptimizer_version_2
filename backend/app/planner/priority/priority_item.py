"""
app.planner.priority.priority_item
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents one prioritized optimization task.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PriorityItem:
    """
    Represents one optimization priority.
    """

    id: str = ""

    type: str = ""

    title: str = ""

    description: str = ""

    priority_level: str = "medium"

    priority_score: float = 0.0

    reason: str = ""

    affected_sections: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )