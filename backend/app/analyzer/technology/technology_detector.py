"""
app.analyzer.technology.technology_detector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Production-grade technology detector for ResumeOptimizer.

Responsibilities
----------------
- Detect technologies from resume text.
- Support aliases.
- Ignore case.
- Support multi-word technologies.
- Avoid partial-word false positives.
- Return unique technology IDs.

The detector is read-only and relies entirely on the Knowledge Runtime.
"""

from __future__ import annotations

import re
from functools import lru_cache

from app.knowledge.provider import get_knowledge


class TechnologyDetector:
    """
    Detect technologies from resume text.
    """

    def __init__(self) -> None:
        self._lookup = get_knowledge().technologies

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize text before matching.

        Examples
        --------
        Spring_Boot -> spring boot
        Spring-Boot -> spring boot
        Python3 -> python3
        """

        text = text.casefold()

        text = re.sub(r"[_\-]+", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    @lru_cache(maxsize=1024)
    def _compile_pattern(candidate: str) -> re.Pattern[str]:
        """
        Compile a regex that matches a complete technology name.

        Word boundaries prevent:
            java matching javascript
            sql matching nosql
        """

        escaped = re.escape(
            TechnologyDetector._normalize(candidate)
        )

        escaped = escaped.replace(r"\ ", r"\s+")

        return re.compile(
            rf"\b{escaped}\b",
            re.IGNORECASE,
        )

    def detect(
        self,
        text: str,
    ) -> set[str]:
        """
        Detect technology IDs from text.
        """

        normalized_text = self._normalize(text)

        detected: set[str] = set()

        for technology in self._lookup.all():

            technology_id = technology["id"]

            candidates = [
                technology_id,
                technology["name"],
                *technology.get("aliases", []),
            ]

            for candidate in candidates:

                pattern = self._compile_pattern(candidate)

                if pattern.search(normalized_text):

                    detected.add(
                        technology_id
                    )

                    break

        return detected