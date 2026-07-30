from app.constants.skills import COMMON_SKILLS


class KeywordExtractor:

    @staticmethod
    def extract(text: str) -> list[str]:

        lower = text.lower()

        found = []

        for skill in COMMON_SKILLS:

            if skill.lower() in lower:

                found.append(skill)

        return sorted(set(found))