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

    CORE_ENGINEERING_CATEGORIES = {

        SkillCategory.PROGRAMMING,

        SkillCategory.FRONTEND,

        SkillCategory.BACKEND,

        SkillCategory.DATABASE,

        SkillCategory.FRAMEWORK,

        SkillCategory.DEVOPS,

        SkillCategory.CLOUD,

        SkillCategory.TOOLS,

    }

    @classmethod
    def _should_keep(
        cls,
        skill,
        matched: set[str],
    ) -> bool:

        # -----------------------------------------
        # Explicit JD Match
        # -----------------------------------------

        if skill.name.lower() in matched:
            return True

        # -----------------------------------------
        # Core Engineering Skills
        # -----------------------------------------

        if skill.category in cls.CORE_ENGINEERING_CATEGORIES:
            return True

        # -----------------------------------------
        # High Confidence Resume Skills
        # -----------------------------------------

        if getattr(skill, "confidence", 0.0) >= 0.7:
            return True

        return False

    @classmethod
    def _build_skill_lists(
        cls,
        reasoning,
        resume,
    ):

        keep = []
        remove = []
        add = []

        matched = {

            skill.lower()

            for skill in reasoning.matched

        }

        # -----------------------------------------
        # KEEP / REMOVE
        # -----------------------------------------

        for skill in resume.skills:

            if cls._should_keep(
                skill,
                matched,
            ):

                reason = (

                    "Matched with Job Description"

                    if skill.name.lower() in matched

                    else "Valuable engineering skill"

                )

                keep.append(

                    SkillDecision(

                        skill=skill,

                        action=SkillAction.KEEP,

                        priority=min(
                            int(
                                getattr(
                                    skill,
                                    "confidence",
                                    1.0,
                                )
                                * 100
                            ),
                            100,
                        ),

                        reason=reason,

                    )

                )

            else:

                remove.append(

                    SkillDecision(

                        skill=skill,

                        action=SkillAction.REMOVE,

                        priority=10,

                        reason="Low confidence and not required",

                    )

                )

        # -----------------------------------------
        # ADD
        # -----------------------------------------

        for gap in reasoning.missing:

            try:

                category = SkillCategory(
                    gap.category
                )

            except (ValueError, TypeError):

                category = SkillCategory.OTHER

            new_skill = Skill(

                name=gap.name,

                category=category,

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

        return (
            keep,
            remove,
            add,
        )

    @classmethod
    def build(
        cls,
        resume,
        jd,
    ) -> OptimizationPlan:

        # -----------------------------------------
        # Role Transition
        # -----------------------------------------

        transition = RoleTransitionEngine.find(

            resume.detected_role,

            jd.target_role,

        )

        # -----------------------------------------
        # Brain Reasoning
        # -----------------------------------------

        reasoning = ReasoningEngine.analyze(

            resume,

            jd,

        )

        keep, remove, add = cls._build_skill_lists(

            reasoning,

            resume,

        )

        # -----------------------------------------
        # Capacity Planning
        # -----------------------------------------

        capacity = CapacityManager.calculate(

            resume,

            keep,

            remove,

            add,

        )

        # -----------------------------------------
        # Replacement Planning
        # -----------------------------------------

        replacement = ReplacementEngine.build(

            keep=capacity["keep"],

            remove=remove,

            add=capacity["add"],

            capacity=capacity["capacity"],

        )

        # -----------------------------------------
        # Role Promotion
        # -----------------------------------------

        if transition:

            promoted = {

                skill.lower()

                for skill in transition.promote

            }

            for item in replacement["add"]:

                if item.skill.name.lower() in promoted:

                    item.priority = min(
                        item.priority + 20,
                        100,
                    )

        # -----------------------------------------
        # Final Optimization Plan
        # -----------------------------------------

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