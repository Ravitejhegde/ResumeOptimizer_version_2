from __future__ import annotations

from app.engine.intelligence.category_classifier import (
    CategoryClassifier,
)
from app.engine.intelligence.evidence_engine import (
    EvidenceEngine,
)
from app.engine.intelligence.optimization_strategy_builder import (
    OptimizationStrategyBuilder,
)
from app.engine.intelligence.paragraph_assignment_engine import (
    ParagraphAssignmentEngine,
)
from app.engine.intelligence.priority_engine import (
    PriorityEngine,
)
from app.engine.intelligence.promotion_engine import (
    PromotionEngine,
)
from app.engine.intelligence.role_classifier import (
    RoleClassifier,
)
from app.engine.intelligence.role_detector import (
    RoleDetector,
)
from app.engine.intelligence.technology_ranker import (
    TechnologyRanker,
)

from app.engine.models.analysis_result import (
    AnalysisResult,
)
from app.engine.models.document import (
    Document,
)


class IntelligenceEngine:
    """
    Central coordinator for ResumeOptimizer's
    intelligence layer.

    This class orchestrates all intelligence
    modules and produces one OptimizationStrategy.
    """

    def __init__(self) -> None:

        self._role_detector = RoleDetector()

        self._role_classifier = RoleClassifier()

        self._category_classifier = (
            CategoryClassifier()
        )

        self._technology_ranker = (
            TechnologyRanker()
        )

        self._priority_engine = (
            PriorityEngine()
        )

        self._evidence_engine = (
            EvidenceEngine()
        )

        self._promotion_engine = (
            PromotionEngine()
        )

        self._assignment_engine = (
            ParagraphAssignmentEngine()
        )

        self._strategy_builder = (
            OptimizationStrategyBuilder()
        )

    def build(
        self,
        document: Document,
        analysis: AnalysisResult,
    ):

        role = self._role_detector.detect(
            " ".join(
                analysis.keywords.normalized_skills
            )
        )

        role_profile = (
            self._role_classifier.classify(
                role
            )
        )

        ranked = (
            self._technology_ranker.rank(
                analysis.keywords.normalized_skills,
                role_profile,
            )
        )

        evidence = (
            self._evidence_engine.analyze(
                document,
                analysis.keywords.normalized_skills,
            )
        )

        priorities = (
            self._priority_engine.calculate(
                ranked
            )
        )

        promotions = (
            self._promotion_engine.build(
                priorities,
                evidence,
            )
        )

        assignments = (
            self._assignment_engine.assign(
                document,
                promotions,
            )
        )

        return self._strategy_builder.build(
            role_profile,
            promotions,
            assignments,
        )