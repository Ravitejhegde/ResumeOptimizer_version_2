import re

from app.models.job_profile import JobProfile
from .keyword_extractor import KeywordExtractor


class JobDescriptionAnalyzer:

    @staticmethod
    def analyze(text: str) -> JobProfile:

        print("\n========== JOB DESCRIPTION ==========")
        print(text)
        print("=====================================\n")

        profile = JobProfile()

        first_line = text.split("\n")[0].strip()

        if first_line and len(first_line) < 80:
            profile.title = first_line

        match = re.search(
            r"(\d+\+?\s*years?)",
            text,
            re.IGNORECASE,
        )

        if match:
            profile.experience = match.group()

        profile.skills = KeywordExtractor.extract(text)

        print("Detected Skills:")
        print(profile.skills)

        return profile