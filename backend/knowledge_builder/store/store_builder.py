"""
knowledge_builder.store.store_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds and validates a fully populated KnowledgeStore.

Responsibilities
----------------
- Execute every loader
- Populate the KnowledgeStore
- Validate the completed store
- Return a ready-to-use KnowledgeStore

This class intentionally does NOT:
- Read JSON files directly
- Build relationships
- Export knowledge
"""

from __future__ import annotations

from knowledge_builder.loaders import (
    ATSLoader,
    CategoryLoader,
    KeywordLoader,
    RelationshipLoader,
    RoleLoader,
    SectionLoader,
    SkillLoader,
    SynonymLoader,
    TechnologyLoader,
)
from knowledge_builder.models import KnowledgeStore
from knowledge_builder.validators import StoreValidator


class StoreBuilder:
    """
    Builds and validates a KnowledgeStore.
    """

    def __init__(self) -> None:
        self._store = KnowledgeStore()

    @property
    def store(self) -> KnowledgeStore:
        """
        Return the current KnowledgeStore.
        """
        return self._store

    def build(self) -> KnowledgeStore:
        """
        Build, validate, and return a KnowledgeStore.

        Raises
        ------
        ValueError
            If validation fails.
        """

        self._store = KnowledgeStore()

        self._load_categories()
        self._load_technologies()
        self._load_skills()
        self._load_roles()
        self._load_sections()
        self._load_synonyms()
        self._load_keywords()
        self._load_relationships()
        self._load_ats_rules()

        self._validate()

        return self._store

    def rebuild(self) -> KnowledgeStore:
        """
        Rebuild the entire knowledge store.
        """
        return self.build()

    # ---------------------------------------------------------
    # Loading
    # ---------------------------------------------------------

    def _load_categories(self) -> None:
        for item in CategoryLoader.from_default_location().load():
            self._store.add_category(item)

    def _load_technologies(self) -> None:
        for item in TechnologyLoader.from_default_location().load():
            self._store.add_technology(item)

    def _load_skills(self) -> None:
        for item in SkillLoader.from_default_location().load():
            self._store.add_skill(item)

    def _load_roles(self) -> None:
        for item in RoleLoader.from_default_location().load():
            self._store.add_role(item)

    def _load_sections(self) -> None:
        for item in SectionLoader.from_default_location().load():
            self._store.add_section(item)

    def _load_synonyms(self) -> None:
        for item in SynonymLoader.from_default_location().load():
            self._store.add_synonym(item)

    def _load_keywords(self) -> None:
        for item in KeywordLoader.from_default_location().load():
            self._store.add_keyword(item)

    def _load_relationships(self) -> None:
        for item in RelationshipLoader.from_default_location().load():
            self._store.add_relationship(item)

    def _load_ats_rules(self) -> None:
        for item in ATSLoader.from_default_location().load():
            self._store.add_ats_rule(item)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate(self) -> None:
        """
        Validate the populated KnowledgeStore.

        Raises
        ------
        ValueError
            If one or more validation errors are found.
        """
        validator = StoreValidator(self._store)
        errors = validator.validate()

        if errors:
            message = "\n".join(
                f"- {error}"
                for error in errors
            )

            raise ValueError(
                "KnowledgeStore validation failed:\n\n"
                f"{message}"
            )