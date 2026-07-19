import re

from app.services.docx.document_block import (
    DocumentBlock,
)


class SectionDetector:
    """
    Detects resume sections from document blocks.
    """

    SECTION_ALIASES = {

        "professional summary": "SUMMARY",
        "summary": "SUMMARY",
        "profile": "SUMMARY",
        "career objective": "SUMMARY",
        "objective": "SUMMARY",

        "technical skills": "SKILLS",
        "skills": "SKILLS",
        "core skills": "SKILLS",
        "key skills": "SKILLS",

        "experience": "EXPERIENCE",
        "work experience": "EXPERIENCE",
        "professional experience": "EXPERIENCE",
        "employment": "EXPERIENCE",

        "projects": "PROJECTS",
        "academic projects": "PROJECTS",
        "personal projects": "PROJECTS",

        "education": "EDUCATION",
        "academic qualification": "EDUCATION",

        "certifications": "CERTIFICATIONS",
        "certification": "CERTIFICATIONS",

        "achievements": "ACHIEVEMENTS",

        "languages": "LANGUAGES",

        "interests": "INTERESTS",

        "contact": "CONTACT",

    }

    @staticmethod
    def normalize(
        text: str,
    ) -> str:

        text = text.lower()

        text = re.sub(
            r"[^a-z ]",
            "",
            text,
        )

        return text.strip()

    @classmethod
    def detect(
        cls,
        blocks: list[DocumentBlock],
    ):

        detected = []

        current_section = "HEADER"

        for block in blocks:

            text = cls.normalize(
                block.text
            )

            if text in cls.SECTION_ALIASES:

                current_section = cls.SECTION_ALIASES[
                    text
                ]

            detected.append(

                {

                    "block": block,

                    "section": current_section,

                }

            )

        return detected