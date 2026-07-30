from __future__ import annotations

import logging

from app.engine.ai.context.job_context_builder import (
    JobContextBuilder,
)

from app.engine.ai.context.knowledge_context_builder import (
    KnowledgeContextBuilder,
)

from app.engine.ai.context.resume_context_builder import (
    ResumeContextBuilder,
)

from app.engine.ai.context.optimization_context import (
    OptimizationContext,
)

from app.engine.ai.models.optimization_constraints import (
    OptimizationConstraints,
)

from app.engine.models.document.document import (
    Document,
)


logger = logging.getLogger(__name__)


class AIContextFactory:
    """
    Creates complete OptimizationContext for AI.

    Flow:

        Document
           +
        Job Intelligence
           +
        Knowledge Builder Output

                |
                v

        AIContextFactory

                |
                v

        OptimizationContext

                |
                v

        PromptBuilder


    Responsibilities:

        - Coordinate all context builders.
        - Create one AI-ready context.
        - Keep AI integration clean.


    Does NOT:

        - Build prompts.
        - Call AI.
        - Optimize resume.
        - Modify documents.
    """



    def __init__(
        self,
    ) -> None:

        self._resume_builder = (
            ResumeContextBuilder()
        )

        self._job_builder = (
            JobContextBuilder()
        )

        self._knowledge_builder = (
            KnowledgeContextBuilder()
        )



    def create(
        self,
        document: Document,
        job_data,
        knowledge_data,
    ) -> OptimizationContext:
        """
        Build complete AI optimization context.
        """



        logger.info(
            "[AIContextFactory] Building AI context."
        )



        resume_context = (
            self._resume_builder.build(
                document
            )
        )


        job_context = (
            self._job_builder.build(
                job_data
            )
        )


        knowledge_context = (
            self._knowledge_builder.build(
                knowledge_data
            )
        )



        constraints = (
            OptimizationConstraints()
        )



        context = OptimizationContext(

            resume=resume_context,

            job=job_context,

            knowledge=knowledge_context,

            constraints=constraints,

        )



        logger.info(

            "[AIContextFactory] "
            "Context created role=%s",

            job_context.role_title,

        )


        return context