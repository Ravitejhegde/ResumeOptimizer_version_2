from __future__ import annotations

from app.knowledge.domains.software_engineering.index import (
    TechnologyIndex,
)


class TechnologyExtractor:
    """
    Extracts technologies from text using the
    Software Engineering Knowledge Platform.

    Responsibilities
    ----------------
    • Match technologies
    • Resolve synonyms
    • Prevent substring collisions
    • Return canonical technology IDs
    """

    def __init__(
        self,
        index: TechnologyIndex,
    ) -> None:

        self._index = index

    def extract(
        self,
        text: str,
    ) -> list[str]:

        if not text.strip():

            return []

        remaining = text

        detected: set[str] = set()

        for technology, pattern in self._index.patterns:

            while True:

                match = pattern.search(
                    remaining
                )

                if match is None:

                    break

                detected.add(

                    self._index.canonical(
                        technology
                    )

                )

                start, end = match.span()

                remaining = (

                    remaining[:start]

                    + (" " * (end - start))

                    + remaining[end:]

                )

        return sorted(
            detected
        )