from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class OptimizationResponse:
    """
    Final response returned by the
    application workflow.
    """

    success: bool

    message: str

    output_path: str = ""

    generated_resume_id: str = ""