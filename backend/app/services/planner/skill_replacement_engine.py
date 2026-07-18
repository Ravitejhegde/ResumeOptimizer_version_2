from dataclasses import dataclass, field


@dataclass(slots=True)
class ReplacementPlan:
    keep: list[str] = field(default_factory=list)
    replace: dict[str, str] = field(default_factory=dict)
    move_to_other_sections: list[str] = field(default_factory=list)


class SkillReplacementEngine:
    """
    Decides which technologies should be kept,
    replaced or moved to another section.
    """

    @staticmethod
    def build(
        resume_skills: list[str],
        selected_skills: list[str],
    ) -> ReplacementPlan:

        plan = ReplacementPlan()

        resume_lower = {
            s.lower(): s
            for s in resume_skills
        }

        selected_lower = {
            s.lower(): s
            for s in selected_skills
        }

        # Already exists in resume
        for key, value in resume_lower.items():

            if key in selected_lower:
                plan.keep.append(value)

        # Missing selected skills
        missing = [
            skill
            for skill in selected_skills
            if skill.lower() not in resume_lower
        ]

        # Candidates for replacement
        replace_candidates = [
            skill
            for skill in resume_skills
            if skill.lower() not in selected_lower
        ]

        for old, new in zip(
            replace_candidates,
            missing,
        ):
            plan.replace[old] = new

        # Remaining skills
        if len(missing) > len(replace_candidates):

            plan.move_to_other_sections.extend(
                missing[len(replace_candidates):]
            )

        return plan