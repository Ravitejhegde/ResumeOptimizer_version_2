"""
knowledge_builder.models.knowledge_store
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Central in-memory repository for all knowledge entities.

The KnowledgeStore is the single source of truth after the loading
phase. It does not read JSON files or build relationships—it simply
stores strongly typed objects and provides fast lookups.

Responsibilities
----------------
- Store domain models
- Prevent duplicate IDs
- Provide O(1) lookups
- Expose read-only collections
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from .ats_rule import ATSRule
from .category import Category
from .keyword import Keyword
from .relationship import Relationship
from .role import Role
from .section import Section
from .skill import Skill
from .synonym import Synonym
from .technology import Technology


@dataclass(slots=True)
class KnowledgeStore:
    """
    Central repository for every knowledge object.

    All collections are indexed by their unique identifier.
    """

    categories: Dict[str, Category] = field(default_factory=dict)
    technologies: Dict[str, Technology] = field(default_factory=dict)
    skills: Dict[str, Skill] = field(default_factory=dict)
    roles: Dict[str, Role] = field(default_factory=dict)
    sections: Dict[str, Section] = field(default_factory=dict)
    synonyms: Dict[str, Synonym] = field(default_factory=dict)
    keywords: Dict[str, Keyword] = field(default_factory=dict)
    relationships: Dict[str, Relationship] = field(default_factory=dict)
    ats_rules: Dict[str, ATSRule] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Generic helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _add_item(store: Dict[str, object], item: object, item_id: str) -> None:
        """
        Add an item to a dictionary while preventing duplicate IDs.
        """
        if item_id in store:
            raise ValueError(
                f"Duplicate knowledge id detected: '{item_id}'"
            )

        store[item_id] = item

    # ------------------------------------------------------------------
    # Category
    # ------------------------------------------------------------------

    def add_category(self, category: Category) -> None:
        self._add_item(self.categories, category, category.id)

    def get_category(self, category_id: str) -> Category | None:
        return self.categories.get(category_id)

    # ------------------------------------------------------------------
    # Technology
    # ------------------------------------------------------------------

    def add_technology(self, technology: Technology) -> None:
        self._add_item(
            self.technologies,
            technology,
            technology.id,
        )

    def get_technology(self, technology_id: str) -> Technology | None:
        return self.technologies.get(technology_id)

    # ------------------------------------------------------------------
    # Skill
    # ------------------------------------------------------------------

    def add_skill(self, skill: Skill) -> None:
        self._add_item(
            self.skills,
            skill,
            skill.id,
        )

    def get_skill(self, skill_id: str) -> Skill | None:
        return self.skills.get(skill_id)

    # ------------------------------------------------------------------
    # Role
    # ------------------------------------------------------------------

    def add_role(self, role: Role) -> None:
        self._add_item(
            self.roles,
            role,
            role.id,
        )

    def get_role(self, role_id: str) -> Role | None:
        return self.roles.get(role_id)

    # ------------------------------------------------------------------
    # Section
    # ------------------------------------------------------------------

    def add_section(self, section: Section) -> None:
        self._add_item(
            self.sections,
            section,
            section.id,
        )

    def get_section(self, section_id: str) -> Section | None:
        return self.sections.get(section_id)

    # ------------------------------------------------------------------
    # Synonym
    # ------------------------------------------------------------------

    def add_synonym(self, synonym: Synonym) -> None:
        self._add_item(
            self.synonyms,
            synonym,
            synonym.id,
        )

    def get_synonym(self, synonym_id: str) -> Synonym | None:
        return self.synonyms.get(synonym_id)

    # ------------------------------------------------------------------
    # Keyword
    # ------------------------------------------------------------------

    def add_keyword(self, keyword: Keyword) -> None:
        self._add_item(
            self.keywords,
            keyword,
            keyword.id,
        )

    def get_keyword(self, keyword_id: str) -> Keyword | None:
        return self.keywords.get(keyword_id)

    # ------------------------------------------------------------------
    # Relationship
    # ------------------------------------------------------------------

    def add_relationship(
        self,
        relationship: Relationship,
    ) -> None:
        self._add_item(
            self.relationships,
            relationship,
            relationship.id,
        )

    def get_relationship(
        self,
        relationship_id: str,
    ) -> Relationship | None:
        return self.relationships.get(relationship_id)

    # ------------------------------------------------------------------
    # ATS Rules
    # ------------------------------------------------------------------

    def add_ats_rule(
        self,
        rule: ATSRule,
    ) -> None:
        self._add_item(
            self.ats_rules,
            rule,
            rule.id,
        )

    def get_ats_rule(
        self,
        rule_id: str,
    ) -> ATSRule | None:
        return self.ats_rules.get(rule_id)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def total_categories(self) -> int:
        return len(self.categories)

    @property
    def total_technologies(self) -> int:
        return len(self.technologies)

    @property
    def total_skills(self) -> int:
        return len(self.skills)

    @property
    def total_roles(self) -> int:
        return len(self.roles)

    @property
    def total_sections(self) -> int:
        return len(self.sections)

    @property
    def total_synonyms(self) -> int:
        return len(self.synonyms)

    @property
    def total_keywords(self) -> int:
        return len(self.keywords)

    @property
    def total_relationships(self) -> int:
        return len(self.relationships)

    @property
    def total_ats_rules(self) -> int:
        return len(self.ats_rules)

    @property
    def total_entities(self) -> int:
        return (
            self.total_categories
            + self.total_technologies
            + self.total_skills
            + self.total_roles
            + self.total_sections
            + self.total_synonyms
            + self.total_keywords
            + self.total_relationships
            + self.total_ats_rules
        )