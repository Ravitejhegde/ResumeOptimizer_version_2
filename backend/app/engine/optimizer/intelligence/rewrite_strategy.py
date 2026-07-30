from __future__ import annotations

import logging

from app.engine.models.document.paragraph import (
    Paragraph,
)


logger = logging.getLogger(__name__)


class RewriteStrategy:
    """
    Creates resume-friendly optimized text.

    Responsibilities:

        Paragraph
             +
        Missing technologies

             |
             v

        Improved resume wording


    Does NOT:

        - Call AI.
        - Modify DOCX.
        - Validate output.
    """



    def generate(
        self,
        paragraph: Paragraph,
        technologies: list[str],
    ) -> str:
        """
        Generate optimized paragraph text.
        """


        original = (
            paragraph.text
            .strip()
        )


        if not original:

            return original



        if not technologies:

            return original



        missing = self._find_missing(
            original,
            technologies,
        )



        if not missing:

            return original



        optimized = (
            self._enhance(
                original,
                missing,
                paragraph.section,
            )
        )


        logger.debug(

            "[RewriteStrategy] "
            "paragraph=%s technologies=%s",

            paragraph.id,

            missing,

        )


        return optimized



    # --------------------------------------------------

    def _find_missing(
        self,
        text: str,
        technologies: list[str],
    ) -> list[str]:

        lower = text.lower()


        return [

            tech

            for tech in technologies

            if tech.lower()
            not in lower

        ]



    # --------------------------------------------------

    def _enhance(
        self,
        text: str,
        technologies: list[str],
        section: str | None,
    ) -> str:
        """
        Creates contextual resume wording.
        """


        technology_text = ", ".join(
            technologies
        )


        section_name = (
            str(section).lower()
            if section
            else ""
        )



        # Experience bullets

        if (
            "experience" in section_name
        ):

            return (

                f"{text}. "
                f"Worked with {technology_text} "
                f"to build and deploy "
                f"scalable software solutions."

            )



        # Project bullets

        if (
            "project" in section_name
        ):

            return (

                f"{text}. "
                f"Implemented {technology_text} "
                f"to enhance system performance "
                f"and application scalability."

            )



        # Generic fallback

        return (

            f"{text}. "
            f"Hands-on experience with "
            f"{technology_text}."

        )