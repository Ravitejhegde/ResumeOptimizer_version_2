from dataclasses import dataclass, field

from app.services.intelligence.skill import Skill


@dataclass
class ReplacementPlan:

    keep: list[Skill] = field(default_factory=list)

    remove: list[Skill] = field(default_factory=list)

    add: list[Skill] = field(default_factory=list)


class ReplacementPlanner:

    @staticmethod
    def build(

        ranked_resume: list[Skill],

        jd_skills: list[Skill],

    ) -> ReplacementPlan:

        plan = ReplacementPlan()

        resume_names = {

            skill.name.lower()

            for skill in ranked_resume

        }

        # Keep / Remove
        for skill in ranked_resume:

            if skill.keep:

                plan.keep.append(skill)

            elif skill.remove:

                plan.remove.append(skill)

        # Add missing JD skills
        for skill in jd_skills:

            if skill.name.lower() not in resume_names:

                skill.add = True

                plan.add.append(skill)

        return plan