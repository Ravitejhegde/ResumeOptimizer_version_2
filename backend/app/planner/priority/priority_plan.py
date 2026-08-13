"""
app.planner.priority.priority_plan
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the prioritized optimization tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.planner.priority.priority_item import (
    PriorityItem,
)


@dataclass(slots=True)
class PriorityPlan:
    """
    Collection of prioritized optimization items.
    """

    items: list[PriorityItem] = field(
        default_factory=list
    )

    @property
    def critical(self) -> list[PriorityItem]:
        return [
            item
            for item in self.items
            if item.priority_level == "critical"
        ]

    @property
    def high(self) -> list[PriorityItem]:
        return [
            item
            for item in self.items
            if item.priority_level == "high"
        ]

    @property
    def medium(self) -> list[PriorityItem]:
        return [
            item
            for item in self.items
            if item.priority_level == "medium"
        ]

    @property
    def low(self) -> list[PriorityItem]:
        return [
            item
            for item in self.items
            if item.priority_level == "low"
        ]

    def sort(self) -> None:
        self.items.sort(
            key=lambda item: item.priority_score,
            reverse=True,
        )