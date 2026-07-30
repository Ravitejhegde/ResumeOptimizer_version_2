from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RoleProfile:
    """
    Detected role information.

    Produced by the Analyzer and consumed by:

        Analyzer
            ↓
        Intelligence Engine
            ↓
        Planner
            ↓
        Optimizer

    Represents semantic understanding of
    the target professional role.
    """

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    id: str

    name: str

    knowledge_id: str | None = None

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    confidence: float = 0.0

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    category: str | None = None

    experience_level: str | None = None

    # --------------------------------------------------
    # Skills
    # --------------------------------------------------

    required_skills: list[str] = field(
        default_factory=list,
    )

    optional_skills: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Related Roles
    # --------------------------------------------------

    related_roles: list[str] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Explainability
    # --------------------------------------------------

    reasons: list[str] = field(
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
                + self.optional_skills
            )
        )

    def is_confident(
        self,
        threshold: float = 0.7,
    ) -> bool:

        return self.confidence >= threshold