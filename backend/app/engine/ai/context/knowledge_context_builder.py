from __future__ import annotations

import logging
from typing import Any

from app.engine.ai.models.knowledge_context import (
    KnowledgeContext,
)


logger = logging.getLogger(__name__)


class KnowledgeContextBuilder:
    """
    Converts Knowledge Builder / Intelligence output
    into AI-friendly KnowledgeContext.

    Flow:

        Intelligence Layer
              |
              v
        KnowledgeContextBuilder
              |
              v
        KnowledgeContext
              |
              v
        PromptBuilder
              |
              v
        AI


    Responsibilities:

        - Collect role intelligence.
        - Collect skill intelligence.
        - Collect technology relationships.
        - Preserve knowledge source information.


    Does NOT:

        - Analyze JD.
        - Call AI.
        - Generate prompts.
    """



    def build(
        self,
        knowledge: Any,
    ) -> KnowledgeContext:
        """
        Build structured AI knowledge context.

        Supports flexible input because Knowledge Builder
        may evolve over time.
        """

        context = KnowledgeContext()



        # --------------------------------------------------
        # Target role
        # --------------------------------------------------

        context.target_role = (
            self._get_value(
                knowledge,
                "target_role",
            )
        )


        context.role_family = (
            self._get_value(
                knowledge,
                "role_family",
            )
        )



        # --------------------------------------------------
        # Skills
        # --------------------------------------------------

        context.matched_skills = (
            self._get_list(
                knowledge,
                "matched_skills",
            )
        )


        context.missing_skills = (
            self._get_list(
                knowledge,
                "missing_skills",
            )
        )


        context.prioritized_skills = (
            self._get_list(
                knowledge,
                "priorities",
            )
        )



        # --------------------------------------------------
        # Categories
        # --------------------------------------------------

        context.skill_categories = (
            self._get_dict(
                knowledge,
                "categories",
            )
        )



        # --------------------------------------------------
        # Technology relationships
        # --------------------------------------------------

        context.technology_map = (
            self._get_dict(
                knowledge,
                "technology_map",
            )
        )



        # --------------------------------------------------
        # AI guidance
        # --------------------------------------------------

        context.role_expectations = (
            self._get_list(
                knowledge,
                "role_expectations",
            )
        )


        context.optimization_hints = (
            self._get_list(
                knowledge,
                "optimization_hints",
            )
        )



        # --------------------------------------------------
        # Preserve unknown future knowledge
        # --------------------------------------------------

        if isinstance(
            knowledge,
            dict,
        ):

            known_keys = {

                "target_role",
                "role_family",
                "matched_skills",
                "missing_skills",
                "priorities",
                "categories",
                "technology_map",
                "role_expectations",
                "optimization_hints",

            }


            for key, value in knowledge.items():

                if key not in known_keys:

                    context.add_metadata(
                        key,
                        value,
                    )



        logger.info(

            "[KnowledgeContextBuilder] "
            "role=%s missing=%s matched=%s",

            context.target_role,

            len(
                context.missing_skills
            ),

            len(
                context.matched_skills
            ),

        )


        return context



    # --------------------------------------------------
    # Flexible readers
    # --------------------------------------------------

    @staticmethod
    def _get_value(
        source: Any,
        key: str,
    ) -> str | None:

        if isinstance(
            source,
            dict,
        ):

            return source.get(
                key
            )


        return getattr(
            source,
            key,
            None,
        )



    @staticmethod
    def _get_list(
        source: Any,
        key: str,
    ) -> list[str]:

        value = (
            KnowledgeContextBuilder
            ._get_value(
                source,
                key,
            )
        )


        if not value:

            return []


        if isinstance(
            value,
            list,
        ):

            return [
                str(item)
                for item in value
            ]


        return [
            str(value)
        ]



    @staticmethod
    def _get_dict(
        source: Any,
        key: str,
    ) -> dict[str, list[str]]:

        value = (
            KnowledgeContextBuilder
            ._get_value(
                source,
                key,
            )
        )


        if not isinstance(
            value,
            dict,
        ):

            return {}


        return value