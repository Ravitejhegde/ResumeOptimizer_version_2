from __future__ import annotations

import logging

from app.engine.models.document.paragraph import (
    Paragraph,
)

from app.engine.models.optimizer.rewrite_result import (
    RewriteResult,
)


logger = logging.getLogger(__name__)


class RewriteProcessor:
    """
    Converts optimized paragraph text
    into RewriteResult.

    Pipeline:

        Paragraph
             +
        Optimized Text
             |
             v
        RewriteResult
             |
             v
        Writer


    Responsibilities:

        - Compare original and optimized text.
        - Create rewrite metadata.
        - Measure change size.
        - Protect document quality.


    Does NOT:

        - Generate text.
        - Call AI.
        - Modify DOCX.
    """


    # --------------------------------------------------

    def process(
        self,
        paragraph: Paragraph,
        optimized_text: str | None,
        reason: str = "",
    ) -> RewriteResult:
        """
        Build rewrite result.
        """


        original_text = (
            paragraph.text
            or ""
        )


        optimized_text = (
            optimized_text
            or original_text
        )


        changed = (
            self._normalize(
                original_text
            )
            !=
            self._normalize(
                optimized_text
            )
        )


        confidence = (
            self._calculate_confidence(
                original_text,
                optimized_text,
                changed,
            )
        )


        formatting_safe = (
            self._is_formatting_safe(
                original_text,
                optimized_text,
            )
        )


        if changed:

            logger.info(

                "[RewriteProcessor] "
                "Paragraph=%s changed "
                "length %s -> %s",

                paragraph.id,

                len(original_text),

                len(optimized_text),

            )


        else:

            logger.debug(

                "[RewriteProcessor] "
                "No change paragraph=%s",

                paragraph.id,

            )



        return RewriteResult(

            paragraph_id=paragraph.id,

            success=changed,

            original_text=original_text,

            optimized_text=optimized_text,

            reason=reason,

            confidence=confidence,

            formatting_preserved=formatting_safe,

            original_length=len(
                original_text
            ),

            optimized_length=len(
                optimized_text
            ),

        )


    # --------------------------------------------------

    @staticmethod
    def _normalize(
        text: str,
    ) -> str:
        """
        Normalize text comparison.
        """

        return (
            " ".join(
                text
                .strip()
                .split()
            )
            .lower()
        )


    # --------------------------------------------------

    @staticmethod
    def _calculate_confidence(
        original: str,
        optimized: str,
        changed: bool,
    ) -> float:
        """
        Estimate rewrite reliability.

        This is not AI confidence.
        It is validation confidence.
        """


        if not changed:

            return 0.0


        original_length = len(
            original
        )


        optimized_length = len(
            optimized
        )


        if original_length == 0:

            return 0.5


        growth_ratio = (
            optimized_length
            /
            original_length
        )


        # Too much expansion is risky

        if growth_ratio > 3:

            return 0.4


        if growth_ratio > 2:

            return 0.7


        return 0.95



    # --------------------------------------------------

    @staticmethod
    def _is_formatting_safe(
        original: str,
        optimized: str,
    ) -> bool:
        """
        Checks whether rewrite is likely
        safe for existing formatting.

        Writer handles actual runs.
        """


        # Empty replacement is unsafe

        if not optimized.strip():

            return False



        # Extremely large replacements
        # may break layout

        if len(optimized) > len(original) * 3:

            return False


        return True