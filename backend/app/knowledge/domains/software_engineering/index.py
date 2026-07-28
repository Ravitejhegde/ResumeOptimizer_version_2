from __future__ import annotations

import re

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)


class TechnologyIndex:
    """
    Fast in-memory technology index.

    Responsibilities
    ----------------
    - Build regex patterns
    - Delegate synonym lookup
    - Delegate category lookup
    - Delegate relationship lookup
    """

    def __init__(
        self,
        domain: SoftwareEngineeringDomain,
    ) -> None:

        self._domain = domain

        self._patterns: list[
            tuple[str, re.Pattern]
        ] = []

        self._build_patterns()

    # --------------------------------------------------

    def _build_patterns(
        self,
    ) -> None:

        technologies: list[str] = []

        for values in (
            self._domain.technologies().values()
        ):

            for item in values:

                technologies.append(
                    item["name"]
                )

        technologies = sorted(
            set(technologies),
            key=len,
            reverse=True,
        )

        for technology in technologies:

            escaped = re.escape(
                technology,
            ).replace(
                r"\ ",
                r"\s+",
            )

            if technology[0].isalnum():

                pattern = re.compile(
                    rf"(?<!\w){escaped}(?!\w)",
                    re.IGNORECASE,
                )

            else:

                pattern = re.compile(
                    escaped,
                    re.IGNORECASE,
                )

            self._patterns.append(
                (
                    technology,
                    pattern,
                )
            )

    # --------------------------------------------------

    @property
    def patterns(
        self,
    ) -> list[
        tuple[str, re.Pattern]
    ]:

        return self._patterns

    # --------------------------------------------------

    def canonical(
        self,
        value: str,
    ) -> str:

        return self._domain.synonyms.canonical(
            value,
        )

    def category(
        self,
        technology: str,
    ) -> str | None:

        return self._domain.taxonomy.category(
            technology,
        )

    def related(
        self,
        technology: str,
    ) -> list[str]:

        return self._domain.graph.related(
            technology,
        )