from __future__ import annotations

import re

from app.engine.common.enums import SectionType
from app.engine.models.document.paragraph import Paragraph


class SectionReader:
    """
    Detects logical resume sections.

    Responsibilities:
        - Identify resume headings.
        - Normalize heading text.
        - Map headings to SectionType.

    Does not:
        - Modify paragraphs.
        - Analyze content.
        - Extract skills.
    """


    _SECTION_MAP: dict[SectionType, tuple[str, ...]] = {

        # ----------------------------------
        # Summary
        # ----------------------------------

        SectionType.SUMMARY: (
            "summary",
            "professional summary",
            "profile",
            "objective",
            "career objective",
            "career profile",
            "about me",
            "professional profile",
        ),


        # ----------------------------------
        # Experience
        # ----------------------------------

        SectionType.EXPERIENCE: (
            "experience",
            "work experience",
            "professional experience",
            "employment",
            "employment history",
            "work history",
            "career history",
            "internship",
            "internships",
            "internship experience",
            "internship history",
        ),


        # ----------------------------------
        # Projects
        # ----------------------------------

        SectionType.PROJECTS: (
            "projects",
            "project experience",
            "academic projects",
            "personal projects",
            "key projects",
            "technical projects",
            "ai projects",
            "machine learning projects",
            "ml projects",
        ),


        # ----------------------------------
        # Skills
        # ----------------------------------

        SectionType.SKILLS: (
            "skills",
            "technical skills",
            "core skills",
            "technical expertise",
            "technologies",
            "competencies",
            "tools and technologies",
        ),


        # ----------------------------------
        # Education
        # ----------------------------------

        SectionType.EDUCATION: (
            "education",
            "academic background",
            "qualification",
            "qualifications",
            "academic qualification",
        ),


        # ----------------------------------
        # Certifications
        # ----------------------------------

        SectionType.CERTIFICATIONS: (
            "certifications",
            "certificates",
            "courses",
            "licenses",
        ),


        # ----------------------------------
        # Achievements
        # ----------------------------------

        SectionType.ACHIEVEMENTS: (
            "achievements",
            "awards",
            "honors",
            "honours",
        ),


        # ----------------------------------
        # Publications
        # ----------------------------------

        SectionType.PUBLICATIONS: (
            "publications",
            "research",
        ),


        # ----------------------------------
        # Languages
        # ----------------------------------

        SectionType.LANGUAGES: (
            "languages",
        ),


        # ----------------------------------
        # Interests
        # ----------------------------------

        SectionType.INTERESTS: (
            "interests",
            "hobbies",
        ),
    }


    @classmethod
    def detect(
        cls,
        paragraph: Paragraph,
    ) -> SectionType:
        """
        Detect section from paragraph heading.
        """


        text = cls._normalize(
            paragraph.text
        )


        if not text:
            return SectionType.UNKNOWN


        # Remove numbering:
        # 1. EXPERIENCE
        # 02 SKILLS

        text = re.sub(
            r"^\d+[\.\)]?\s*",
            "",
            text,
        )


        for section, keywords in cls._SECTION_MAP.items():

            for keyword in keywords:


                # Exact match

                if text == keyword:
                    return section



                # Heading with suffix
                # Example:
                # "SKILLS & TECHNOLOGIES"

                if text.startswith(keyword):

                    remaining = (
                        text[len(keyword):]
                        .strip()
                    )


                    remaining = remaining.replace(
                        ":",
                        "",
                    ).strip()


                    if not remaining:
                        return section



        return SectionType.UNKNOWN



    @staticmethod
    def _normalize(
        text: str,
    ) -> str:
        """
        Normalize heading text.
        """


        text = text.lower().strip()


        # Remove bullets and separators

        text = re.sub(
            r"[•|_\-]+",
            " ",
            text,
        )


        # Remove trailing colon

        text = re.sub(
            r":+$",
            "",
            text,
        )


        # Normalize spaces

        text = re.sub(
            r"\s+",
            " ",
            text,
        )


        return text.strip()