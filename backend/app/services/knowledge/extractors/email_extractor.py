import re


class EmailExtractor:
    """
    Extracts email addresses from resume text.
    """

    EMAIL_PATTERN = re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    @classmethod
    def extract(
        cls,
        text: str,
    ) -> str:

        match = cls.EMAIL_PATTERN.search(
            text,
        )

        if match:
            return match.group()

        return ""