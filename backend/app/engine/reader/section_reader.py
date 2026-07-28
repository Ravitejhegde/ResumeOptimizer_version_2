from __future__ import annotations

import re

from app.engine.common.enums import SectionType
from app.engine.models.document.paragraph import Paragraph


class SectionReader:
    """
    Detects the logical resume section to which a
    paragraph belongs.

    This reader performs only section identification.
    It never modifies the paragraph.
    """

    _SECTION_MAP: dict[SectionType, tuple[str, ...]] = {

        SectionType.SUMMARY: (
            "summary",
            "professional summary",
            "profile",
            "objective",
            "career objective",
            "about",
        ),

        SectionType.EXPERIENCE: (
            "experience",
            "work experience",
            "employment",
            "professional experience",
            "career history",
        ),

        SectionType.PROJECTS: (
            "projects",
            "academic projects",
            "personal projects",
            "key projects",
        ),

        SectionType.SKILLS: (
            "skills",
            "technical skills",
            "core skills",
            "competencies",
            "expertise",
        ),

        SectionType.EDUCATION: (
            "education",
            "academic background",
            "qualification",
            "qualifications",
        ),

        SectionType.CERTIFICATIONS: (
            "certifications",
            "licenses",
            "certificates",
        ),

        SectionType.ACHIEVEMENTS: (
            "achievements",
            "awards",
            "honours",
            "honors",
        ),

        SectionType.PUBLICATIONS: (
            "publications",
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

        heading = paragraph.text.strip().lower()

        heading = re.sub(
            r"[:\-]+$",
            "",
            heading,
        )

        for section, keywords in cls._SECTION_MAP.items():

            if heading in keywords:
                return section

        return SectionType.UNKNOWN




