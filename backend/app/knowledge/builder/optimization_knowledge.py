"""
app.knowledge.builder.optimization_knowledge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Structured knowledge prepared for resume optimization.

The Knowledge Builder prepares domain knowledge and
user-authorized optimization skills for the Planner.
It does not generate resume text or make rewrite decisions.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class KnowledgeCategory:
    """
    Role-specific presentation category.
    """

    id: str

    name: str

    technologies: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True)
class OptimizationSkill:
    """
    One skill prepared for optimization.
    """

    name: str

    canonical: str

    taxonomy_category: str

    presentation_category: str

    role_relevance: str = ""

    matched: bool = False

    user_selected: bool = False


@dataclass(slots=True)
class OptimizationKnowledge:
    """
    Knowledge prepared by the Knowledge Builder.

    This object contains domain knowledge and authorization
    information required by the Planner.
    """

    role_id: str = ""

    role_name: str = ""

    categories: list[KnowledgeCategory] = field(
        default_factory=list
    )

    matched_skills: list[str] = field(
        default_factory=list
    )

    selected_missing_skills: list[str] = field(
        default_factory=list
    )

    optimization_skills: list[OptimizationSkill] = field(
        default_factory=list
    )

    @property
    def skill_names(self) -> list[str]:
        """
        Return the final optimization skill names.
        """

        return [
            skill.name
            for skill in self.optimization_skills
        ]