from __future__ import annotations

import logging

from app.engine.models.document.paragraph import (
    Paragraph,
)

from app.engine.models.planner.rewrite_plan import (
    RewritePlan,
)


logger = logging.getLogger(__name__)


class TechnologyProcessor:
    """
    Extracts technology promotion targets
    from rewrite plans.

    Pipeline:

        RewritePlan
             |
             v
        TechnologyProcessor
             |
             v
        Technology List
             |
             v
        Optimizer / Writer


    Responsibilities:

        - Extract technologies.
        - Validate promotion actions.
        - Remove duplicates.
        - Normalize technology names.


    Does NOT:

        - Generate content.
        - Call AI.
        - Modify document.
    """

    ALLOWED_ACTIONS = {
        "promote",
        "improve",
        "add",
    }


    # --------------------------------------------------

    def process(
        self,
        paragraph: Paragraph,
        rewrites: list[RewritePlan] | None,
    ) -> tuple[
        Paragraph,
        list[str],
    ]:
        """
        Extract technologies applicable
        to one paragraph.
        """


        if not rewrites:

            logger.debug(
                "[TechnologyProcessor] "
                "No rewrite plans paragraph=%s",
                paragraph.id,
            )

            return (
                paragraph,
                [],
            )


        technologies: list[str] = []

        seen: set[str] = set()



        for rewrite in rewrites:


            if not self._is_valid_action(
                rewrite
            ):

                continue



            technology = (
                self._normalize(
                    rewrite.technology
                )
            )



            if technology is None:

                logger.warning(

                    "[TechnologyProcessor] "
                    "Missing technology "
                    "paragraph=%s",

                    paragraph.id,

                )

                continue



            key = technology.lower()



            if key in seen:

                continue



            seen.add(
                key
            )


            technologies.append(
                technology
            )



        logger.info(

            "[TechnologyProcessor] "
            "paragraph=%s technologies=%s",

            paragraph.id,

            technologies,

        )


        return (
            paragraph,
            technologies,
        )


    # --------------------------------------------------

    def _is_valid_action(
        self,
        rewrite: RewritePlan,
    ) -> bool:
        """
        Validate rewrite intent.
        """


        if rewrite.action is None:

            return False


        action = (
            rewrite.action
            .strip()
            .lower()
        )


        if action not in self.ALLOWED_ACTIONS:

            logger.debug(

                "[TechnologyProcessor] "
                "Skipping action=%s",

                action,

            )

            return False


        return True



    # --------------------------------------------------

    def _normalize(
        self,
        technology: str | None,
    ) -> str | None:
        """
        Normalize technology names.

        Keeps readable output.
        """


        if not technology:

            return None


        value = (
            technology
            .strip()
        )


        if not value:

            return None


        # Preserve common acronyms

        replacements = {

            "aws": "AWS",

            "docker": "Docker",

            "sql": "SQL",

            "html": "HTML",

            "css": "CSS",

            "javascript": "JavaScript",

            "typescript": "TypeScript",

            "nodejs": "Node.js",

            "fastapi": "FastAPI",

            "postgresql": "PostgreSQL",

        }


        lower = value.lower()


        return replacements.get(
            lower,
            value,
        )