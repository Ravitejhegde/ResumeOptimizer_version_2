class PlanAudit:

    @classmethod
    def evaluate(
        cls,
        plan,
        result,
    ):

        result.recommendations = [

            item.skill.name

            for item in plan.add

        ]

        result.risks = list(
            plan.warnings
        )

        return result