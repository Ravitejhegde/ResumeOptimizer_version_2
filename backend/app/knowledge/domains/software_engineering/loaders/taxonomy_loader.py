from __future__ import annotations

import json
from pathlib import Path


class TaxonomyLoader:
    """
    Loads all taxonomy category files.

    Folder structure:

    taxonomy/
        frontend.json
        backend.json
        database.json
        ...

    Each file contains:

    {
        "category": {
            "id": "...",
            "name": "..."
        },
        "technologies": [
            ...
        ]
    }
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

        self._categories: list[dict] = []

        self._technologies: dict[
            str,
            list[dict],
        ] = {}

        # technology_id -> category_id
        self._category_lookup: dict[
            str,
            str,
        ] = {}

    # --------------------------------------------------

    def load(
        self,
    ) -> None:

        self._categories.clear()

        self._technologies.clear()

        self._category_lookup.clear()

        if not self._path.exists():

            raise FileNotFoundError(
                f"Taxonomy directory not found: {self._path}"
            )

        for file in sorted(
            self._path.glob("*.json")
        ):

            with file.open(
                "r",
                encoding="utf-8",
            ) as stream:

                try:
                    data = json.load(stream)
                except Exception as e:
                    raise RuntimeError(
                        f"Failed to load JSON: {file}"
                    ) from e

            category = data.get(
                "category",
            )

            if category is None:

                raise ValueError(
                    f"{file.name} is missing 'category'."
                )

            category_id = category["id"]

            technologies = data.get(
                "technologies",
                [],
            )

            self._categories.append(
                category,
            )

            self._technologies[
                category_id
            ] = technologies

            for technology in technologies:

                self._category_lookup[
                    technology["id"]
                ] = category_id

    # --------------------------------------------------

    @property
    def categories(
        self,
    ) -> list[dict]:

        return self._categories

    @property
    def technologies(
        self,
    ) -> dict[str, list[dict]]:

        return self._technologies

    # --------------------------------------------------

    def exists(
        self,
        category_id: str,
    ) -> bool:

        return category_id in self._technologies

    def get(
        self,
        category_id: str,
    ) -> list[dict]:

        return self._technologies.get(
            category_id,
            [],
        )

    def all(
        self,
    ) -> list[dict]:

        technologies: list[dict] = []

        for items in self._technologies.values():

            technologies.extend(items)

        return technologies

    # --------------------------------------------------

    def category(
        self,
        technology_id: str,
    ) -> str | None:

        return self._category_lookup.get(
            technology_id,
        )
