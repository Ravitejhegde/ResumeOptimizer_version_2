"""
knowledge_builder.validators.store_validator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validates a populated KnowledgeStore.

This validator operates on strongly typed models after all loaders
have completed. It verifies the integrity of cross-references between
entities before the store is used by analyzers, planners, or AI
components.
"""

from __future__ import annotations

from typing import List

from knowledge_builder.models import KnowledgeStore


class StoreValidator:
    """
    Performs integrity validation on a populated KnowledgeStore.
    """

    def __init__(
        self,
        store: KnowledgeStore,
    ) -> None:
        self._store = store
        self._errors: list[str] = []

    @property
    def errors(self) -> list[str]:
        """
        Validation errors collected during the last run.
        """
        return list(self._errors)

    @property
    def is_valid(self) -> bool:
        """
        True if the store has no validation errors.
        """
        return not self._errors

    def validate(self) -> List[str]:
        """
        Validate the complete KnowledgeStore.
        """
        self._errors.clear()

        self._validate_technologies()
        self._validate_skills()
        self._validate_roles()
        self._validate_keywords()
        self._validate_relationships()
        self._validate_ats_rules()

        return self.errors

    # ------------------------------------------------------------------
    # Technology Validation
    # ------------------------------------------------------------------

    def _validate_technologies(self) -> None:
        for technology in self._store.technologies.values():

            if technology.category_id not in self._store.categories:
                self._errors.append(
                    f"Technology '{technology.id}' references "
                    f"unknown category '{technology.category_id}'."
                )

    # ------------------------------------------------------------------
    # Skill Validation
    # ------------------------------------------------------------------

    def _validate_skills(self) -> None:
        for skill in self._store.skills.values():

            for technology_id in skill.technology_ids:

                if technology_id not in self._store.technologies:
                    self._errors.append(
                        f"Skill '{skill.id}' references "
                        f"unknown technology '{technology_id}'."
                    )

    # ------------------------------------------------------------------
    # Role Validation
    # ------------------------------------------------------------------

    def _validate_roles(self) -> None:
        """
        Validate role definitions.
        """

        for role in self._store.roles.values():

            # Validate required skills

            for skill_id in role.required_skill_ids:

                if skill_id not in self._store.skills:
                    self._errors.append(
                        f"Role '{role.id}' references "
                        f"unknown skill '{skill_id}'."
                    )

            # Duplicate required skills

            if len(role.required_skill_ids) != len(
                set(role.required_skill_ids)
            ):
                self._errors.append(
                    f"Role '{role.id}' contains duplicate required skills."
                )

            # Basic validation

            if not role.id.strip():
                self._errors.append(
                    "Role has an empty id."
                )

            if not role.name.strip():
                self._errors.append(
                    f"Role '{role.id}' has an empty name."
                )

            if role.importance < 0:
                self._errors.append(
                    f"Role '{role.id}' has a negative importance."
                )

    # ------------------------------------------------------------------
    # Keyword Validation
    # ------------------------------------------------------------------

    def _validate_keywords(self) -> None:
        for keyword in self._store.keywords.values():

            for technology_id in keyword.technology_ids:

                if technology_id not in self._store.technologies:
                    self._errors.append(
                        f"Keyword '{keyword.id}' references "
                        f"unknown technology '{technology_id}'."
                    )

            for skill_id in keyword.skill_ids:

                if skill_id not in self._store.skills:
                    self._errors.append(
                        f"Keyword '{keyword.id}' references "
                        f"unknown skill '{skill_id}'."
                    )

            for role_id in keyword.role_ids:

                if role_id not in self._store.roles:
                    self._errors.append(
                        f"Keyword '{keyword.id}' references "
                        f"unknown role '{role_id}'."
                    )

    # ------------------------------------------------------------------
    # Relationship Validation
    # ------------------------------------------------------------------

    def _validate_relationships(self) -> None:
        for relationship in self._store.relationships.values():

            if relationship.source_id == relationship.target_id:
                self._errors.append(
                    f"Relationship '{relationship.id}' "
                    "cannot reference itself."
                )

    # ------------------------------------------------------------------
    # ATS Rule Validation
    # ------------------------------------------------------------------

    def _validate_ats_rules(self) -> None:
        """
        Validate ATS rule metadata.
        """

        for rule in self._store.ats_rules.values():

            if not rule.id.strip():
                self._errors.append(
                    "ATS rule has an empty id."
                )

            if not rule.name.strip():
                self._errors.append(
                    f"ATS rule '{rule.id}' has an empty name."
                )

            if not rule.category.strip():
                self._errors.append(
                    f"ATS rule '{rule.id}' has an empty category."
                )

            if rule.score < 0:
                self._errors.append(
                    f"ATS rule '{rule.id}' has a negative score."
                )