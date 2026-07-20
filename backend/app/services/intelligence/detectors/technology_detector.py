import re

from app.services.intelligence.knowledge.engine import (
    KnowledgeEngine,
)

from app.services.intelligence.technology.canonicalizer import (
    TechnologyCanonicalizer,
)

from app.services.intelligence.technology.matcher import (
    TechnologyMatcher,
)

from app.services.intelligence.detectors.technology_normalizer import (
    TechnologyNormalizer,
)


class TechnologyDetector:
    """
    Detects known technologies from free text.

    Detection Pipeline

        Raw Text
            ↓
        Normalize
            ↓
        Match Known Technologies
            ↓
        Canonicalize
            ↓
        Remove Duplicates
    """

    @classmethod
    def detect(
        cls,
        text: str,
    ) -> list[str]:

        if not text:
            return []

        normalized = TechnologyNormalizer.normalize(
            text
        )

        found = []

        technologies = sorted(

            (
                item["name"]
                for item in KnowledgeEngine.technologies()
            ),

            key=len,

            reverse=True,

        )

        for technology in technologies:

            pattern = (
                rf"(?<![A-Za-z0-9])"
                rf"{re.escape(technology)}"
                rf"(?![A-Za-z0-9])"
            )

            if re.search(

                pattern,

                normalized,

                flags=re.IGNORECASE,

            ):

                found.append(

                    TechnologyCanonicalizer.normalize(
                        technology
                    )

                )

        return TechnologyMatcher.normalize_list(
            found
        )