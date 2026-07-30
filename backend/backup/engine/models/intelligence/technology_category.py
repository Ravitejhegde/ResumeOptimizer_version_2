from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TechnologyCategory:
    """
    Group of technologies belonging to a domain category.

    Used by:

        Knowledge Platform
              ↓
        Intelligence Engine
              ↓
        Skill Analysis

    Example:

        Backend Frameworks
            - FastAPI
            - Django
            - Spring Boot
    """

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    id: str

    name: str

    knowledge_id: str | None = None

    # --------------------------------------------------
    # Description
    # --------------------------------------------------

    description: str | None = None

    # --------------------------------------------------
    # Technologies
    # --------------------------------------------------

    technologies: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def contains(
        self,
        technology: str,
    ) -> bool:

        normalized = technology.lower()

        return any(
            item.lower() == normalized
            for item in self.technologies
        )