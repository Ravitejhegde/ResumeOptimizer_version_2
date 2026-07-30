from __future__ import annotations

import logging

from app.engine.analyzer.document_analyzer import (
    DocumentAnalyzer,
)

from app.engine.intelligence.intelligence_engine import (
    IntelligenceEngine,
)

from app.engine.models.optimizer.optimization_request import (
    OptimizationRequest,
)

from app.engine.models.optimizer.optimization_result import (
    OptimizationResult,
)

from app.engine.optimizer.optimizer_engine import (
    OptimizerEngine,
)

from app.engine.planner.planner_engine import (
    PlannerEngine,
)

from app.engine.writer.engine.writer_engine import (
    WriterEngine,
)

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


logger = logging.getLogger(__name__)



class ResumeOptimizationEngine:
    """
    ResumeOptimizer V3 Orchestrator.

    Pipeline:

        Document
            |
            v
        Analyzer
            |
            v
        Intelligence
            |
            v
        Planner
            |
            v
        OptimizerEngine
            |
            v
        AI Pipeline
            |
            v
        Writer
    """



    def __init__(
        self,
    ) -> None:


        self._knowledge = KnowledgeManager()

        self._knowledge.initialize()



        self._analyzer = DocumentAnalyzer(
            self._knowledge,
        )


        self._intelligence = IntelligenceEngine(
            self._knowledge,
        )


        self._planner = PlannerEngine()


        self._optimizer = OptimizerEngine()


        self._writer = WriterEngine()



    async def optimize(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResult:
        """
        Execute complete optimization pipeline.
        """



        logger.info(
            "[Orchestrator] Starting optimization."
        )



        document = request.document



        # ----------------------------------
        # ANALYZE
        # ----------------------------------

        analysis = (
            self._analyzer.analyze(

                document=document,

                job_description=(
                    request.metadata.get(
                        "job_description"
                    )
                ),

            )
        )


        logger.info(
            "[Orchestrator] Analysis completed."
        )



        # ----------------------------------
        # INTELLIGENCE
        # ----------------------------------

        strategy = (
            self._intelligence.build(
                analysis
            )
        )


        logger.info(
            "[Orchestrator] Intelligence completed."
        )



        # ----------------------------------
        # PLANNING
        # ----------------------------------

        plan = (
            self._planner.build(

                strategy=strategy,

                document=document,

            )
        )


        logger.info(
            "[Orchestrator] Plan created sections=%s",
            len(
                plan.sections
            ),
        )



        # ----------------------------------
        # Attach AI CONTEXT
        # ----------------------------------

        request.plan = plan


        request.job_context = analysis


        request.knowledge_context = strategy



        logger.info(
            "[Orchestrator] AI context attached."
        )



        # ----------------------------------
        # AI OPTIMIZATION
        # ----------------------------------

        result = await (

            self._optimizer.optimize(
                request
            )

        )


        logger.info(
            "[Orchestrator] Optimization completed rewrites=%s",

            len(
                result.rewrites
            ),

        )



        # ----------------------------------
        # WRITER
        # ----------------------------------

        if result.rewrites:


            source_file = (
                request.metadata.get(
                    "source_file"
                )
            )


            output_file = (
                request.metadata.get(
                    "output_file"
                )
            )


            if source_file and output_file:


                self._writer.write(

                    result=result,

                    source_file=source_file,

                    output_file=output_file,

                )


                logger.info(
                    "[Orchestrator] DOCX written."
                )


        else:

            logger.warning(
                "[Orchestrator] No rewrites generated."
            )



        return result