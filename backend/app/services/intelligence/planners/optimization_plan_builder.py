from app.services.intelligence.models import (
    OptimizationPlan,
)

from app.services.intelligence.planners.skill_matcher import (
    SkillMatcher,
)

from app.services.intelligence.planners.replacement_engine import (
    ReplacementEngine,
)

from app.services.intelligence.planners.capacity_manager import (
    CapacityManager,
)

from app.services.intelligence.planners.role_transition_engine import (
    RoleTransitionEngine,
)


class OptimizationPlanBuilder:
    """
    Builds the complete optimization plan
    using all planner components.
    """

    @classmethod
    def build(

        cls,

        resume,

        jd,

    ) -> OptimizationPlan:

        # ------------------------------------
        # Role Transition
        # ------------------------------------

        transition = RoleTransitionEngine.find(

            resume.detected_role,

            jd.target_role,

        )

        # ------------------------------------
        # Skill Matching
        # ------------------------------------

        keep, remove, add = SkillMatcher.match(

            resume,

            jd,

        )

        # ------------------------------------
        # Capacity Planning
        # ------------------------------------

        capacity = CapacityManager.calculate(

            resume,

            keep,

            remove,

            add,

        )

        # ------------------------------------
        # Replacement Planning
        # ------------------------------------

        replacement = ReplacementEngine.build(

            keep=capacity["keep"],

            remove=remove,

            add=capacity["add"],

            capacity=capacity["capacity"],

        )

        # ------------------------------------
        # Merge Transition Rules
        # ------------------------------------

        if transition:

            promoted = {

                skill.lower()

                for skill in transition.promote

            }

            for item in replacement["add"]:

                if item.skill.name.lower() in promoted:

                    item.priority += 20

        # ------------------------------------
        # Build Final Plan
        # ------------------------------------

        return OptimizationPlan(

            source_role=resume.detected_role,

            target_role=jd.target_role,

            keep=replacement["keep"],

            remove=[],

            add=replacement["add"],

            warnings=[],

        )