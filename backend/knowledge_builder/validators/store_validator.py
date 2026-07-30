"""
knowledge_builder.validators.store_validator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validates a populated KnowledgeStore.

This validator operates on strongly typed models after all loaders
have completed. It verifies the integrity of cross-references between
entities before the store is used by analyzers, planners, or AI
components.

Responsibilities
----------------
- Validate cross references
- Detect orphan references
- Detect missing IDs
- Report all validation errors

This validator intentionally does NOT:
- Modify the KnowledgeStore
- Load JSON files
- Build relationships
- Export knowledge
"""

from __future__ import annotations

from typing import List

from knowledge_builder.models import KnowledgeStore


class StoreValidator:
    """
    Performs integrity validation on a populated KnowledgeStore.
    """

    def __init__(self, store: KnowledgeStore) -> None:
        self._store = store
        self._errors: list[str] = []

    @property
    def errors(self) -> list[str]:
        """
        Validation errors collected during the last run.
        """
        return list(self._errors)

    def validate(self) -> List[str]:
        """
        Validate the entire KnowledgeStore.

        Returns
        -------
        list[str]
            List of validation errors. Empty if valid.
        """
        self._errors.clear()

        self._validate_technologies()
        self._validate_skills()
        self._validate_roles()
        self._validate_keywords()
        self._validate_relationships()
        self._validate_ats_rules()

        return self.errors

    @property
    def is_valid(self) -> bool:
        """
        True if the store has no validation errors.
        """
        return not self._errors

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
        for role in self._store.roles.values():

            for technology_id in role.technology_ids:
                if technology_id not in self._store.technologies:
                    self._errors.append(
                        f"Role '{role.id}' references "
                        f"unknown technology '{technology_id}'."
                    )

            for skill_id in role.skill_ids:
                if skill_id not in self._store.skills:
                    self._errors.append(
                        f"Role '{role.id}' references "
                        f"unknown skill '{skill_id}'."
                    )

            for section_id in role.section_ids:
                if section_id not in self._store.sections:
                    self._errors.append(
                        f"Role '{role.id}' references "
                        f"unknown section '{section_id}'."
                    )

            for keyword_id in role.keyword_ids:
                if keyword_id not in self._store.keywords:
                    self._errors.append(
                        f"Role '{role.id}' references "
                        f"unknown keyword '{keyword_id}'."
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
        for rule in self._store.ats_rules.values():

            for section_id in rule.section_ids:
                if section_id not in self._store.sections:
                    self._errors.append(
                        f"ATS rule '{rule.id}' references "
                        f"unknown section '{section_id}'."
                    )

            for keyword_id in rule.keyword_ids:
                if keyword_id not in self._store.keywords:
                    self._errors.append(
                        f"ATS rule '{rule.id}' references "
                        f"unknown keyword '{keyword_id}'."
                    )