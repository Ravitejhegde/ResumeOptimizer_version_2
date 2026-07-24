import re

from app.services.intelligence.translator.paragraph_type import (
    ParagraphType,
)


class ParagraphClassifier:

    HEADINGS = {

        "PROFESSIONAL SUMMARY",
        "SUMMARY",
        "INTERNSHIP EXPERIENCE",
        "WORK EXPERIENCE",
        "EXPERIENCE",
        "PROJECTS",
        "SKILLS",
        "EDUCATION",
        "CERTIFICATIONS",

    }

    @classmethod
    def classify(
        cls,
        paragraph,
    ) -> ParagraphType:

        text = paragraph.text.strip()

        if not text:

            return ParagraphType.EMPTY

        upper = text.upper()

        # ---------------------------------
        # Section Heading
        # ---------------------------------

        if upper in cls.HEADINGS:

            return ParagraphType.HEADING

        # ---------------------------------
        # Contact
        # ---------------------------------

        if "@" in text:

            return ParagraphType.CONTACT

        if re.search(r"\d{10}", text):

            return ParagraphType.CONTACT

        if "linkedin" in text.lower():

            return ParagraphType.CONTACT

        if "github" in text.lower():

            return ParagraphType.CONTACT

        # ---------------------------------
        # Name
        # ---------------------------------

        words = text.split()

        if (
            len(words) <= 3
            and text == text.title()
            and "|" not in text
            and ":" not in text
        ):

            return ParagraphType.NAME

        # ---------------------------------
        # Job Title
        # ---------------------------------

        if "|" in text and (
            "Developer" in text
            or "Engineer" in text
        ):

            return ParagraphType.JOB_TITLE

        # ---------------------------------
        # Company
        # ---------------------------------

        if "|" in text and "-" in text:

            return ParagraphType.COMPANY

        # ---------------------------------
        # Skills
        # ---------------------------------

        if ":" in text:

            prefixes = [

                "Frontend",
                "Backend",
                "Programming",
                "Database",
                "Tools",

            ]

            for prefix in prefixes:

                if text.startswith(prefix):

                    return ParagraphType.SKILLS

        # ---------------------------------
        # Education
        # ---------------------------------

        if (
            "CGPA" in text
            or "Bachelor" in text
            or "Master" in text
        ):

            return ParagraphType.EDUCATION

        # ---------------------------------
        # Project Technology
        # ---------------------------------

        if "•" in text:

            return ParagraphType.PROJECT_TECHNOLOGY

        # ---------------------------------
        # Project Title
        # ---------------------------------

        if (
    len(text) < 100
    and not text.startswith("Developed")
    and not text.startswith("Implemented")
    and not text.startswith("Collaborated")
    and not text.startswith("Managed")
):

            keywords = [

        "Management System",
        "Management",
        "Application",
        "Platform",
        "Portal",
        "Dashboard",

    ]

            for keyword in keywords:

                if keyword in text:

                    return ParagraphType.PROJECT_TITLE

        # ---------------------------------
        # Project / Experience Description
        # ---------------------------------

        if (
            text.startswith("Developed")
            or text.startswith("Implemented")
            or text.startswith("Collaborated")
            or text.startswith("Managed")
        ):

            return ParagraphType.PROJECT_DESCRIPTION

        # ---------------------------------
        # Default
        # ---------------------------------

        return ParagraphType.EXPERIENCE

    @classmethod
    def should_rewrite(
        cls,
        paragraph,
    ) -> bool:

        paragraph_type = cls.classify(
            paragraph
        )

        return paragraph_type in {

            ParagraphType.SUMMARY,
            ParagraphType.EXPERIENCE,
            ParagraphType.PROJECT_DESCRIPTION,

        }