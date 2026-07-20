import json
from functools import lru_cache
from pathlib import Path


class KnowledgeLoader:
    """
    Loads all ResumeOptimizer knowledge files.

    Files are cached so they are only read once.
    """

    ROOT = Path(__file__).parent

    @classmethod
    @lru_cache(maxsize=None)
    def load(cls, filename: str):

        path = cls.ROOT / filename

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    @classmethod
    def aliases(cls):

        return cls.load(
            "aliases.json"
        )

    @classmethod
    def technologies(cls):

        return cls.load(
            "technologies.json"
        )

    @classmethod
    def categories(cls):

        return cls.load(
            "categories.json"
        )

    @classmethod
    def roles(cls):

        return cls.load(
            "roles.json"
        )

    @classmethod
    def synonyms(cls):

        return cls.load(
            "synonyms.json"
        )

    @classmethod
    def stopwords(cls):

        return cls.load(
            "stopwords.json"
        )