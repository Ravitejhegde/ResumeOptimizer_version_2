from app.constants.skills import COMMON_SKILLS


class ResumeSkillExtractor:

    @staticmethod
    def extract(text: str) -> list[str]:

        lower = text.lower()

        skills = []

        for skill in COMMON_SKILLS:

            if skill.lower() in lower:
                skills.append(skill)

        return sorted(set(skills))