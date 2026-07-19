import re

from dataclasses import dataclass


@dataclass
class Education:

    degree: str = ""

    institution: str = ""

    year: str = ""

    score: str = ""


class EducationDetector:
    """
    Detect education entries from EDUCATION section.
    """

    YEAR_PATTERN = re.compile(r"(19|20)\d{2}")

    SCORE_PATTERN = re.compile(
        r"(\d+(\.\d+)?\s*(CGPA|GPA|%|Percentage))",
        re.IGNORECASE,
    )

    @classmethod
    def detect(
        cls,
        section_blocks,
    ) -> list[Education]:

        education_list = []

        current = None

        for item in section_blocks:

            if item["section"] != "EDUCATION":
                continue

            text = item["block"].text.strip()

            if not text:
                continue

            if current is None:
                current = Education()

            # Graduation year
            if cls.YEAR_PATTERN.search(text):
                current.year = text
                continue

            # CGPA / Percentage
            if cls.SCORE_PATTERN.search(text):
                current.score = text
                continue

            # Degree
            if current.degree == "":
                current.degree = text
                continue

            # Institution
            if current.institution == "":
                current.institution = text
                continue

        if current:
            education_list.append(current)

        return education_list