from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path


class SynonymLoader:
    """
    Loads technology synonyms.

    Folder structure

    synonyms/
        frontend.json
        backend.json
        database.json
        ...

    Each file contains

    {
        "synonyms": [
            {
                "canonical": "...",
                "aliases": [...]
            }
        ]
    }
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

        self._synonyms: list[dict] = []

        self._lookup: dict[str, str] = {}

    # --------------------------------------------------

    def load(
        self,
    ) -> None:

        self._synonyms.clear()
        self._lookup.clear()

        if not self._path.exists():
            raise FileNotFoundError(
                f"Synonym directory not found: {self._path}"
            )

        for file in sorted(self._path.glob("*.json")):

            # Skip empty files
            if file.stat().st_size == 0:
                print(f"[Knowledge] Skipping empty synonym file: {file.name}")
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

            synonyms = data.get("synonyms", [])

            if not isinstance(synonyms, list):
                print(f"[Knowledge] Invalid synonym structure: {file.name}")
                continue

            self._synonyms.extend(synonyms)

            for item in synonyms:

                canonical = item.get("canonical")

                if not canonical:
                    continue

                canonical = canonical.lower()

                self._lookup[canonical] = canonical

                aliases = item.get("aliases", [])

                if not isinstance(aliases, list):
                    continue

                for alias in aliases:

                    if not alias:
                        continue

                    self._lookup[alias.lower()] = canonical

    # --------------------------------------------------

    @property
    def synonyms(
        self,
    ) -> list[dict]:

        return self._synonyms

    # --------------------------------------------------

    def canonical(
        self,
        value: str,
    ) -> str:

        return self._lookup.get(
            value.lower(),
            value.lower(),
        )

    # --------------------------------------------------

    def exists(
        self,
        value: str,
    ) -> bool:

        return value.lower() in self._lookup