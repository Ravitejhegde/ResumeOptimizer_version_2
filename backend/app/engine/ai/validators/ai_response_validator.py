from __future__ import annotations

import logging

from app.engine.ai.models.ai_response import (
    AIOptimizationResponse,
)

from app.engine.ai.guardrails.length_controller import (
    LengthController,
)


logger = logging.getLogger(__name__)



class AIResponseValidator:
    """
    Validates AI generated optimization response.

    New architecture:

        OpenRouter
             |
             v
        AIResponseParser
             |
             v
        AIOptimizationResponse
             |
             v
        AIResponseValidator
             |
             v
        AIResponseMapper
             |
             v
        Writer


    Responsibilities:

        - Validate AI output structure.
        - Detect empty responses.
        - Enforce length safety.
        - Prevent unsafe expansion.


    Does NOT:

        - Modify AI output.
        - Regenerate content.
        - Write DOCX.
    """



    def __init__(
        self,
    ) -> None:

        self._length_controller = (
            LengthController()
        )



    def validate(
        self,
        response: AIOptimizationResponse,
    ) -> tuple[bool, list[str]]:
        """
        Validate AI response.
        """

        errors: list[str] = []



        if response is None:

            return (
                False,
                [
                    "AI response is empty."
                ],
            )



        # ----------------------------------
        # Content validation
        # ----------------------------------

        self._validate_content(
            response,
            errors,
        )



        # ----------------------------------
        # Paragraph validation
        # ----------------------------------

        self._validate_sections(
            response,
            errors,
        )



        # ----------------------------------
        # Length validation
        # ----------------------------------

        self._validate_length(
            response,
            errors,
        )



        # ----------------------------------
        # Identity validation
        # ----------------------------------

        self._validate_identity(
            response,
            errors,
        )



        valid = (
            len(errors) == 0
        )



        logger.info(
            "[AIResponseValidator] valid=%s errors=%s",
            valid,
            len(errors),
        )


        return (
            valid,
            errors,
        )



    # ==================================================
    # Content checks
    # ==================================================

    def _validate_content(
        self,
        response: AIOptimizationResponse,
        errors: list[str],
    ) -> None:
        """
        Ensure AI returned paragraph rewrites.
        """


        rewrites = getattr(
            response,
            "rewrites",
            [],
        )


        paragraphs = getattr(
            response,
            "paragraphs",
            [],
        )


        has_content = bool(
            rewrites
            or paragraphs
            or getattr(
                response,
                "summary",
                None,
            )
        )


        if not has_content:

            errors.append(
                "AI response contains no optimized content."
            )



    # ==================================================
    # Paragraph checks
    # ==================================================

    def _validate_sections(
        self,
        response: AIOptimizationResponse,
        errors: list[str],
    ) -> None:
        """
        Validate paragraph rewrite structure.
        """


        items = (

            getattr(
                response,
                "rewrites",
                None,
            )

            or

            getattr(
                response,
                "paragraphs",
                None,
            )

            or []

        )



        for item in items:


            paragraph_id = getattr(
                item,
                "paragraph_id",
                None,
            )


            optimized_text = getattr(
                item,
                "optimized_text",
                None,
            )



            if not paragraph_id:

                errors.append(
                    "AI rewrite missing paragraph_id."
                )



            if not optimized_text:

                errors.append(
                    "AI rewrite missing optimized_text."
                )



    # ==================================================
    # Length checks
    # ==================================================

    def _validate_length(
        self,
        response: AIOptimizationResponse,
        errors: list[str],
    ) -> None:
        """
        Prevent AI from generating oversized paragraphs.
        """


        items = (

            getattr(
                response,
                "rewrites",
                None,
            )

            or

            getattr(
                response,
                "paragraphs",
                None,
            )

            or []

        )



        for item in items:


            text = getattr(
                item,
                "optimized_text",
                "",
            )


            if not text:

                continue



            word_count = len(
                text.split()
            )



            # Safety limit.
            # Later connect with paragraph budget.

            if word_count > 120:

                errors.append(
                    "AI generated paragraph exceeds length limit."
                )



    # ==================================================
    # Identity protection
    # ==================================================

    def _validate_identity(
        self,
        response: AIOptimizationResponse,
        errors: list[str],
    ) -> None:
        """
        Placeholder for identity safety.

        Future:

            Original Resume Context
                    |
                    v
            AI Response

        Verify:

            - Name unchanged
            - Email unchanged
            - Phone unchanged
            - Links unchanged
        """

        return