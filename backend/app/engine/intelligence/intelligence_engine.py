from __future__ import annotations


from app.engine.intelligence.builders.strategy_builder import (
    StrategyBuilder,
)

from app.engine.intelligence.detectors.role_detector import (
    RoleDetector,
)

from app.engine.intelligence.planners.promotion_planner import (
    PromotionPlanner,
)

from app.engine.intelligence.scorers.priority_scorer import (
    PriorityScorer,
)

from app.engine.intelligence.scorers.skill_gap_scorer import (
    SkillGapScorer,
)

from app.engine.intelligence.selectors.technology_selector import (
    TechnologySelector,
)

from app.engine.models.analysis.analysis_result import (
    AnalysisResult,
)

from app.engine.models.intelligence.optimization_strategy import (
    OptimizationStrategy,
)

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


class IntelligenceEngine:
    """
    Converts analysis into optimization intelligence.

    Flow:

        AnalysisResult
              |
              v
        Role Detection
              |
              v
        Skill Gap Analysis
              |
              v
        Priority Scoring
              |
              v
        Technology Selection
              |
              v
        Promotion Planning
              |
              v
        Optimization Strategy
    """


    def __init__(
        self,
        knowledge: KnowledgeManager,
    ) -> None:


        self._role_detector = RoleDetector(
            knowledge,
        )


        self._gap_scorer = SkillGapScorer()


        self._priority_scorer = PriorityScorer()


        self._selector = TechnologySelector()


        # IMPORTANT:
        # PromotionPlanner now uses KnowledgeManager
        self._planner = PromotionPlanner(
            knowledge,
        )


        self._builder = StrategyBuilder()



    def build(
        self,
        analysis: AnalysisResult,
    ) -> OptimizationStrategy:


        # ----------------------------------
        # Detect target role
        # ----------------------------------

        role = self._role_detector.detect(
            analysis,
        )


        # ----------------------------------
        # Calculate skill gaps
        # ----------------------------------

        gap = self._gap_scorer.score(
            analysis,
        )


        print(
            "\n========== INTELLIGENCE DEBUG =========="
        )

        print("\nRole:")
        print(role)


        print("\nSkill Gap:")
        print(gap)



        # ----------------------------------
        # Score priorities
        # ----------------------------------

        priorities = self._priority_scorer.score(
            gap,
        )


        print("\nPriorities:")
        print(priorities)



        # ----------------------------------
        # Select technologies
        # ----------------------------------

        selected = self._selector.select(
            priorities,
        )


        print("\nSelected Technologies:")
        print(selected)



        # ----------------------------------
        # Build promotion plan
        # ----------------------------------

        promotion_plan = self._planner.build(
            selected,
        )


        print("\nPromotion Plan:")
        print(promotion_plan)


        print(
            "\n========================================\n"
        )



        # ----------------------------------
        # Attach intelligence data
        # ----------------------------------

        analysis.role = role

        analysis.skill_gap = gap



        # ----------------------------------
        # Create final strategy
        # ----------------------------------

        strategy = self._builder.build(

            analysis=analysis,

            role=role,

            promotion_plan=promotion_plan,

        )


        analysis.optimization_strategy = strategy


        return strategy