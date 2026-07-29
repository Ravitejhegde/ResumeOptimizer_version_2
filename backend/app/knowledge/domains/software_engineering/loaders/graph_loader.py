from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path


class GraphLoader:
    """
    Loads technology relationship graph.
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

        for file in sorted(self._path.glob("*.json")):

            if file.stat().st_size == 0:
                print(f"[Knowledge] Skipping empty graph file: {file.name}")
                continue

            try:

                with file.open(
                    "r",
                    encoding="utf-8",
                ) as stream:

                    data = json.load(stream)

            except JSONDecodeError:

                print(f"[Knowledge] Invalid JSON: {file.name}")
                continue

            except Exception as ex:

                print(f"[Knowledge] Failed to load {file.name}: {ex}")
                continue

            relationships = data.get(
                "relationships",
                [],
            )

            if not isinstance(relationships, list):
                continue

            self._relationships.extend(
                relationships,
            )

            for relation in relationships:

                technology = relation.get(
                    "technology"
                )

                if not technology:
                    continue

                related = relation.get(
                    "related",
                    [],
                )

                if not isinstance(
                    related,
                    list,
                ):
                    related = []

                self._graph[
                    technology
                ] = related

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