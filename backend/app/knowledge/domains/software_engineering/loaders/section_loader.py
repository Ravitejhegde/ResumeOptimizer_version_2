from __future__ import annotations

import json
from json import JSONDecodeError
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

            # Skip empty files
            if file.stat().st_size == 0:
                print(f"[Knowledge] Skipping empty section file: {file.name}")
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

            if not isinstance(data, dict):
                print(f"[Knowledge] Invalid section format: {file.name}")
                continue

            section = data.get("section")

            if not isinstance(section, dict):
                print(f"[Knowledge] Missing 'section' object: {file.name}")
                continue

            section_id = section.get("id")

            if not section_id:
                print(f"[Knowledge] Missing section id: {file.name}")
                continue

            self._sections[section_id] = section

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

        return section_id in self._sections

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