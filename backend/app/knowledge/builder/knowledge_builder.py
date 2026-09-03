from __future__ import annotations

from app.knowledge.builder.optimization_knowledge import (
    KnowledgeCategory,
    OptimizationKnowledge,
    OptimizationSkill,
)


class KnowledgeBuilder:
    """
    Builds structured optimization knowledge from the
    existing Knowledge Platform.

    Responsibilities:
    - resolve role knowledge
    - resolve role-specific presentation categories
    - combine matched and user-selected skills
    - normalize skills
    - map skills to taxonomy categories
    - map skills to presentation categories
    - determine role relevance

    This class does not generate resume text.
    """

    def __init__(
        self,
        knowledge_manager,
    ) -> None:

        self._knowledge = knowledge_manager

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def build(
        self,
        role_id: str,
        matched_skills: list[str],
        selected_missing_skills: list[str],
    ) -> OptimizationKnowledge:

        role = self._knowledge.role(
            role_id,
        )

        profile = self._knowledge.profile(
            role_id,
        )

        if role is None:
            raise ValueError(
                f"Unknown role: {role_id}"
            )

        if profile is None:
            raise ValueError(
                f"Knowledge profile not found for role: {role_id}"
            )

        categories = self._build_categories(
            profile,
        )

        role_relevance = self._build_role_relevance(
            role,
        )

        optimization_skills = self._build_skills(
            categories=categories,
            role_relevance=role_relevance,
            matched_skills=matched_skills,
            selected_missing_skills=selected_missing_skills,
        )

        return OptimizationKnowledge(
            role_id=role_id,
            role_name=role.get(
                "title",
                role_id,
            ),
            categories=categories,
            matched_skills=self._unique(
                matched_skills,
            ),
            selected_missing_skills=self._unique(
                selected_missing_skills,
            ),
            optimization_skills=optimization_skills,
        )

    # --------------------------------------------------
    # Categories
    # --------------------------------------------------

    def _build_categories(
        self,
        profile: dict,
    ) -> list[KnowledgeCategory]:

        categories: list[KnowledgeCategory] = []

        for category in profile.get(
            "categories",
            [],
        ):

            categories.append(
                KnowledgeCategory(
                    id=category.get(
                        "id",
                        "",
                    ),
                    name=category.get(
                        "name",
                        "",
                    ),
                    technologies=list(
                        category.get(
                            "technologies",
                            [],
                        )
                    ),
                )
            )

        return categories

    # --------------------------------------------------
    # Role relevance
    # --------------------------------------------------

    @staticmethod
    def _build_role_relevance(
        role: dict,
    ) -> dict[str, str]:

        relevance: dict[str, str] = {}

        for skill in role.get(
            "required",
            [],
        ):

            relevance[
                skill.lower()
            ] = "required"

        for skill in role.get(
            "preferred",
            [],
        ):

            key = skill.lower()

            if key not in relevance:
                relevance[key] = "preferred"

        for skill in role.get(
            "nice_to_have",
            [],
        ):

            key = skill.lower()

            if key not in relevance:
                relevance[key] = "nice_to_have"

        return relevance

    # --------------------------------------------------
    # Skills
    # --------------------------------------------------

    def _build_skills(
        self,
        categories: list[KnowledgeCategory],
        role_relevance: dict[str, str],
        matched_skills: list[str],
        selected_missing_skills: list[str],
    ) -> list[OptimizationSkill]:

        matched = {
            self._knowledge.normalize(
                skill,
            ): skill
            for skill in matched_skills
        }

        selected = {
            self._knowledge.normalize(
                skill,
            ): skill
            for skill in selected_missing_skills
        }

        final_skills: dict[str, OptimizationSkill] = {}

        for canonical, original_name in matched.items():

            final_skills[canonical] = (
                self._create_skill(
                    name=original_name,
                    canonical=canonical,
                    categories=categories,
                    role_relevance=role_relevance,
                    matched=True,
                    user_selected=False,
                )
            )

        for canonical, original_name in selected.items():

            final_skills[canonical] = (
                self._create_skill(
                    name=original_name,
                    canonical=canonical,
                    categories=categories,
                    role_relevance=role_relevance,
                    matched=canonical in matched,
                    user_selected=True,
                )
            )

        return list(
            final_skills.values()
        )

    # --------------------------------------------------
    # Skill creation
    # --------------------------------------------------

    def _create_skill(
        self,
        name: str,
        canonical: str,
        categories: list[KnowledgeCategory],
        role_relevance: dict[str, str],
        matched: bool,
        user_selected: bool,
    ) -> OptimizationSkill:

        taxonomy_category = (
            self._knowledge.category(
                canonical,
            )
            or "unknown"
        )

        presentation_category = (
            self._find_presentation_category(
                canonical,
                categories,
            )
            or "Other"
        )

        relevance = role_relevance.get(
            canonical.lower(),
            "not_listed",
        )

        return OptimizationSkill(
            name=name,
            canonical=canonical,
            taxonomy_category=taxonomy_category,
            presentation_category=presentation_category,
            role_relevance=relevance,
            matched=matched,
            user_selected=user_selected,
        )

    # --------------------------------------------------
    # Presentation mapping
    # --------------------------------------------------

    @staticmethod
    def _find_presentation_category(
        canonical: str,
        categories: list[KnowledgeCategory],
    ) -> str | None:

        for category in categories:

            technologies = {
                technology.lower()
                for technology in category.technologies
            }

            if canonical.lower() in technologies:
                return category.name

        return None

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    @staticmethod
    def _unique(
        values: list[str],
    ) -> list[str]:

        seen: set[str] = set()
        result: list[str] = []

        for value in values:

            key = value.lower()

            if key in seen:
                continue

            seen.add(key)
            result.append(value)

        return result