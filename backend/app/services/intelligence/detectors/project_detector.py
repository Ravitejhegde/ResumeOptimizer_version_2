import re

from dataclasses import dataclass, field

from app.services.intelligence.detectors.technology_detector import (
    TechnologyDetector,
)


@dataclass
class Project:

    title: str = ""

    description: list[str] = field(
        default_factory=list
    )

    technologies: list[str] = field(
        default_factory=list
    )


class ProjectDetector:
    """
    Extract projects from PROJECTS section.
    """

    @classmethod
    def detect(
        cls,
        section_blocks,
    ) -> list[Project]:

        projects = []

        current = None

        for item in section_blocks:

            if item["section"] != "PROJECTS":
                continue

            text = item["block"].text.strip()

            if not text:
                continue

            # -------------------------------
            # Detect new project title
            # -------------------------------

            if (
                len(text) < 80
                and not text.startswith("•")
                and not text.startswith("-")
            ):

                if current:

                    current.technologies = sorted(
                        set(current.technologies)
                    )

                    projects.append(current)

                current = Project()

                current.title = text

                continue

            # -------------------------------
            # Description
            # -------------------------------

            if current is None:

                current = Project()

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

            projects.append(current)

        return projects