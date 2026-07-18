import json
from pathlib import Path


class TechnologyClassifier:

    _lookup = None

    @classmethod
    def _load(cls):

        if cls._lookup is not None:
            return

        data_path = (
            Path(__file__).resolve().parent
            / "data"
            / "technologies.json"
        )

        with open(
            data_path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        lookup = {}

        for category, technologies in data.items():

            for technology in technologies:

                lookup[
                    technology.lower()
                ] = category

        cls._lookup = lookup

    @classmethod
    def classify(
        cls,
        technology: str,
    ) -> str:

        cls._load()

        return cls._lookup.get(
            technology.strip().lower(),
            "other",
        )

    @classmethod
    def exists(
        cls,
        technology: str,
    ) -> bool:

        cls._load()

        return (
            technology.strip().lower()
            in cls._lookup
        )

    @classmethod
    def get_all(
        cls,
    ) -> dict[str, str]:

        cls._load()

        return dict(cls._lookup)

    @classmethod
    def get_by_category(
        cls,
        category: str,
    ) -> list[str]:

        cls._load()

        return sorted(

            technology

            for technology, tech_category
            in cls._lookup.items()

            if tech_category == category

        )