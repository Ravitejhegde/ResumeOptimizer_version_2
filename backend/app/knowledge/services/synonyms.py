from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SynonymDictionary:
    """
    Maintains technology and skill synonyms.

    Used throughout the engine to normalize
    resume skills and job description skills
    before comparison.
    """

    synonyms: dict[str, set[str]] = field(
        default_factory=dict
    )

    def register(
        self,
        canonical: str,
        *aliases: str,
    ) -> None:

        canonical = canonical.lower().strip()

        values = self.synonyms.setdefault(
            canonical,
            set(),
        )

        values.add(canonical)

        for alias in aliases:

            alias = alias.lower().strip()

            values.add(alias)

    def normalize(
        self,
        value: str,
    ) -> str:

        value = value.lower().strip()

        for canonical, aliases in self.synonyms.items():

            if value in aliases:

                return canonical

        return value

    def is_synonym(
        self,
        first: str,
        second: str,
    ) -> bool:

        return (
            self.normalize(first)
            ==
            self.normalize(second)
        )




