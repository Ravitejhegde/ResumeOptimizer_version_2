from app.services.intelligence.models import (
    OptimizationPlan,
)


class OptimizationPlanBuilder:
    """
    Builds an optimization plan from the
    structured ResumeAnalysis and JDAnalysis.
    """

    @classmethod
    def build(
        cls,
        knowledge,
        job_description,
        selected_skills: list[str],
    ) -> OptimizationPlan:

        keep = []
        remove = []
        add = []

        # -----------------------------------------
        # JD Skills
        # -----------------------------------------

        jd_skills = getattr(
            job_description,
            "skills",
            [],
        )

        jd_skill_set = {

            getattr(skill, "name", str(skill))
            .lower()
            .strip()

            for skill in jd_skills

        }

        # -----------------------------------------
        # Resume Skills
        # -----------------------------------------

        resume_skills = []

        for skill in knowledge.skills:

            skill_name = getattr(

                skill,

                "name",

                str(skill),

            )

            resume_skills.append(skill_name)

            if skill_name.lower().strip() in jd_skill_set:

                keep.append(skill_name)

            else:

                remove.append(skill_name)

        # -----------------------------------------
        # Add Only Selected Skills
        # -----------------------------------------

        resume_skill_set = {

            skill.lower().strip()

            for skill in resume_skills

        }

        for skill in selected_skills:

            skill_name = getattr(

                skill,

                "name",

                str(skill),

            )

            if skill_name.lower().strip() not in resume_skill_set:

                add.append(skill_name)

        # -----------------------------------------
        # Build Plan
        # -----------------------------------------

        return OptimizationPlan(

            source_role=knowledge.detected_role,

            target_role=getattr(

                job_description,

                "title",

                knowledge.detected_role,

            ),

            keep=keep,

            remove=remove,

            add=add,

            warnings=[],

            jd_skills=[

                getattr(skill, "name", str(skill))

                for skill in jd_skills

            ],

            selected_skills=selected_skills,

            max_skill_lines=5,

        )