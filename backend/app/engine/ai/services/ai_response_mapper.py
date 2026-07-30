from __future__ import annotations

import logging

from app.engine.ai.models.ai_response import (
    AIOptimizationResponse,
)

from app.engine.models.optimizer.rewrite_result import (
    RewriteResult,
)


logger = logging.getLogger(__name__)


class AIResponseMapper:
    """
    Converts AI output into optimizer rewrite results.

    Flow:

        AIOptimizationResponse
                |
                v
          AIResponseMapper
                |
                v
          RewriteResult[]

                |
                v

          Writer Pipeline


    Responsibilities:

        - Convert AI sections into rewrite objects.
        - Preserve paragraph identifiers.
        - Prepare Writer-compatible output.


    Does NOT:

        - Generate text.
        - Validate AI quality.
        - Modify DOCX.
    """



    def map(
        self,
        response: AIOptimizationResponse,
    ) -> list[RewriteResult]:
        """
        Convert AI response into rewrite results.
        """


        rewrites: list[RewriteResult] = []


        # ----------------------------------
        # Summary
        # ----------------------------------

        if response.summary:

            rewrites.append(

                RewriteResult(

                    paragraph_id="summary",

                    success=True,

                    original_text="",

                    optimized_text=response.summary,

                    reason="AI summary optimization",

                    confidence=response.confidence,

                    formatting_preserved=True,

                    original_length=0,

                    optimized_length=len(
                        response.summary
                    ),

                )

            )



        # ----------------------------------
        # Experience
        # ----------------------------------

        for section in response.experience:

            rewrite = self._map_section(
                section
            )

            if rewrite:

                rewrites.append(
                    rewrite
                )



        # ----------------------------------
        # Projects
        # ----------------------------------

        for section in response.projects:

            rewrite = self._map_section(
                section
            )

            if rewrite:

                rewrites.append(
                    rewrite
                )



        logger.info(

            "[AIResponseMapper] "
            "Mapped AI rewrites=%s",

            len(rewrites),

        )


        return rewrites



    # --------------------------------------------------
    # Section mapper
    # --------------------------------------------------

    def _map_section(
        self,
        section,
    ) -> RewriteResult | None:
        """
        Convert one AI section.
        """


        if not section.optimized_text:

            return None



        paragraph_id = (
            section.identifier
            or
            section.section_type
        )


        return RewriteResult(

            paragraph_id=paragraph_id,

            success=True,

            original_text=(
                section.original_text
                or ""
            ),

            optimized_text=(
                section.optimized_text
            ),

            reason=(
                section.reason
                or
                "AI resume optimization"
            ),

            confidence=(
                section.confidence
            ),

            formatting_preserved=True,

            original_length=len(
                section.original_text
                or ""
            ),

            optimized_length=len(
                section.optimized_text
            ),

        )