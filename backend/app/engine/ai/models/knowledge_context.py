from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class KnowledgeContext:
    """
    Structured knowledge provided to AI.

    This model is intentionally flexible.

    Knowledge Builder may provide:
        - skills
        - technology relationships
        - role expectations
        - industry knowledge
        - optimization hints
        - scoring information


    Responsibilities:

        - Carry trusted knowledge data to AI layer.
        - Provide structured context.
        - Avoid raw dictionary dependency.


    Does NOT:

        - Build prompts.
        - Call AI.
        - Optimize resume.
    """


    # --------------------------------------------------
    # Target information
    # --------------------------------------------------

    target_role: str | None = None

    role_family: str | None = None


    # --------------------------------------------------
    # Skill intelligence
    # --------------------------------------------------

    matched_skills: list[str] = field(
        default_factory=list,
    )


    missing_skills: list[str] = field(
        default_factory=list,
    )


    prioritized_skills: list[str] = field(
        default_factory=list,
    )


    # --------------------------------------------------
    # Technology relationships
    # --------------------------------------------------

    technology_map: dict[str, list[str]] = field(
        default_factory=dict,
    )


    skill_categories: dict[str, list[str]] = field(
        default_factory=dict,
    )


    # --------------------------------------------------
    # AI guidance
    # --------------------------------------------------

    role_expectations: list[str] = field(
        default_factory=list,
    )


    optimization_hints: list[str] = field(
        default_factory=list,
    )


    warnings: list[str] = field(
        default_factory=list,
    )


    # --------------------------------------------------
    # Extensible metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def has_missing_skills(
        self,
    ) -> bool:
        """
        Check whether JD gaps exist.
        """

        return bool(
            self.missing_skills
        )



    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store additional knowledge
        without changing schema.
        """

        self.metadata[key] = value



    def all_skills(
        self,
    ) -> list[str]:
        """
        Return combined skill universe.
        """

        return list(
            dict.fromkeys(
                self.matched_skills
                +
                self.missing_skills
                +
                self.prioritized_skills
            )
        )