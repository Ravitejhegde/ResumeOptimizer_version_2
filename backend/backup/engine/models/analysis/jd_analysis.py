from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class JDAnalysis:
    """
    Structured Job Description analysis.

    Produced by Job Description Analyzer.

    Used by:
        - Skill Comparator
        - Intelligence Engine
        - Planner

    Represents the semantic understanding
    of a job description.
    """

    # --------------------------------------------------
    # Role Understanding
    # --------------------------------------------------

    role: str | None = None

    role_family: str | None = None

    confidence: float = 0.0

    # --------------------------------------------------
    # Experience
    # --------------------------------------------------

    minimum_experience: float | None = None

    preferred_experience: float | None = None

    # --------------------------------------------------
    # Skills
    # --------------------------------------------------

    required_skills: list[str] = field(
        default_factory=list,
    )

    preferred_skills: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Skill Intelligence
    # --------------------------------------------------

    skill_categories: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Keywords
    # --------------------------------------------------

    keywords: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Job Content
    # --------------------------------------------------

    responsibilities: list[str] = field(
        default_factory=list,
    )

    qualifications: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Explainability
    # --------------------------------------------------

    entities: dict[
        str,
        list[str],
    ] = field(
        default_factory=dict,
    )

    warnings: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def has_skill(
        self,
        skill: str,
    ) -> bool:

        normalized = skill.lower()

        return any(
            item.lower() == normalized
            for item in (
                self.required_skills
                + self.preferred_skills
            )
        )