from __future__ import annotations

import json
from pathlib import Path


class MetadataLoader:
    """
    Loads metadata for the knowledge domain.

    data/metadata.json
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

        self._metadata: dict = {}

    # --------------------------------------------------

    def load(
        self,
    ) -> None:

        with self._path.open(
            "r",
            encoding="utf-8",
        ) as file:

            self._metadata = json.load(
                file,
            )

    # --------------------------------------------------

    @property
    def metadata(
        self,
    ) -> dict:

        return self._metadata

    @property
    def domain(
        self,
    ) -> dict:

        return self._metadata.get(
            "domain",
            {},
        )

    @property
    def knowledge(
        self,
    ) -> dict:

        return self._metadata.get(
            "knowledge",
            {},
        )

    @property
    def maintainer(
        self,
    ) -> dict:

        return self._metadata.get(
            "maintainer",
            {},
        )
