"""
knowledge_builder.builders.role_index_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds optimized lookup indexes for Role objects.
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

    by_alias: dict[str, Role] = field(default_factory=dict)

    by_keyword: dict[str, set[Role]] = field(default_factory=dict)

    by_skill: dict[str, set[Role]] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return len(self.by_id)

    def get_by_id(
        self,
        role_id: str,
    ) -> Role | None:
        return self.by_id.get(role_id)

    def get_by_name(
        self,
        name: str,
    ) -> Role | None:
        return self.by_name.get(name.casefold())

    def get_by_alias(
        self,
        alias: str,
    ) -> Role | None:
        return self.by_alias.get(alias.casefold())

    def get_by_skill(
        self,
        skill_id: str,
    ) -> tuple[Role, ...]:
        return tuple(
            self.by_skill.get(
                skill_id,
                set(),
            )
        )

    def get_by_keyword(
        self,
        keyword: str,
    ) -> tuple[Role, ...]:
        return tuple(
            self.by_keyword.get(
                keyword.casefold(),
                set(),
            )
        )

    def find(
        self,
        value: str,
    ) -> Role | None:
        return (
            self.by_id.get(value)
            or self.by_name.get(value.casefold())
            or self.by_alias.get(value.casefold())
        )


class RoleIndexBuilder(BaseBuilder[RoleIndex]):
    """
    Builds optimized lookup indexes for roles.
    """

    def build(self) -> RoleIndex:

        index = RoleIndex()

        for role in self.store.roles.values():

            # -----------------------------
            # ID
            # -----------------------------

            if role.id in index.by_id:
                raise ValueError(
                    f"Duplicate role id '{role.id}'."
                )

            index.by_id[role.id] = role

            # -----------------------------
            # Name
            # -----------------------------

            normalized_name = role.name.casefold()

            if normalized_name in index.by_name:
                raise ValueError(
                    f"Duplicate role name '{role.name}'."
                )

            index.by_name[normalized_name] = role

            # -----------------------------
            # Aliases
            # -----------------------------

            for alias in role.aliases:

                normalized_alias = alias.casefold()

                if normalized_alias in index.by_alias:
                    raise ValueError(
                        f"Duplicate role alias '{alias}'."
                    )

                index.by_alias[
                    normalized_alias
                ] = role

            # -----------------------------
            # Keywords
            # -----------------------------

            for keyword in role.keywords:

                index.by_keyword.setdefault(
                    keyword.casefold(),
                    set(),
                ).add(role)

            # -----------------------------
            # Required Skills
            # -----------------------------

            for skill_id in role.required_skill_ids:

                index.by_skill.setdefault(
                    skill_id,
                    set(),
                ).add(role)

        return index