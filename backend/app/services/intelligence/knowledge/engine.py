from app.services.intelligence.knowledge.loader import (
    KnowledgeLoader,
)


class KnowledgeEngine:
    """
    Central access point for ResumeOptimizer knowledge.

    No other module should read JSON files directly.
    """

    @classmethod
    def aliases(cls):

        return KnowledgeLoader.aliases()

    @classmethod
    def technologies(cls):

        return KnowledgeLoader.technologies()

    @classmethod
    def categories(cls):

        return KnowledgeLoader.categories()

    @classmethod
    def roles(cls):

        return KnowledgeLoader.roles()

    @classmethod
    def synonyms(cls):

        return KnowledgeLoader.synonyms()

    @classmethod
    def stopwords(cls):

        return KnowledgeLoader.stopwords()

    # ------------------------------------
    # Helpers
    # ------------------------------------

    @classmethod
    def is_known(cls, technology: str) -> bool:

        names = {

            item["name"].lower()

            for item in cls.technologies()

        }

        return technology.lower() in names

    @classmethod
    def category(cls, technology: str):

        for item in cls.technologies():

            if (

                item["name"].lower()

                == technology.lower()

            ):

                return item["category"]

        return "Other"

    @classmethod
    def role_skills(

        cls,

        role: str,

    ):

        return cls.roles().get(

            role,

            [],

        )