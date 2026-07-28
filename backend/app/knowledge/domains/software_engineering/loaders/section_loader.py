from __future__ import annotations

import json
from pathlib import Path


class SectionLoader:
    """
    Loads all resume section definitions.

    Folder structure

    sections/
        summary.json
        experience.json
        education.json
        ...
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path)

        self._sections: dict[str, dict] = {}

    # --------------------------------------------------

    def load(
        self,
    ) -> None:

        self._sections.clear()

        if not self._path.exists():

            raise FileNotFoundError(
                f"Section directory not found: {self._path}"
            )

        for file in sorted(
            self._path.glob("*.json")
        ):

            with file.open(
                "r",
                encoding="utf-8",
            ) as stream:

                data = json.load(
                    stream,
                )

            section = data.get(
                "section",
            )

            if section is None:

                raise ValueError(
                    f"{file.name} is missing 'section'."
                )

            self._sections[
                section["id"]
            ] = section

    # --------------------------------------------------

    @property
    def sections(
        self,
    ) -> dict[str, dict]:

        return self._sections

    # --------------------------------------------------

    def exists(
        self,
        section_id: str,
    ) -> bool:

        return (
            section_id
            in self._sections
        )

    # --------------------------------------------------

    def get(
        self,
        section_id: str,
    ) -> dict | None:

        return self._sections.get(
            section_id,
        )

    # --------------------------------------------------

    def all(
        self,
    ) -> list[dict]:

        return list(
            self._sections.values(),
        )
