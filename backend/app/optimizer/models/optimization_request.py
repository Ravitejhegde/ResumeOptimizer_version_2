"""
app.optimizer.models.optimization_request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the input to the OptimizerEngine.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.planner.blueprint.optimization_blueprint import (
    OptimizationBlueprint,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)
from app.job_understanding.models.job_understanding import (
    JobUnderstanding,
)


@dataclass(slots=True)
class OptimizationRequest:
    """
    Request consumed by the OptimizerEngine.

    Combines everything required to perform
    AI-driven resume optimization.
    """

    # -------------------------------------------------
    # Resume
    # -------------------------------------------------

    document: DocumentModel

    resume: ResumeUnderstanding

    # -------------------------------------------------
    # Job
    # -------------------------------------------------

    job: JobUnderstanding

    # -------------------------------------------------
    # Planner Output
    # -------------------------------------------------

    blueprint: OptimizationBlueprint

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    @property
    def ready(self) -> bool:
        """
        True if the request contains all
        required optimization inputs.
        """

        return all(
            (
                self.document,
                self.resume,
                self.job,
                self.blueprint,
            )
        )