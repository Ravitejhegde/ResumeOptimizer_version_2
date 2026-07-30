from __future__ import annotations

import logging
import re

from app.engine.models.optimizer.rewrite_result import (
    RewriteResult,
)


logger = logging.getLogger(__name__)


class RewriteValidator:
    """
    Validates individual rewrite results.

    Pipeline:

        RewriteStrategy
              |
              v
        RewriteProcessor
              |
              v
        RewriteValidator
              |
              v
            Writer


    Responsibilities:

        - Reject invalid rewrites.
        - Prevent keyword stuffing.
        - Control text expansion.
        - Protect resume quality.


    Does NOT:

        - Generate text.
        - Modify DOCX.
        - Decide optimization.
    """



    def validate(
        self,
        rewrite: RewriteResult,
    ) -> bool:
        """
        Validate one rewrite.
        """

        if not rewrite.success:

            return False



        if not rewrite.original_text.strip():

            logger.warning(
                "Empty original text paragraph=%s",
                rewrite.paragraph_id,
            )

            return False



        if not rewrite.optimized_text.strip():

            logger.warning(
                "Empty optimized text paragraph=%s",
                rewrite.paragraph_id,
            )

            return False



        if self._has_keyword_stuffing(
            rewrite.optimized_text
        ):

            logger.warning(
                "Keyword stuffing detected=%s",
                rewrite.paragraph_id,
            )

            return False



        if self._excessive_growth(
            rewrite,
        ):

            logger.warning(
                "Excessive rewrite growth=%s",
                rewrite.paragraph_id,
            )

            return False



        return True



    # --------------------------------------------------
    # Keyword stuffing detection
    # --------------------------------------------------

    def _has_keyword_stuffing(
        self,
        text: str,
    ) -> bool:
        """
        Detect unnatural repeated keywords.

        Example rejected:

            AWS AWS AWS Docker Docker Docker
        """


        words = re.findall(
            r"\b[a-zA-Z0-9+#.-]+\b",
            text.lower(),
        )


        frequency: dict[str, int] = {}


        for word in words:

            frequency[word] = (
                frequency.get(word, 0)
                + 1
            )



        # Normal resume words
        ignored_words = {

            "system",
            "systems",
            "application",
            "applications",
            "development",
            "experience",
            "using",
            "built",
            "developed",
            "implemented",

        }



        for word, count in frequency.items():


            if word in ignored_words:

                continue



            # Only extreme repetition

            if (
                len(word) > 3
                and count >= 4
            ):

                return True



        return False



    # --------------------------------------------------
    # Length control
    # --------------------------------------------------

    def _excessive_growth(
        self,
        rewrite: RewriteResult,
    ) -> bool:
        """
        Prevent unnecessary paragraph expansion.

        Example:

            Original:
                20 words

            Optimized:
                200 words

        """


        original_words = len(
            rewrite.original_text.split()
        )


        optimized_words = len(
            rewrite.optimized_text.split()
        )



        if original_words == 0:

            return True



        growth_ratio = (
            optimized_words
            /
            original_words
        )



        # Allow reasonable resume enhancement

        return growth_ratio > 2.5