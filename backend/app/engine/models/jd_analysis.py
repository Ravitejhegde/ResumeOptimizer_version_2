from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class JDAnalysis:
    """
    Structured Job Description analysis.

    This model represents everything extracted
    from a job description.

    Initially only skills are populated.
    More fields will be filled as the engine
    evolves.
    """

    # -----------------------------------------
    # Role
    # -----------------------------------------

    role: str | None = None

    role_family: str | None = None

    # -----------------------------------------
    # Experience
    # -----------------------------------------

    minimum_experience: float | None = None

    preferred_experience: float | None = None

    # -----------------------------------------
    # Skills
    # -----------------------------------------

    required_skills: list[str] = field(
        default_factory=list
    )

    preferred_skills: list[str] = field(
        default_factory=list
    )

    # -----------------------------------------
    # Future
    # -----------------------------------------

    responsibilities: list[str] = field(
        default_factory=list
    )

    qualifications: list[str] = field(
        default_factory=list
    )

    keywords: list[str] = field(
        default_factory=list
    )




