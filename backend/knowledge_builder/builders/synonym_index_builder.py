"""
knowledge_builder.builders.synonym_index_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds optimized lookup indexes for Synonym objects.

Indexes produced
----------------
- By ID
- By canonical value
- By alias

The builder never modifies the KnowledgeStore.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from knowledge_builder.builders.base_builder import BaseBuilder
from knowledge_builder.models import Synonym


@dataclass(slots=True)
class SynonymIndex:
    """
    Fast lookup structure for synonyms.
    """

    by_id: dict[str, Synonym] = field(default_factory=dict)
    by_canonical: dict[str, Synonym] = field(default_factory=dict)
    by_alias: dict[str, Synonym] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return len(self.by_id)

    def get_by_id(self, synonym_id: str) -> Synonym | None:
        return self.by_id.get(synonym_id)

    def get_by_canonical(self, canonical: str) -> Synonym | None:
        return self.by_canonical.get(canonical.casefold())

    def get_by_alias(self, alias: str) -> Synonym | None:
        return self.by_alias.get(alias.casefold())

    def find(self, value: str) -> Synonym | None:
        """
        Find a synonym using ID, canonical value, or alias.
        """
        normalized = value.casefold()

        return (
            self.by_id.get(value)
            or self.by_canonical.get(normalized)
            or self.by_alias.get(normalized)
        )


class SynonymIndexBuilder(BaseBuilder[SynonymIndex]):
    """
    Builds optimized synonym lookup indexes.
    """

    def build(self) -> SynonymIndex:
        index = SynonymIndex()

        for synonym in self.store.synonyms.values():

            # -------------------------------------------------
            # ID
            # -------------------------------------------------

            if synonym.id in index.by_id:
                raise ValueError(
                    f"Duplicate synonym id '{synonym.id}'."
                )

            index.by_id[synonym.id] = synonym

            # -------------------------------------------------
            # Canonical Value
            # -------------------------------------------------

            normalized_canonical = synonym.canonical.casefold()

            if normalized_canonical in index.by_canonical:
                raise ValueError(
                    f"Duplicate canonical value "
                    f"'{synonym.canonical}'."
                )

            index.by_canonical[
                normalized_canonical
            ] = synonym

            # -------------------------------------------------
            # Aliases
            # -------------------------------------------------

            for alias in synonym.aliases:

                normalized_alias = alias.casefold()

                if normalized_alias in index.by_alias:
                    raise ValueError(
                        f"Duplicate synonym alias "
                        f"'{alias}'."
                    )

                index.by_alias[
                    normalized_alias
                ] = synonym

        return index