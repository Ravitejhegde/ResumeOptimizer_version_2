from .optimization_plan import OptimizationPlan


class ResumePlanner:

    @staticmethod
    def build(
        selected_skills: list[str],
    ) -> OptimizationPlan:

        plan = OptimizationPlan()

        # Temporary implementation.
        # Later this becomes our intelligent planning engine.

        plan.skills.extend(selected_skills)

        return plan