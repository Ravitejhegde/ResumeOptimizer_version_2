from __future__ import annotations

import logging

from app.engine.optimizer.intelligence.relevance_scorer import (
    RelevanceScorer,
)

from app.engine.optimizer.intelligence.rewrite_strategy import (
    RewriteStrategy,
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

from app.engine.optimizer.processors.rewrite_processor import (
    RewriteProcessor,
)

from app.engine.optimizer.processors.technology_processor import (
    TechnologyProcessor,
)

from app.engine.optimizer.validators.optimization_validator import (
    OptimizationValidator,
)


logger = logging.getLogger(__name__)


class OptimizerEngine:
    """
    Executes OptimizationPlan.

    Pipeline:

        OptimizationPlan
              |
              v
        SectionExecutor
              |
              v
        ParagraphExecutor
              |
              v
        TechnologyProcessor
              |
              v
        RelevanceScorer
              |
              v
        RewriteStrategy
              |
              v
        RewriteProcessor
              |
              v
        OptimizationResult


    Does NOT:

        - Modify DOCX
        - Write files
        - Call AI directly
    """



    def __init__(
        self,
    ) -> None:


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


        self._validator = (
            OptimizationValidator()
        )



    # --------------------------------------------------
    # Main optimization execution
    # --------------------------------------------------

    def optimize(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResult:


        document = request.document


        logger.info(
            "[Optimizer] Starting optimization"
        )


        logger.info(
            "[Optimizer] Sections=%s",
            len(request.plan.sections),
        )



        rewrites = []

        changed = 0



        # ----------------------------------
        # Process planned sections
        # ----------------------------------

        for section in request.plan.sections:



            logger.info(

                "[Optimizer] Processing section=%s",

                section.section,

            )



            paragraphs = (
                self._section_executor.execute(
                    document,
                    section,
                )
            )



            logger.info(

                "[Optimizer] Paragraphs found=%s",

                len(paragraphs),

            )



            # ----------------------------------
            # Process paragraphs
            # ----------------------------------

            for paragraph in paragraphs:



                paragraph, applicable = (
                    self._paragraph_executor.execute(
                        paragraph,
                        request.plan.rewrites,
                    )
                )



                if not applicable:

                    continue



                # ----------------------------------
                # Extract technologies
                # ----------------------------------

                _, technologies = (
                    self._technology_processor.process(
                        paragraph,
                        applicable,
                    )
                )



                if not technologies:

                    continue



                # ----------------------------------
                # Relevance scoring
                # ----------------------------------

                relevance = (
                    self._relevance.score(
                        paragraph,
                        technologies,
                    )
                )



                logger.info(

                    "[Optimizer] "
                    "paragraph=%s relevance=%.2f",

                    paragraph.id,

                    relevance,

                )



                if relevance < 0.4:

                    logger.info(

                        "[Optimizer] "
                        "Skipping paragraph=%s",

                        paragraph.id,

                    )

                    continue



                # ----------------------------------
                # Generate optimized text
                # ----------------------------------

                optimized_text = (
                    self._strategy.generate(
                        paragraph,
                        technologies,
                    )
                )



                # ----------------------------------
                # Create rewrite result
                # ----------------------------------

                result = (
                    self._rewrite_processor.process(
                        paragraph=paragraph,
                        optimized_text=optimized_text,
                        reason=", ".join(
                            technologies
                        ),
                    )
                )



                if result.success:

                    changed += 1


                    rewrites.append(
                        result
                    )



                logger.info(

                    "[Optimizer] "
                    "rewrite paragraph=%s success=%s",

                    result.paragraph_id,

                    result.success,

                )



        # ----------------------------------
        # Create result
        # ----------------------------------

        result = OptimizationResult(

            document=document,

            rewrites=rewrites,

            changed_paragraphs=changed,

        )



        logger.info(

            "[Optimizer] "
            "Generated rewrites=%s",

            len(rewrites),

        )



        # ----------------------------------
        # Validate
        # ----------------------------------

        result = (
            self._validator.validate(
                result
            )
        )



        logger.info(

            "[Optimizer] "
            "Validation complete rewrites=%s",

            len(result.rewrites),

        )


        return result