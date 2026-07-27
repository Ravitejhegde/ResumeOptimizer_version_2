from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class RoleProfile:
    """
    Represents the primary role detected
    from the Job Description.
    """

    role: str

    confidence: float

    categories: list[str] = field(
        default_factory=list
    )

    primary_skills: list[str] = field(
        default_factory=list
    )

    secondary_skills: list[str] = field(
        default_factory=list
    )




