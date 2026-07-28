from __future__ import annotations

from dataclasses import dataclass, field

from knowledge_builder.models.technology import (
    Technology,
)


@dataclass(slots=True)
class Category:
    """
    Represents a technology category.

    Example:
        Programming Languages
        Frameworks
        Databases
        Cloud
    """

    id: str

    name: str

    description: str = ""

    technologies: list[Technology] = field(
        default_factory=list,
    )

    tags: list[str] = field(
        default_factory=list,
    )

    def add(
        self,
        technology: Technology,
    ) -> None:

        self.technologies.append(
            technology,
        )

    @property
    def count(
        self,
    ) -> int:

        return len(
            self.technologies,
        )