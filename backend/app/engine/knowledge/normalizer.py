from __future__ import annotations

import re

from app.engine.knowledge.synonyms import (
    SynonymDictionary,
)


class SkillNormalizer:
    """
    Converts raw skills into a canonical form.

    Examples

    AI -> artificial intelligence

    JS -> javascript

    Node JS -> node.js

    REST API -> rest api

    Postgre SQL -> postgresql
    """

    def __init__(
        self,
        dictionary: SynonymDictionary,
    ) -> None:

        self._dictionary = dictionary

    @staticmethod
    def _clean(
        text: str,
    ) -> str:

        text = text.lower()

        text = text.strip()

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

    def normalize(
        self,
        value: str,
    ) -> str:

        cleaned = self._clean(
            value,
        )

        return self._dictionary.normalize(
            cleaned,
        )

    def normalize_many(
        self,
        values: list[str],
    ) -> list[str]:

        normalized = {

            self.normalize(value)

            for value in values

            if value.strip()

        }

        return sorted(normalized)