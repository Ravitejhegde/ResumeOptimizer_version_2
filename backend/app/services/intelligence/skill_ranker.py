from app.services.intelligence.skill import Skill


class SkillRanker:

    @staticmethod
    def rank(
        resume_skills: list[Skill],
        jd_skills: list[Skill],
    ) -> list[Skill]:

        jd_names = {

            skill.name.lower()

            for skill in jd_skills

        }

        for skill in resume_skills:

            name = skill.name.lower()

            if name in jd_names:

                skill.score = 100

                skill.keep = True

            else:

                skill.score = 20

                skill.remove = True

        return sorted(

            resume_skills,

            key=lambda x: x.score,

            reverse=True,

        )