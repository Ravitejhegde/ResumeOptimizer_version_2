from app.services.intelligence.knowledge.engine import (
    KnowledgeEngine,
)

from .canonicalizer import (
    TechnologyCanonicalizer,
)


class TechnologyMatcher:
    """
    Technology comparison engine.

    Supports:
    - Alias matching
    - Canonical matching
    - Synonym matching
    - Duplicate removal
    """

    @classmethod
    def equals(
        cls,
        left: str,
        right: str,
    ) -> bool:

        left = TechnologyCanonicalizer.normalize(
            left
        )

        right = TechnologyCanonicalizer.normalize(
            right
        )

        if left == right:
            return True

        synonyms = KnowledgeEngine.synonyms()

        for canonical, values in synonyms.items():

            group = {
                canonical.lower(),
                *[
                    value.lower()
                    for value in values
                ],
            }

            if (
                left.lower() in group
                and right.lower() in group
            ):
                return True

        return False

    @classmethod
    def normalize_list(
        cls,
        technologies: list[str],
    ) -> list[str]:

        normalized = []
        seen = set()

        for technology in technologies:

            canonical = (
                TechnologyCanonicalizer.normalize(
                    technology
                )
            )

            key = canonical.lower()

            if key in seen:
                continue

            seen.add(key)

            normalized.append(canonical)

        normalized.sort()

        return normalized

    @classmethod
    def contains(
        cls,
        technologies: list[str],
        technology: str,
    ) -> bool:

        return any(

            cls.equals(
                item,
                technology,
            )

            for item in technologies

        )