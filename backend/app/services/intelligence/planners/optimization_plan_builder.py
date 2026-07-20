from app.services.intelligence.models import (
    OptimizationPlan,
    Skill,
    SkillAction,
    SkillCategory,
    SkillDecision,
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

from app.services.intelligence.reasoning.reasoning_engine import (
    ReasoningEngine,
)


class OptimizationPlanBuilder:
    """
    Builds the complete optimization plan
    using the Brain v3 Reasoning Engine.
    """

    @staticmethod
    def _build_skill_lists(
        reasoning,
        resume,
    ):
        keep = []
        remove = []
        add = []

        # -------------------------
        # KEEP / REMOVE
        # -------------------------

        matched = {
            skill.lower()
            for skill in reasoning.matched
        }

        for skill in resume.skills:

            if skill.name.lower() in matched:

                keep.append(
                    SkillDecision(
                        skill=skill,
                        action=SkillAction.KEEP,
                        priority=100,
                        reason="Matched with Job Description",
                    )
                )

            else:

                remove.append(
                    SkillDecision(
                        skill=skill,
                        action=SkillAction.REMOVE,
                        priority=10,
                        reason="Not required",
                    )
                )

        # -------------------------
        # ADD
        # -------------------------

        for gap in reasoning.missing:

            new_skill = Skill(
                name=gap.name,
                category=SkillCategory.OTHER,
                section="Skills",
                source="job_description",
                confidence=1.0,
            )

            add.append(
                SkillDecision(
                    skill=new_skill,
                    action=SkillAction.ADD,
                    priority=gap.priority,
                    reason=gap.reason,
                )
            )

        return keep, remove, add

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
        # Brain v3 Reasoning
        # ------------------------------------

        reasoning = ReasoningEngine.analyze(
            resume,
            jd,
        )

        keep, remove, add = cls._build_skill_lists(
            reasoning,
            resume,
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
        # Role Promotion
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
        # Final Plan
        # ------------------------------------

        return OptimizationPlan(
            source_role=resume.detected_role,
            target_role=jd.target_role,
            keep=replacement["keep"],
            remove=remove,
            add=replacement["add"],
            warnings=[
                risk.description
                for risk in reasoning.risks
            ],
        )