from __future__ import annotations

import re

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)


class TechnologyIndex:
    """
    Fast in-memory technology index.

    Built once during startup and reused
    throughout the application.
    """

    def __init__(
        self,
        domain: SoftwareEngineeringDomain,
    ) -> None:

        self._domain = domain

        self._patterns: list[
            tuple[str, re.Pattern]
        ] = []

        self._canonical: dict[str, str] = {}

        self._categories: dict[str, str] = {}

        self._related: dict[str, list[str]] = {}

        self._build()

    # --------------------------------------------------

    def _build(self) -> None:

        technologies: list[str] = []

        # -----------------------------
        # Taxonomy
        # -----------------------------

        for category, values in (
            self._domain.technologies().items()
        ):

            for item in values:

                technology_id = item["id"]
                technology_name = item["name"]

                self._canonical[
                    technology_name.lower()
                ] = technology_id

                self._categories[
                    technology_id
                ] = category

                technologies.append(
                    technology_name
                )

        # -----------------------------
        # Synonyms
        # -----------------------------

        for synonym in (
            self._domain.synonyms.synonyms
        ):

            canonical = synonym["canonical"]

            self._canonical[
                canonical.lower()
            ] = canonical

            for alias in synonym["aliases"]:

                self._canonical[
                    alias.lower()
                ] = canonical

        # -----------------------------
        # Graph
        # -----------------------------

        for relation in (
            self._domain.graph.relationships
        ):

            self._related[
                relation["technology"]
            ] = relation["related"]

        # -----------------------------
        # Regex
        # -----------------------------

        technologies = sorted(
            set(technologies),
            key=len,
            reverse=True,
        )

        for technology in technologies:

            escaped = re.escape(
                technology
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
    ):

        return self._patterns

    def canonical(
        self,
        value: str,
    ) -> str:

        return self._canonical.get(
            value.lower(),
            value.lower(),
        )

    def category(
        self,
        technology: str,
    ) -> str | None:

        return self._categories.get(
            technology,
        )

    def related(
        self,
        technology: str,
    ) -> list[str]:

        return self._related.get(
            technology,
            [],
        )




