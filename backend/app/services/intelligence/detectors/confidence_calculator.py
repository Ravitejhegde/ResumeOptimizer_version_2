from app.services.intelligence.models import (
    Skill,
)


class ConfidenceCalculator:
    """
    Calculates confidence for each detected skill.

    Higher confidence means the candidate has
    stronger evidence of actually using that skill.
    """

    SECTION_WEIGHT = {

        "EXPERIENCE": 100,

        "PROJECTS": 90,

        "CERTIFICATIONS": 80,

        "SKILLS": 70,

        "SUMMARY": 60,

        "EDUCATION": 30,

        "HEADER": 10,

    }

    @classmethod
    def calculate(

        cls,

        skills: list[Skill],

    ) -> list[Skill]:

        for skill in skills:

            score = cls.SECTION_WEIGHT.get(

                skill.section.upper(),

                50,

            )

            skill.confidence = score

        return skills