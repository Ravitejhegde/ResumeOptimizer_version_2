from app.services.intelligence.skill_ranker import (
    SkillRanker,
)

from app.services.intelligence.replacement_planner import (
    ReplacementPlanner,
)

from app.services.intelligence.section_allocator import (
    SectionAllocator,
)

from app.services.intelligence.resume_planner import (
    ResumePlanner,
)

from app.services.intelligence.skill_decision_engine import (
    SkillDecisionEngine,
)


class IntelligenceEngine:

    def analyze(

        self,

        resume_skills,

        jd_skills,

    ):

        # -------------------------------------
        # Rank Resume Skills
        # -------------------------------------

        ranked_resume = SkillRanker.rank(

            resume_skills,

            jd_skills,

        )

        # -------------------------------------
        # Build Replacement Plan
        # -------------------------------------

        replacement_plan = ReplacementPlanner.build(

            ranked_resume,

            jd_skills,

        )

        # -------------------------------------
        # Allocate Sections
        # -------------------------------------

        replacement_plan.add = SectionAllocator.allocate(

            replacement_plan.add,

        )

        replacement_plan.keep = SectionAllocator.allocate(

            replacement_plan.keep,

        )

        replacement_plan.remove = SectionAllocator.allocate(

            replacement_plan.remove,

        )

        # -------------------------------------
        # Build Resume Plan
        # -------------------------------------

        resume_plan = ResumePlanner.build(

            replacement_plan,

        )

        # -------------------------------------
        # Skill Decisions
        # -------------------------------------

        decisions = SkillDecisionEngine.build(

            keep=replacement_plan.keep,

            remove=replacement_plan.remove,

            add=replacement_plan.add,

        )

        print("\n========== SKILL DECISIONS ==========\n")

        for decision in decisions:

            print(

                f"{decision.action:<8}"

                f"{decision.skill.name:<25}"

                f"Priority : {decision.priority}"

            )

        print("\n====================================\n")

        return resume_plan