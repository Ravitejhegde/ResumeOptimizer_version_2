from __future__ import annotations

import json
from pathlib import Path


class GraphLoader:
    """
    Loads technology relationship graph.

    Folder structure

    graph/
        frontend.json
        backend.json
        database.json
        ...

    Each file contains

    {
        "relationships": [
            {
                "technology": "...",
                "related": [...]
            }
        ]
    }
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

        self._relationships: list[dict] = []

        self._graph: dict[str, list[str]] = {}

    # --------------------------------------------------

    def load(
        self,
    ) -> None:

        self._relationships.clear()

        self._graph.clear()

        if not self._path.exists():

            raise FileNotFoundError(
                f"Graph directory not found: {self._path}"
            )

        for file in sorted(
            self._path.glob("*.json")
        ):

            with file.open(
                "r",
                encoding="utf-8",
            ) as stream:

                data = json.load(stream)

            relationships = data.get(
                "relationships",
                [],
            )

            self._relationships.extend(
                relationships,
            )

            for relation in relationships:

                self._graph[
                    relation["technology"]
                ] = relation.get(
                    "related",
                    [],
                )

    # --------------------------------------------------

    @property
    def relationships(
        self,
    ) -> list[dict]:

        return self._relationships

    # --------------------------------------------------

    def related(
        self,
        technology: str,
    ) -> list[str]:

        return self._graph.get(
            technology,
            [],
        )

    def exists(
        self,
        technology: str,
    ) -> bool:

        return technology in self._graph
