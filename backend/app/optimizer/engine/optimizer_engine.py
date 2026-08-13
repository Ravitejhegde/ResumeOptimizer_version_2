"""
app.optimizer.engine.optimizer_engine

Main orchestration engine for AI resume optimization.
"""

from __future__ import annotations

from app.optimizer.builders.prompt_builder import (
    PromptBuilder,
)
from app.optimizer.clients.ai_client import (
    AIClient,
)
from app.optimizer.models.optimization_request import (
    OptimizationRequest,
)
from app.optimizer.models.optimization_result import (
    OptimizationResult,
)
from app.optimizer.parsers.ai_response_parser import (
    AIResponseParser,
)
from app.optimizer.validators.ai_response_validator import (
    AIResponseValidator,
)


class OptimizerEngine:
    """
    Executes the complete optimization pipeline.
    """

    def __init__(
        self,
    ) -> None:

        self._prompt_builder = PromptBuilder()

        self._client = AIClient()

        self._parser = AIResponseParser()

        self._ai_validator = (
            AIResponseValidator()
        )

    def optimize(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResult:
        """
        Execute optimization.
        """

        if not request.ready:

            return OptimizationResult(
                document=request.document,
                success=False,
                message=(
                    "Optimization request is incomplete."
                ),
            )

        # ----------------------------------
        # Build Prompt
        # ----------------------------------

        prompt = self._prompt_builder.build(
            request
        )

        print("\n========== PROMPT ==========\n")
        print(prompt)

        # ----------------------------------
        # AI Call
        # ----------------------------------

        response = self._client.optimize(
            prompt
        )

        print("\n========== AI RESPONSE ==========\n")
        print(response)

        # ----------------------------------
        # Parse
        # ----------------------------------

        updates = self._parser.parse(
            response
        )

        # ----------------------------------
        # AI Validation
        # ----------------------------------

        ai_errors = (
            self._ai_validator.validate(
                updates
            )
        )

        if ai_errors:

            return OptimizationResult(
                document=request.document,
                paragraph_updates=[],
                warnings=ai_errors,
                success=False,
                message=(
                    "AI response validation failed."
                ),
            )

        # ----------------------------------
        # Success
        # ----------------------------------

        return OptimizationResult(
            document=request.document,
            paragraph_updates=updates,
            success=True,
            message=(
                "Optimization completed successfully."
            ),
        )