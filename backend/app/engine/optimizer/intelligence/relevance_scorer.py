from __future__ import annotations

import logging

from app.engine.models.document.paragraph import (
    Paragraph,
)


logger = logging.getLogger(__name__)


class RelevanceScorer:
    """
    Scores paragraph relevance for technology promotion.

    Purpose:

        Decide whether a paragraph is
        suitable for optimization.

    Score:

        0.0 - 0.3
            Low relevance

        0.4 - 0.7
            Medium relevance

        0.8 - 1.0
            Strong rewrite candidate


    Does NOT:

        - Rewrite text.
        - Modify document.
        - Select technologies.
    """



    def score(
        self,
        paragraph: Paragraph,
        technologies: list[str],
    ) -> float:
        """
        Calculate paragraph relevance.
        """


        if not technologies:

            return 0.0



        text = (
            paragraph.text
            .lower()
            .strip()
        )


        if not text:

            return 0.0



        score = 0.0



        # ----------------------------------
        # Resume action verbs
        # ----------------------------------

        action_words = [

            "built",
            "developed",
            "created",
            "implemented",
            "designed",
            "engineered",
            "deployed",
            "integrated",
            "automated",
            "optimized",

        ]



        for word in action_words:

            if word in text:

                score += 0.08



        # ----------------------------------
        # Technical context
        # ----------------------------------

        technical_words = [

            "api",
            "backend",
            "frontend",
            "application",
            "system",
            "platform",
            "service",
            "architecture",
            "database",
            "model",
            "algorithm",
            "pipeline",

        ]



        for word in technical_words:

            if word in text:

                score += 0.05



        # ----------------------------------
        # Project / Experience relevance
        # ----------------------------------

        if paragraph.section:

            section = str(
                paragraph.section
            ).lower()


            if (
                "experience" in section
                or
                "project" in section
            ):

                score += 0.15



        # ----------------------------------
        # Existing technology overlap
        # ----------------------------------

        matched = 0


        for technology in technologies:

            if technology.lower() in text:

                matched += 1



        if matched:

            score += min(
                matched * 0.15,
                0.30,
            )



        # ----------------------------------
        # Paragraph length quality
        # ----------------------------------

        word_count = len(
            text.split()
        )


        if 10 <= word_count <= 80:

            score += 0.10



        elif word_count < 5:

            score -= 0.15



        # ----------------------------------
        # Final normalization
        # ----------------------------------

        score = max(
            score,
            0.0,
        )


        score = min(
            score,
            1.0,
        )



        logger.debug(

            "[RelevanceScorer] "
            "paragraph=%s score=%.2f",

            paragraph.id,

            score,

        )



        return score