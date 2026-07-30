from __future__ import annotations

from app.engine.models.optimizer.optimization_result import (
    OptimizationResult,
)


class OptimizationValidator:
    """
    Validates the optimization output before
    it is passed to the Writer.
    """

    # --------------------------------------------------

    def validate(
        self,
        result: OptimizationResult,
    ) -> OptimizationResult:

        warnings: list[str] = []

        if not result.rewrites:

            warnings.append(
                "No paragraphs were optimized."
            )

        if result.document.is_empty:

            warnings.append(
                "Document is empty."
            )

        result.warnings.extend(
            warnings,
        )

        result.success = (
            len(warnings) == 0
        )

        return result
