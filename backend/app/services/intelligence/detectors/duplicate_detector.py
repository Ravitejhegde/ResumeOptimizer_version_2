from collections import defaultdict

from app.services.intelligence.models import (
    Skill,
)


class DuplicateDetector:
    """
    Removes duplicate skills while preserving
    the highest confidence occurrence.
    """

    @staticmethod
    def remove_duplicate_skills(
        skills: list[Skill],
    ) -> list[Skill]:

        grouped = defaultdict(list)

        for skill in skills:

            grouped[
                skill.name.lower()
            ].append(skill)

        unique = []

        for items in grouped.values():

            best = max(

                items,

                key=lambda x: getattr(
                    x,
                    "confidence",
                    1.0,
                ),

            )

            unique.append(best)

        return sorted(

            unique,

            key=lambda x: (

                x.section,

                x.name,

            ),

        )

    @staticmethod
    def remove_duplicate_sections(

        sections: list,

    ) -> list:

        seen = set()

        unique = []

        for section in sections:

            name = section.name.lower()

            if name in seen:

                continue

            seen.add(name)

            unique.append(section)

        return unique