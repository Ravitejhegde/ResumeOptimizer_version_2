from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RoleProfile:
    """
    Detected role information.

    Produced by the Analyzer and consumed by
    the Planner and Optimizer.
    """

    id: str

    name: str

    confidence: float = 0.0

    category: str | None = None

    experience_level: str | None = None

    required_skills: list[str] = field(
        default_factory=list,
    )

    optional_skills: list[str] = field(
        default_factory=list,
    )

    related_roles: list[str] = field(
        default_factory=list,
    )
