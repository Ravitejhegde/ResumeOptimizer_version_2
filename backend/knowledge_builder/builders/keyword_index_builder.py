"""
knowledge_builder.builders.keyword_index_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds optimized lookup indexes for Keyword objects.

Indexes produced
----------------
- By ID
- By normalized value
- By alias
- By technology
- By skill
- By role

The builder never modifies the KnowledgeStore.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from knowledge_builder.builders.base_builder import BaseBuilder
from knowledge_builder.models import Keyword


@dataclass(slots=True)
class KeywordIndex:
    """
    Fast lookup structure for ATS keywords.
    """

    by_id: dict[str, Keyword] = field(default_factory=dict)
    by_value: dict[str, Keyword] = field(default_factory=dict)
    by_alias: dict[str, Keyword] = field(default_factory=dict)

    by_technology: dict[str, set[Keyword]] = field(default_factory=dict)
    by_skill: dict[str, set[Keyword]] = field(default_factory=dict)
    by_role: dict[str, set[Keyword]] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return len(self.by_id)

    def get_by_id(self, keyword_id: str) -> Keyword | None:
        return self.by_id.get(keyword_id)

    def get_by_value(self, value: str) -> Keyword | None:
        return self.by_value.get(value.casefold())

    def get_by_alias(self, alias: str) -> Keyword | None:
        return self.by_alias.get(alias.casefold())

    def get_by_skill(self, skill_id: str) -> tuple[Keyword, ...]:
        return tuple(
            self.by_skill.get(
                skill_id,
                set(),
            )
        )

    def get_by_role(self, role_id: str) -> tuple[Keyword, ...]:
        return tuple(
            self.by_role.get(
                role_id,
                set(),
            )
        )

    def get_by_technology(
        self,
        technology_id: str,
    ) -> tuple[Keyword, ...]:
        return tuple(
            self.by_technology.get(
                technology_id,
                set(),
            )
        )

    def find(self, value: str) -> Keyword | None:
        """
        Find a keyword using ID, value, or alias.
        """
        return (
            self.by_id.get(value)
            or self.by_value.get(value.casefold())
            or self.by_alias.get(value.casefold())
        )


class KeywordIndexBuilder(BaseBuilder[KeywordIndex]):
    """
    Builds optimized lookup indexes for ATS keywords.
    """

    def build(self) -> KeywordIndex:
        index = KeywordIndex()

        for keyword in self.store.keywords.values():

            # -------------------------------------------------
            # ID
            # -------------------------------------------------

            if keyword.id in index.by_id:
                raise ValueError(
                    f"Duplicate keyword id '{keyword.id}'."
                )

            index.by_id[keyword.id] = keyword

            # -------------------------------------------------
            # Value
            # -------------------------------------------------

            normalized_value = keyword.value.casefold()

            if normalized_value in index.by_value:
                raise ValueError(
                    f"Duplicate keyword value '{keyword.value}'."
                )

            index.by_value[normalized_value] = keyword

            # -------------------------------------------------
            # Aliases
            # -------------------------------------------------

            for alias in keyword.aliases:

                normalized_alias = alias.casefold()

                if normalized_alias in index.by_alias:
                    raise ValueError(
                        f"Duplicate keyword alias '{alias}'."
                    )

                index.by_alias[normalized_alias] = keyword

            # -------------------------------------------------
            # Technologies
            # -------------------------------------------------

            for technology_id in keyword.technology_ids:
                index.by_technology.setdefault(
                    technology_id,
                    set(),
                ).add(keyword)

            # -------------------------------------------------
            # Skills
            # -------------------------------------------------

            for skill_id in keyword.skill_ids:
                index.by_skill.setdefault(
                    skill_id,
                    set(),
                ).add(keyword)

            # -------------------------------------------------
            # Roles
            # -------------------------------------------------

            for role_id in keyword.role_ids:
                index.by_role.setdefault(
                    role_id,
                    set(),
                ).add(keyword)

        return index