"""
knowledge_builder.models.role
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a normalized engineering role.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Role:
    """
    Represents a normalized engineering role.
    """

    id: str

    name: str

    description: str = ""

    required_skill_ids: tuple[str, ...] = field(
        default_factory=tuple
    )

    aliases: tuple[str, ...] = field(
        default_factory=tuple
    )

    keywords: tuple[str, ...] = field(
        default_factory=tuple
    )

    importance: int = 0

    deprecated: bool = False

    def requires_skill(
        self,
        skill_id: str,
    ) -> bool:
        """
        Return True if this role requires the skill.
        """
        return skill_id in self.required_skill_ids

    def matches(
        self,
        value: str,
    ) -> bool:
        """
        Return True if the supplied value refers to this role.
        """
        normalized = value.casefold().strip()

        if normalized == self.name.casefold():
            return True

        return normalized in (
            alias.casefold()
            for alias in self.aliases
        )

    def to_dict(self) -> dict:
        """
        Serialize Role.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "required_skill_ids": list(
                self.required_skill_ids
            ),
            "aliases": list(self.aliases),
            "keywords": list(self.keywords),
            "importance": self.importance,
            "deprecated": self.deprecated,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "Role":
        """
        Deserialize Role.
        """
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get(
                "description",
                "",
            ),
            required_skill_ids=tuple(
                data.get(
                    "required_skill_ids",
                    [],
                )
            ),
            aliases=tuple(
                data.get(
                    "aliases",
                    [],
                )
            ),
            keywords=tuple(
                data.get(
                    "keywords",
                    [],
                )
            ),
            importance=int(
                data.get(
                    "importance",
                    0,
                )
            ),
            deprecated=bool(
                data.get(
                    "deprecated",
                    False,
                )
            ),
        )