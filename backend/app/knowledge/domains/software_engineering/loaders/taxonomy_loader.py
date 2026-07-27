from __future__ import annotations

import json
from pathlib import Path


class TaxonomyLoader:
    """
    Loads the Software Engineering taxonomy.

    The taxonomy is stored as JSON and contains:

    - metadata
    - categories
    - technologies_by_category
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
    def categories(self) -> list[dict]:

        return self._data.get(
            "categories",
            [],
        )

    @property
    def technologies(self) -> dict:

        return self._data.get(
            "technologies_by_category",
            {},
        )