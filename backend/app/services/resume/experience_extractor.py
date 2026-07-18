import re


class ExperienceExtractor:

    @staticmethod
    def extract(text: str) -> list[str]:

        matches = re.findall(
            r"\d+\+?\s+years?",
            text,
            flags=re.IGNORECASE,
        )

        return matches