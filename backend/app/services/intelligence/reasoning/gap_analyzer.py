from .models import (
    SkillGap,
)


class GapAnalyzer:

    @classmethod
    def analyze(

        cls,

        resume_skills,

        jd_skills,

    ):

        matched = []
        missing = []
        extra = []

        resume = {

            skill.name.lower()

            for skill in resume_skills

        }

        jd = {

            skill.name.lower()

            for skill in jd_skills

        }

        for skill in jd_skills:

            if skill.name.lower() in resume:

                matched.append(
                    skill.name
                )

            else:

                missing.append(

                    SkillGap(

                        name=skill.name,

                        priority=50,

                        required=True,

                        reason="Missing from resume",

                    )

                )

        for skill in resume_skills:

            if skill.name.lower() not in jd:

                extra.append(
                    skill.name
                )

        return (

            matched,

            missing,

            extra,

        )