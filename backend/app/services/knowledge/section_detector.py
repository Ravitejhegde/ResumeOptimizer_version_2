import json
from pathlib import Path


class SectionDetector:

    _lookup = None

    @classmethod
    def _load(cls):

        if cls._lookup is not None:
            return

        data_path = (
    Path(__file__).resolve().parent
    / "data"
    / "sections.json"
)

        with open(
            data_path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        lookup = {}

        for section, headings in data.items():

            for heading in headings:

                lookup[heading.lower()] = section

        cls._lookup = lookup

    @classmethod
    def detect(
        cls,
        text: str,
    ) -> str:

        cls._load()

        return cls._lookup.get(
            text.strip().lower(),
            "unknown",
        )