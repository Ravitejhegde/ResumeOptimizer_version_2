from __future__ import annotations

import re

from app.engine.common.enums import SectionType
from app.engine.models.document.paragraph import Paragraph


class SectionReader:
    """
    Detects logical resume sections.

    Responsibilities:
        - Identify section headings.
        - Normalize heading text.
        - Map heading to SectionType.

    Does not:
        - Modify paragraphs.
        - Analyze content.
        - Extract skills.
    """

    _SECTION_MAP: dict[SectionType, tuple[str, ...]] = {

        SectionType.SUMMARY: (
            "summary",
            "professional summary",
            "profile",
            "objective",
            "career objective",
            "about",
            "career profile",
        ),


        SectionType.EXPERIENCE: (
            "experience",
            "work experience",
            "employment",
            "professional experience",
            "career history",
            "work history",
        ),


        SectionType.PROJECTS: (
            "projects",
            "academic projects",
            "personal projects",
            "key projects",
            "project experience",
        ),


        SectionType.SKILLS: (
            "skills",
            "technical skills",
            "core skills",
            "competencies",
            "expertise",
            "technologies",
            "technical expertise",
        ),


        SectionType.EDUCATION: (
            "education",
            "academic background",
            "qualification",
            "qualifications",
            "academic qualification",
        ),


        SectionType.CERTIFICATIONS: (
            "certifications",
            "licenses",
            "certificates",
            "courses",
        ),


        SectionType.ACHIEVEMENTS: (
            "achievements",
            "awards",
            "honours",
            "honors",
        ),


        SectionType.PUBLICATIONS: (
            "publications",
            "research",
        ),


        SectionType.LANGUAGES: (
            "languages",
        ),


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

        heading = cls._normalize(
            paragraph.text
        )


        if not heading:
            return SectionType.UNKNOWN


        for section, keywords in cls._SECTION_MAP.items():

            if heading in keywords:

                return section


            for keyword in keywords:

                if cls._is_heading_match(
                    heading,
                    keyword,
                ):
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


        text = re.sub(
            r"[:\-|]+$",
            "",
            text,
        )


        text = re.sub(
            r"\s+",
            " ",
            text,
        )


        return text


    @staticmethod
    def _is_heading_match(
        heading: str,
        keyword: str,
    ) -> bool:
        """
        Handles common heading variations.
        """

        if len(heading) > 50:
            return False


        return (
            heading.startswith(keyword)
            and len(
                heading.split()
            )
            <= 4
        )