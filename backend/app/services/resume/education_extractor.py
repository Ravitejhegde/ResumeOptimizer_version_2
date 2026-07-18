import re


class EducationExtractor:

    @staticmethod
    def extract(text: str) -> list[str]:

        keywords = [
            "b.e",
            "b.tech",
            "bca",
            "bsc",
            "b.com",
            "mca",
            "m.tech",
            "msc",
            "mba",
            "phd",
            "diploma",
        ]

        text_lower = text.lower()

        result = []

        for keyword in keywords:

            if keyword in text_lower:

                result.append(keyword.upper())

        return result