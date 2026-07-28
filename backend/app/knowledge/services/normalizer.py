from __future__ import annotations

import re

from app.knowledge.domains.software_engineering.domain import (
    SoftwareEngineeringDomain,
)


class SkillNormalizer:
    """
    Converts raw skills into their canonical form
    using the Software Engineering Knowledge Domain.
    """

    def __init__(
        self,
        domain: SoftwareEngineeringDomain,
    ) -> None:

        self._domain = domain

    # --------------------------------------------------

    @staticmethod
    def _clean(
        text: str,
    ) -> str:

        text = text.lower().strip()

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        text = re.sub(
            r"[-_]",
            " ",
            text,
        )

        return text

    # --------------------------------------------------

    def normalize(
        self,
        value: str,
    ) -> str:

        cleaned = self._clean(
            value,
        )

        return self._domain.canonical(
            cleaned,
        )

    # --------------------------------------------------

    def normalize_many(
        self,
        values: list[str],
    ) -> list[str]:

        normalized = {

            self.normalize(value)

            for value in values

            if value.strip()

        }

        return sorted(
            normalized,
        )
