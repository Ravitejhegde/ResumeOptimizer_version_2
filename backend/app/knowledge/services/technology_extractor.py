from __future__ import annotations

import re

from app.knowledge.domains.software_engineering.index import (
    TechnologyIndex,
)


class TechnologyExtractor:
    """
    Extracts technologies from text.

    Responsibilities
    ----------------
    - Match technologies using regex patterns
    - Resolve to canonical technology IDs
    - Prevent duplicate and overlapping matches
    """

    def __init__(
        self,
        index: TechnologyIndex,
    ) -> None:

        self._index = index

    # --------------------------------------------------

    def extract(
        self,
        text: str,
    ) -> list[str]:

        if not text:
            return []

        remaining = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        if not remaining:
            return []

        detected: set[str] = set()

        for technology, pattern in self._index.patterns:

            while True:

                match = pattern.search(
                    remaining,
                )

                if match is None:
                    break

                detected.add(
                    self._index.canonical(
                        technology,
                    )
                )

                start, end = match.span()

                remaining = (
                    remaining[:start]
                    + (" " * (end - start))
                    + remaining[end:]
                )

        return sorted(
            detected,
        )
