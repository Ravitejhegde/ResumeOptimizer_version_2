import re

from app.services.intelligence.constants import (
    TECHNOLOGY_CATEGORY,
)

from app.services.intelligence.detectors.technology_normalizer import (
    TechnologyNormalizer,
)



class TechnologyDetector:

    @staticmethod
    def detect(
        text: str,
    ) -> list[str]:

        # ----------------------------------------
        # Normalize text first
        # ----------------------------------------

        normalized = TechnologyNormalizer.normalize(
            text
        )

        found = set()

        # ----------------------------------------
        # Longest technologies first
        # ----------------------------------------

        technologies = sorted(

            TECHNOLOGY_CATEGORY.keys(),

            key=len,

            reverse=True,

        )

        for technology in technologies:

            pattern = rf"(?<![A-Za-z0-9]){re.escape(technology)}(?![A-Za-z0-9])"

            if re.search(

                pattern,

                normalized,

                flags=re.IGNORECASE,

            ):

                found.add(
                    technology
                )

        return sorted(found)