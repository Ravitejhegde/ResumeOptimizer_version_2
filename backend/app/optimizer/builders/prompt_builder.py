"""
app.optimizer.builders.prompt_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds the complete AI prompt.
"""

from __future__ import annotations

from app.optimizer.models.optimization_request import (
    OptimizationRequest,
)

from app.optimizer.prompts.system_prompt import (
    SYSTEM_PROMPT,
)

from app.optimizer.prompts.resume_prompt import (
    build_resume_prompt,
)

from app.optimizer.prompts.job_prompt import (
    build_job_prompt,
)

from app.optimizer.prompts.planner_prompt import (
    build_planner_prompt,
)

from app.optimizer.prompts.output_prompt import (
    OUTPUT_PROMPT,
)


class PromptBuilder:
    """
    Builds the final prompt for AI.
    """

    def build(
        self,
        request: OptimizationRequest,
    ) -> str:
        """
        Build the complete optimization prompt.
        """

        authorized_paragraph_ids: set[str] = set()

        for paragraph_ids in (
            request.blueprint.section_plan.paragraph_ids.values()
        ):
            authorized_paragraph_ids.update(
                paragraph_ids
            )

        sections = [

            SYSTEM_PROMPT,

            build_resume_prompt(
                request.document,
                request.resume,
                authorized_paragraph_ids,
            ),

            build_job_prompt(
                request.job
            ),

            build_planner_prompt(
                request.blueprint
            ),

            OUTPUT_PROMPT,

        ]

        return "\n\n".join(
            sections
        )