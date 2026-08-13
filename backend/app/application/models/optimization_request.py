from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class OptimizationRequest:
    """
    Application request for a complete
    resume optimization.
    """

    resume_path: str

    job_description: str

    output_path: str