from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.engine.models.document.document import (
    Document,
)

from app.engine.models.planner.optimization_plan import (
    OptimizationPlan,
)



@dataclass(slots=True)
class OptimizationRequest:
    """
    Input provided to optimization pipeline.

    Contains:

        Document
            +
        Optimization Plan
            +
        AI intelligence context


    Flow:

        API
         |
         v
    OptimizationRequest
         |
         v
    OptimizerEngine
         |
         v
    AIContextFactory
         |
         v
    AI Service


    Does NOT:

        - Build prompts.
        - Call AI.
        - Modify DOCX.
    """


    # --------------------------------------------------
    # Core optimization input
    # --------------------------------------------------

    document: Document

    plan: OptimizationPlan



    # --------------------------------------------------
    # Intelligence inputs
    # --------------------------------------------------

    job_context: Any | None = None

    knowledge_context: Any | None = None



    # --------------------------------------------------
    # Request tracking
    # --------------------------------------------------

    request_id: str | None = None



    # --------------------------------------------------
    # Writer constraints
    # --------------------------------------------------

    preserve_formatting: bool = True



    # --------------------------------------------------
    # Runtime metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )



    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def has_ai_context(
        self,
    ) -> bool:
        """
        Check whether AI pipeline
        has required context.
        """

        return (

            self.job_context is not None

            and

            self.knowledge_context is not None

        )



    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add dynamic request metadata.
        """

        self.metadata[key] = value