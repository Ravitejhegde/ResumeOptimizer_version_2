import re

from dataclasses import dataclass, field

from app.services.intelligence.detectors.technology_detector import (
    TechnologyDetector,
)


@dataclass
class Experience:

    company: str = ""

    designation: str = ""

    duration: str = ""

    description: list[str] = field(
        default_factory=list
    )

    technologies: list[str] = field(
        default_factory=list
    )


class ExperienceDetector:
    """
    Extract work experience from EXPERIENCE section.
    """

    YEAR_PATTERN = re.compile(
        r"(19|20)\d{2}"
    )

    @classmethod
    def detect(

        cls,

        section_blocks,

    ) -> list[Experience]:

        experiences = []

        current = None

        for item in section_blocks:

            if item["section"] != "EXPERIENCE":

                continue

            text = item["block"].text.strip()

            if not text:

                continue

            # ----------------------------------
            # New Experience Entry
            # ----------------------------------

            if cls.YEAR_PATTERN.search(text):

                if current:

                    experiences.append(
                        current
                    )

                current = Experience()

                current.duration = text

                continue

            # ----------------------------------
            # First line after duration
            # ----------------------------------

            if current is None:

                current = Experience()

            if current.designation == "":

                current.designation = text

                continue

            # ----------------------------------
            # Description
            # ----------------------------------

            current.description.append(
                text
            )

            current.technologies.extend(

                TechnologyDetector.detect(
                    text
                )

            )

        if current:

            current.technologies = sorted(

                set(current.technologies)

            )

            experiences.append(
                current
            )

        return experiences