from __future__ import annotations

import logging

from app.engine.models.optimizer.optimization_result import (
    OptimizationResult,
)

from app.engine.optimizer.validators.rewrite_validator import (
    RewriteValidator,
)


logger = logging.getLogger(__name__)


class OptimizationValidator:
    """
    Validates optimizer output.

    Pipeline:

        Optimizer
            |
            v
    OptimizationResult
            |
            v
    OptimizationValidator
            |
            v
        Writer


    Responsibilities:

        - Validate document state.
        - Validate rewrite objects.
        - Remove unsafe rewrites.
        - Add warnings.
        - Protect writer pipeline.


    Does NOT:

        - Generate text.
        - Modify DOCX.
        - Decide optimization strategy.
    """



    def __init__(
        self,
    ) -> None:

        self._rewrite_validator = (
            RewriteValidator()
        )



    # --------------------------------------------------
    # Main validation
    # --------------------------------------------------

    def validate(
        self,
        result: OptimizationResult,
    ) -> OptimizationResult:
        """
        Validate optimization result.
        """

        warnings: list[str] = []



        # ----------------------------------
        # Document validation
        # ----------------------------------

        if result.document is None:

            warnings.append(
                "Optimization document is missing."
            )


            result.success = False


            result.warnings.extend(
                warnings
            )


            return result



        if result.document.is_empty:

            warnings.append(
                "Document is empty."
            )



        # ----------------------------------
        # Rewrite validation
        # ----------------------------------

        valid_rewrites = []



        for rewrite in result.rewrites:


            if not rewrite.paragraph_id:

                warnings.append(
                    "Rewrite missing paragraph id."
                )

                continue



            if not rewrite.optimized_text.strip():

                warnings.append(

                    f"Empty optimized text "
                    f"paragraph={rewrite.paragraph_id}"

                )

                continue



            # ----------------------------------
            # Deep rewrite validation
            # ----------------------------------

            if not self._rewrite_validator.validate(
                rewrite
            ):

                warnings.append(

                    f"Rewrite rejected "
                    f"paragraph={rewrite.paragraph_id}"

                )

                continue



            valid_rewrites.append(
                rewrite
            )



        result.rewrites = valid_rewrites



        # ----------------------------------
        # No rewrite warning
        # ----------------------------------

        if not result.rewrites:

            warnings.append(
                "No valid rewrite changes generated."
            )



        # ----------------------------------
        # Final state
        # ----------------------------------

        result.warnings.extend(
            warnings
        )


        result.success = (

            result.document is not None

            and

            not result.document.is_empty

        )



        logger.info(

            "[OptimizationValidator] "
            "rewrites=%s warnings=%s success=%s",

            len(result.rewrites),

            len(result.warnings),

            result.success,

        )



        return result