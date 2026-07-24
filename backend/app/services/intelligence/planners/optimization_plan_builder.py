from app.services.intelligence.models import (
    OptimizationPlan,
)


class OptimizationPlanBuilder:
    """
    Builds an optimization plan from
    ResumeAnalysis and JDAnalysis.
    """

    @classmethod
    def build(
        cls,
        knowledge,
        job_description,
    ) -> OptimizationPlan:

        keep = []
        remove = []
        add = []

        # -----------------------------------------
        # Extract JD skills from JDAnalysis
        # -----------------------------------------

        jd_skills = []

        for skill in getattr(job_description, "skills", []):

            skill_name = getattr(
                skill,
                "name",
                str(skill),
            )

            jd_skills.append(skill_name)

        jd_skill_set = {

            skill.lower().strip()

            for skill in jd_skills

        }

        # -----------------------------------------
        # Compare Resume Skills
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
        # Missing JD Skills
        # -----------------------------------------

        resume_skill_set = {

            skill.lower().strip()

            for skill in resume_skills

        }

        for skill in jd_skills:

            if skill.lower().strip() not in resume_skill_set:

                add.append(skill)

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

            jd_skills=jd_skills,

            selected_skills=add,

            max_skill_lines=5,

        )