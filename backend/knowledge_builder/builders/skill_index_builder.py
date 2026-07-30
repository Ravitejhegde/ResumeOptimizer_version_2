"""
knowledge_builder.builders.skill_index_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds optimized lookup indexes for Skill objects.

Indexes produced
----------------
- By ID
- By normalized name
- By normalized alias
- By ATS keyword
- By technology

The builder never modifies the KnowledgeStore.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from knowledge_builder.builders.base_builder import BaseBuilder
from knowledge_builder.models import Skill


@dataclass(slots=True)
class SkillIndex:
    """
    Fast lookup structure for skills.
    """

    by_id: dict[str, Skill] = field(default_factory=dict)
    by_name: dict[str, Skill] = field(default_factory=dict)
    by_alias: dict[str, Skill] = field(default_factory=dict)
    by_keyword: dict[str, set[Skill]] = field(default_factory=dict)
    by_technology: dict[str, set[Skill]] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return len(self.by_id)

    def get_by_id(self, skill_id: str) -> Skill | None:
        return self.by_id.get(skill_id)

    def get_by_name(self, name: str) -> Skill | None:
        return self.by_name.get(name.casefold())

    def get_by_alias(self, alias: str) -> Skill | None:
        return self.by_alias.get(alias.casefold())

    def get_by_keyword(self, keyword: str) -> tuple[Skill, ...]:
        return tuple(
            self.by_keyword.get(
                keyword.casefold(),
                set(),
            )
        )

    def get_by_technology(
        self,
        technology_id: str,
    ) -> tuple[Skill, ...]:
        return tuple(
            self.by_technology.get(
                technology_id,
                set(),
            )
        )

    def find(self, value: str) -> Skill | None:
        """
        Find a skill using ID, name, or alias.
        """
        return (
            self.by_id.get(value)
            or self.by_name.get(value.casefold())
            or self.by_alias.get(value.casefold())
        )


class SkillIndexBuilder(BaseBuilder[SkillIndex]):
    """
    Builds optimized lookup indexes for skills.
    """

    def build(self) -> SkillIndex:
        index = SkillIndex()

        for skill in self.store.skills.values():

            # -------------------------------------------------
            # ID
            # -------------------------------------------------

            if skill.id in index.by_id:
                raise ValueError(
                    f"Duplicate skill id '{skill.id}'."
                )

            index.by_id[skill.id] = skill

            # -------------------------------------------------
            # Name
            # -------------------------------------------------

            normalized_name = skill.name.casefold()

            if normalized_name in index.by_name:
                raise ValueError(
                    f"Duplicate skill name '{skill.name}'."
                )

            index.by_name[normalized_name] = skill

            # -------------------------------------------------
            # Aliases
            # -------------------------------------------------

            for alias in skill.aliases:

                normalized_alias = alias.casefold()

                if normalized_alias in index.by_alias:
                    raise ValueError(
                        f"Duplicate skill alias '{alias}'."
                    )

                index.by_alias[normalized_alias] = skill

            # -------------------------------------------------
            # ATS Keywords
            # -------------------------------------------------

            for keyword in skill.ats_keywords:

                normalized_keyword = keyword.casefold()

                index.by_keyword.setdefault(
                    normalized_keyword,
                    set(),
                ).add(skill)

            # -------------------------------------------------
            # Technologies
            # -------------------------------------------------

            for technology_id in skill.technology_ids:

                index.by_technology.setdefault(
                    technology_id,
                    set(),
                ).add(skill)

        return index