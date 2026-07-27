from __future__ import annotations

import re

from app.knowledge.domains.software_engineering.index import (
    TechnologyIndex,
)


class TechnologyExtractor:
    """
    Extract technologies from text.

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

        if not text:
            return []

        text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        if not text:
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




