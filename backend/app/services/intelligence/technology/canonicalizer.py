import re

from app.services.intelligence.knowledge.engine import (
    KnowledgeEngine,
)


class TechnologyCanonicalizer:
    """
    Converts technology aliases into a canonical name
    using the ResumeOptimizer Knowledge Engine.
    """

    @staticmethod
    def normalize(
        name: str,
    ) -> str:

        if not name:
            return ""

        value = re.sub(
            r"\s+",
            " ",
            name.strip().lower(),
        )

        aliases = KnowledgeEngine.aliases()

        # aliases.json format:
        #
        # {
        #   "React": ["react","reactjs","react.js"]
        # }

        for canonical, alias_list in aliases.items():

            if value == canonical.lower():

                return canonical

            if value in (

                alias.lower()

                for alias in alias_list

            ):

                return canonical

        return name.strip()