"""
knowledge_builder.builders.role_index_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds optimized lookup indexes for Role objects.

Indexes produced
----------------
- By ID
- By normalized name
- By technology
- By skill
- By keyword
- By section

The builder never modifies the KnowledgeStore.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from knowledge_builder.builders.base_builder import BaseBuilder
from knowledge_builder.models import Role


@dataclass(slots=True)
class RoleIndex:
    """
    Fast lookup structure for roles.
    """

    by_id: dict[str, Role] = field(default_factory=dict)
    by_name: dict[str, Role] = field(default_factory=dict)

    by_technology: dict[str, set[Role]] = field(default_factory=dict)
    by_skill: dict[str, set[Role]] = field(default_factory=dict)
    by_keyword: dict[str, set[Role]] = field(default_factory=dict)
    by_section: dict[str, set[Role]] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return len(self.by_id)

    def get_by_id(self, role_id: str) -> Role | None:
        return self.by_id.get(role_id)

    def get_by_name(self, name: str) -> Role | None:
        return self.by_name.get(name.casefold())

    def get_by_skill(self, skill_id: str) -> tuple[Role, ...]:
        return tuple(
            self.by_skill.get(
                skill_id,
                set(),
            )
        )

    def get_by_technology(
        self,
        technology_id: str,
    ) -> tuple[Role, ...]:
        return tuple(
            self.by_technology.get(
                technology_id,
                set(),
            )
        )

    def get_by_keyword(
        self,
        keyword_id: str,
    ) -> tuple[Role, ...]:
        return tuple(
            self.by_keyword.get(
                keyword_id,
                set(),
            )
        )

    def get_by_section(
        self,
        section_id: str,
    ) -> tuple[Role, ...]:
        return tuple(
            self.by_section.get(
                section_id,
                set(),
            )
        )

    def find(self, value: str) -> Role | None:
        """
        Find a role using ID or name.
        """
        return (
            self.by_id.get(value)
            or self.by_name.get(value.casefold())
        )


class RoleIndexBuilder(BaseBuilder[RoleIndex]):
    """
    Builds optimized lookup indexes for roles.
    """

    def build(self) -> RoleIndex:
        index = RoleIndex()

        for role in self.store.roles.values():

            # -------------------------------------------------
            # ID
            # -------------------------------------------------

            if role.id in index.by_id:
                raise ValueError(
                    f"Duplicate role id '{role.id}'."
                )

            index.by_id[role.id] = role

            # -------------------------------------------------
            # Name
            # -------------------------------------------------

            normalized_name = role.name.casefold()

            if normalized_name in index.by_name:
                raise ValueError(
                    f"Duplicate role name '{role.name}'."
                )

            index.by_name[normalized_name] = role

            # -------------------------------------------------
            # Technologies
            # -------------------------------------------------

            for technology_id in role.technology_ids:
                index.by_technology.setdefault(
                    technology_id,
                    set(),
                ).add(role)

            # -------------------------------------------------
            # Skills
            # -------------------------------------------------

            for skill_id in role.skill_ids:
                index.by_skill.setdefault(
                    skill_id,
                    set(),
                ).add(role)

            # -------------------------------------------------
            # Keywords
            # -------------------------------------------------

            for keyword_id in role.keyword_ids:
                index.by_keyword.setdefault(
                    keyword_id,
                    set(),
                ).add(role)

            # -------------------------------------------------
            # Sections
            # -------------------------------------------------

            for section_id in role.section_ids:
                index.by_section.setdefault(
                    section_id,
                    set(),
                ).add(role)

        return index