from __future__ import annotations

import logging

from app.engine.ai import (
    AIContextFactory,
    AIServiceFactory,
)

from app.engine.models.optimizer.optimization_request import (
    OptimizationRequest,
)

from app.engine.models.optimizer.optimization_result import (
    OptimizationResult,
)

from app.engine.optimizer.executors.paragraph_executor import (
    ParagraphExecutor,
)

from app.engine.optimizer.executors.section_executor import (
    SectionExecutor,
)

from app.engine.optimizer.intelligence.relevance_scorer import (
    RelevanceScorer,
)

from app.engine.optimizer.intelligence.rewrite_strategy import (
    RewriteStrategy,
)

from app.engine.optimizer.processors.rewrite_processor import (
    RewriteProcessor,
)

from app.engine.optimizer.processors.technology_processor import (
    TechnologyProcessor,
)

from app.engine.optimizer.validators.optimization_validator import (
    OptimizationValidator,
)
from app.engine.ai.services.ai_response_mapper import (
    AIResponseMapper,
)
from app.engine.ai.validators.ai_response_validator import (
    AIResponseValidator,
)


logger = logging.getLogger(__name__)


class OptimizerEngine:
    """
    Executes resume optimization.

    Pipeline:

        OptimizationRequest
              |
              |
        +-------------+
        |             |
        v             v

       AI Path     Legacy Path

        |             |
        v             v

    AIOptimization  RewriteResult

        |
        v

      Writer


    Strategy:

        AI optimization is primary.

        Legacy deterministic optimization
        remains fallback during migration.


    Does NOT:

        - Modify DOCX.
        - Write files.
        - Build prompts.
        - Call AI directly.
    """



    def __init__(
        self,
    ) -> None:


        # ------------------------------
        # AI Pipeline
        # ------------------------------

        self._context_factory = (
            AIContextFactory()
        )


        self._ai_service = (
            AIServiceFactory.create()
        )
        self._response_mapper = (
            AIResponseMapper()
        )
        self._ai_validator = (
            AIResponseValidator()
)

        # ------------------------------
        # Legacy Pipeline
        # ------------------------------

        self._section_executor = (
            SectionExecutor()
        )


        self._paragraph_executor = (
            ParagraphExecutor()
        )


        self._technology_processor = (
            TechnologyProcessor()
        )


        self._relevance = (
            RelevanceScorer()
        )


        self._strategy = (
            RewriteStrategy()
        )


        self._rewrite_processor = (
            RewriteProcessor()
        )



        # ------------------------------
        # Validation
        # ------------------------------

        self._validator = (
            OptimizationValidator()
        )



    async def optimize(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResult:
        """
        Execute optimization.

        AI path:

            One resume
              |
              v
            One AI call


        Fallback:

            Existing rewrite engine.
        """



        logger.info(
            "[OptimizerEngine] "
            "Starting optimization."
        )



        # ==================================
        # PRIMARY AI PATH
        # ==================================

        if request.has_ai_context():

            logger.info(
                "[OptimizerEngine] "
                "Using AI optimization path."
            )


            return await (
                self._optimize_with_ai(
                    request
                )
            )



        # ==================================
        # FALLBACK PATH
        # ==================================

        logger.info(
            "[OptimizerEngine] "
            "AI context missing. "
            "Using legacy optimizer."
        )


        return (
            self._optimize_legacy(
                request
            )
        )



    # ==================================================
    # AI Optimization
    # ==================================================

    async def _optimize_with_ai(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResult:


        context = (
            self._context_factory.create(

                document=request.document,

                job_data=request.job_context,

                knowledge_data=request.knowledge_context,

            )
        )


        ai_response = await (
            self._ai_service.optimize(
                context
            )
        )


        logger.info(

            "[OptimizerEngine] "
            "AI optimization completed."

        )



        # ----------------------------------
# Convert AI response
# into Writer compatible rewrites
# ----------------------------------

        # ----------------------------------
# Validate AI response
# ----------------------------------

        valid, errors = (
            self._ai_validator.validate(
                ai_response
            )
        )


        if not valid:

            logger.warning(

                "[OptimizerEngine] "
                "AI response rejected errors=%s",

                errors,

            )


            result = OptimizationResult(

                document=request.document,

                rewrites=[],

                changed_paragraphs=0,

            )


            result.warnings.extend(
                errors
            )


            return result



# ----------------------------------
# Convert AI response
# into Writer rewrites
# ----------------------------------

        rewrites = (
            self._response_mapper.map(
                ai_response
            )
        )


        logger.info(

            "[OptimizerEngine] "
            "AI rewrites mapped=%s",

            len(rewrites),

        )



        result = OptimizationResult(

            document=request.document,

            rewrites=rewrites,

            changed_paragraphs=len(
            rewrites
            ),

        )



        return (
            self._validator.validate(
                result
            )
        )



    # ==================================================
    # Legacy Optimization
    # ==================================================

    def _optimize_legacy(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResult:


        document = request.document


        rewrites = []

        changed = 0



        for section in request.plan.sections:


            paragraphs = (
                self._section_executor.execute(
                    document,
                    section,
                )
            )



            for paragraph in paragraphs:


                paragraph, applicable = (
                    self._paragraph_executor.execute(
                        paragraph,
                        request.plan.rewrites,
                    )
                )


                if not applicable:

                    continue



                _, technologies = (
                    self._technology_processor.process(
                        paragraph,
                        applicable,
                    )
                )


                if not technologies:

                    continue



                relevance = (
                    self._relevance.score(
                        paragraph,
                        technologies,
                    )
                )


                if relevance < 0.4:

                    continue



                optimized_text = (
                    self._strategy.generate(
                        paragraph,
                        technologies,
                    )
                )


                rewrite = (
                    self._rewrite_processor.process(
                        paragraph=paragraph,

                        optimized_text=optimized_text,

                        reason=", ".join(
                            technologies
                        ),

                    )
                )



                if rewrite.success:

                    rewrites.append(
                        rewrite
                    )

                    changed += 1



        result = OptimizationResult(

            document=document,

            rewrites=rewrites,

            changed_paragraphs=changed,

        )


        return (
            self._validator.validate(
                result
            )
        )