from __future__ import annotations

import json
from pathlib import Path


class SynonymLoader:
    """
    Loads technology synonyms for the
    Software Engineering domain.

    The JSON contains:

    - metadata
    - synonyms
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

        self._data: dict = {}

    def load(self) -> dict:

        with self._path.open(
            "r",
            encoding="utf-8",
        ) as file:

            self._data = json.load(file)

        return self._data

    @property
    def metadata(self) -> dict:

        return self._data.get(
            "metadata",
            {},
        )

    @property
    def synonyms(self) -> list[dict]:

        return self._data.get(
            "synonyms",
            [],
        )