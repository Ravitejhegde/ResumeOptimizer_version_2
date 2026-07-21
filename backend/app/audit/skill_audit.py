class SkillAudit:

    @classmethod
    def evaluate(
        cls,
        reasoning,
        result,
    ):

        result.matched_skills = list(
            reasoning.matched
        )

        result.missing_skills = [

            gap.name

            for gap in reasoning.missing

        ]

        result.extra_skills = list(
            reasoning.extra
        )

        return result