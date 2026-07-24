import re


class SkillsSectionLocator:
    """
    Finds the Skills section inside the
    document snapshot.
    """

    HEADINGS = {
        "SKILLS",
        "TECHNICAL SKILLS",
        "TECHNICAL EXPERTISE",
        "CORE SKILLS",
        "KEY SKILLS",
    }

    STOP_HEADINGS = {
        "EDUCATION",
        "PROJECTS",
        "CERTIFICATIONS",
        "EXPERIENCE",
        "WORK EXPERIENCE",
        "INTERNSHIP",
        "INTERNSHIP EXPERIENCE",
        "SUMMARY",
        "PROFESSIONAL SUMMARY",
        "ACHIEVEMENTS",
    }

    @classmethod
    def _normalize(cls, text: str) -> str:

        text = re.sub(r"\s+", " ", text)

        return text.strip().upper()

    @classmethod
    def locate(
        cls,
        snapshot,
    ):

        start = None

        paragraphs = snapshot.paragraphs

        # ----------------------------
        # Find Skills Heading
        # ----------------------------

        for i, paragraph in enumerate(paragraphs):

            heading = cls._normalize(
                paragraph.text
            )

            if heading in cls.HEADINGS:

                start = i

                break

        if start is None:

            return []

        # ----------------------------
        # Collect Skills Paragraphs
        # ----------------------------

        result = []

        for paragraph in paragraphs[start + 1:]:

            heading = cls._normalize(
                paragraph.text
            )

            if heading in cls.STOP_HEADINGS:

                break

            result.append(
                paragraph
            )

        return result