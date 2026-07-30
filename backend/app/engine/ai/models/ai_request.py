from __future__ import annotations

from dataclasses import dataclass, field

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
class AIOptimizationRequest:
    """
    Complete input package for AI optimization.

    This represents the SINGLE AI request.

    Flow:

        ResumeContext
              +
        JobContext
              +
        KnowledgeContext
              +
        Constraints

              |
              v

        AIOptimizationRequest

              |
              v

        PromptBuilder

              |
              v

        OpenRouter


    Responsibilities:

        - Combine all AI input context.
        - Ensure one-call architecture.
        - Provide complete information to PromptBuilder.


    Does NOT:

        - Build prompts.
        - Call AI.
        - Parse response.
    """


    # --------------------------------------------------
    # Core context
    # --------------------------------------------------

    resume: ResumeContext

    job: JobContext

    knowledge: KnowledgeContext

    constraints: OptimizationConstraints


    # --------------------------------------------------
    # Request metadata
    # --------------------------------------------------

    request_id: str | None = None


    version: str = (
        "v1"
    )


    # --------------------------------------------------
    # Additional dynamic context
    # --------------------------------------------------

    metadata: dict[str, str] = field(
        default_factory=dict,
    )


    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value: str,
    ) -> None:
        """
        Add dynamic request information.
        """

        self.metadata[key] = value



    def summary(
        self,
    ) -> dict[str, object]:
        """
        Small debug representation.

        Does not expose full resume data.
        """

        return {

            "request_id": self.request_id,

            "target_role":
                self.job.role_title,

            "missing_skills":
                len(
                    self.knowledge.missing_skills
                ),

            "sections":
                self.resume.section_count(),

            "constraint_count":
                len(
                    self.constraints.to_instruction_list()
                ),

        }