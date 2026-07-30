from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.engine.ai.models.job_context import (
    JobContext,
)

from app.engine.ai.models.knowledge_context import (
    KnowledgeContext,
)

from app.engine.ai.models.optimization_constraints import (
    OptimizationConstraints,
)

from app.engine.ai.models.resume_context import (
    ResumeContext,
)



@dataclass(slots=True)
class OptimizationContext:
    """
    Complete AI optimization context.

    This is the single knowledge package
    consumed by PromptBuilder.

    Flow:

        ResumeContext
              +
        JobContext
              +
        KnowledgeContext
              +
        OptimizationConstraints

                    |
                    v

          OptimizationContext

                    |
                    v

              PromptBuilder


    Responsibilities:

        - Combine all AI input information.
        - Provide one consistent context object.
        - Support future AI features.


    Does NOT:

        - Create prompts.
        - Call AI.
        - Validate responses.
        - Modify documents.
    """


    # --------------------------------------------------
    # Core contexts
    # --------------------------------------------------

    resume: ResumeContext

    job: JobContext

    knowledge: KnowledgeContext

    constraints: OptimizationConstraints



    # --------------------------------------------------
    # Optimization objective
    # --------------------------------------------------

    objective: str = (
        "Optimize resume for target job while preserving authenticity and formatting."
    )


    # --------------------------------------------------
    # AI task configuration
    # --------------------------------------------------

    task_type: str = (
        "full_resume_optimization"
    )


    version: str = (
        "v1"
    )


    # --------------------------------------------------
    # Additional dynamic data
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )



    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store additional context data.
        """

        self.metadata[key] = value



    def summary(
        self,
    ) -> dict[str, Any]:
        """
        Debug summary without exposing
        complete resume content.
        """

        return {

            "task":
                self.task_type,

            "target_role":
                self.job.role_title,

            "resume_sections":
                self.resume.section_count(),

            "missing_skills":
                len(
                    self.knowledge.missing_skills
                ),

            "required_skills":
                len(
                    self.job.all_required_skills()
                ),

            "constraints":
                len(
                    self.constraints
                    .to_instruction_list()
                ),

        }



    def has_context(
        self,
    ) -> bool:
        """
        Check whether AI has enough information.
        """

        return all(
            [
                self.resume,
                self.job,
                self.knowledge,
                self.constraints,
            ]
        )