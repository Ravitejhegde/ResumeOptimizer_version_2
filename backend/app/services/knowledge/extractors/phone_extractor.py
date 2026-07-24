import re


class PhoneExtractor:
    """
    Extracts phone numbers from resume text.
    """

    PHONE_PATTERNS = [
        re.compile(
            r"(?:\+91[\s-]?)?[6-9]\d{9}"
        ),
        re.compile(
            r"(?:\+\d{1,3}[\s-]?)?(?:\d[\s-]?){10,15}"
        ),
    ]

    @classmethod
    def extract(
        cls,
        text: str,
    ) -> str:

        for pattern in cls.PHONE_PATTERNS:

            match = pattern.search(
                text,
            )

            if match:

                phone = (
                    match.group()
                    .replace(" ", "")
                    .replace("-", "")
                )

                return phone

        return ""