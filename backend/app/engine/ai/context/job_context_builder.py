from __future__ import annotations

import logging
from typing import Any

from app.engine.ai.models.job_context import (
    JobContext,
)


logger = logging.getLogger(__name__)


class JobContextBuilder:
    """
    Converts JD analysis output into AI JobContext.

    Flow:

        JD Analyzer / Intelligence
                |
                v
        JobContextBuilder
                |
                v
           JobContext
                |
                v
       OptimizationContext
                |
                v
              AI


    Responsibilities:

        - Collect target role.
        - Collect required skills.
        - Collect responsibilities.
        - Preserve JD intelligence.


    Does NOT:

        - Parse raw JD.
        - Call AI.
        - Generate optimization.
    """



    def build(
        self,
        job_data: Any,
    ) -> JobContext:
        """
        Build structured job context.

        Supports flexible input because
        Analyzer output may evolve.
        """


        context = JobContext()



        # --------------------------------------------------
        # Role information
        # --------------------------------------------------

        context.role_title = (
            self._get_value(
                job_data,
                "role_title",
            )
            or
            self._get_value(
                job_data,
                "target_role",
            )
        )


        context.role_family = (
            self._get_value(
                job_data,
                "role_family",
            )
        )


        context.seniority = (
            self._get_value(
                job_data,
                "seniority",
            )
        )



        # --------------------------------------------------
        # Skills
        # --------------------------------------------------

        context.required_skills = (
            self._get_list(
                job_data,
                "required_skills",
            )
        )


        context.preferred_skills = (
            self._get_list(
                job_data,
                "preferred_skills",
            )
        )


        context.skill_categories = (
            self._get_dict(
                job_data,
                "skill_categories",
            )
        )



        # --------------------------------------------------
        # Responsibilities
        # --------------------------------------------------

        context.responsibilities = (
            self._get_list(
                job_data,
                "responsibilities",
            )
        )


        context.technical_expectations = (
            self._get_list(
                job_data,
                "technical_expectations",
            )
        )


        context.soft_skill_expectations = (
            self._get_list(
                job_data,
                "soft_skill_expectations",
            )
        )



        # --------------------------------------------------
        # Requirements
        # --------------------------------------------------

        context.experience_requirement = (
            self._get_value(
                job_data,
                "experience_requirement",
            )
        )


        context.education_requirement = (
            self._get_value(
                job_data,
                "education_requirement",
            )
        )



        # --------------------------------------------------
        # Raw backup
        # --------------------------------------------------

        context.raw_description = (
            self._get_value(
                job_data,
                "raw_description",
            )
        )



        # --------------------------------------------------
        # Unknown future fields
        # --------------------------------------------------

        if isinstance(
            job_data,
            dict,
        ):

            known = {

                "role_title",
                "target_role",
                "role_family",
                "seniority",
                "required_skills",
                "preferred_skills",
                "skill_categories",
                "responsibilities",
                "technical_expectations",
                "soft_skill_expectations",
                "experience_requirement",
                "education_requirement",
                "raw_description",

            }


            for key, value in job_data.items():

                if key not in known:

                    context.add_metadata(
                        key,
                        value,
                    )



        logger.info(

            "[JobContextBuilder] "
            "role=%s skills=%s",

            context.role_title,

            len(
                context.all_required_skills()
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

            value = source.get(
                key
            )

            return (
                str(value)
                if value is not None
                else None
            )


        value = getattr(
            source,
            key,
            None,
        )


        return (
            str(value)
            if value is not None
            else None
        )



    @staticmethod
    def _get_list(
        source: Any,
        key: str,
    ) -> list[str]:

        value = (
            JobContextBuilder
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
            value
        ]



    @staticmethod
    def _get_dict(
        source: Any,
        key: str,
    ) -> dict[str, list[str]]:

        if isinstance(
            source,
            dict,
        ):

            value = source.get(
                key
            )

            if isinstance(
                value,
                dict,
            ):

                return value


        return {}