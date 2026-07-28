from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class JDAnalysis:
    """
    Structured Job Description analysis.
    """

    role: str | None = None

    role_family: str | None = None

    minimum_experience: float | None = None

    preferred_experience: float | None = None

    required_skills: list[str] = field(
        default_factory=list,
    )

    preferred_skills: list[str] = field(
        default_factory=list,
    )

    keywords: list[str] = field(
        default_factory=list,
    )

    responsibilities: list[str] = field(
        default_factory=list,
    )

    qualifications: list[str] = field(
        default_factory=list,
    )
