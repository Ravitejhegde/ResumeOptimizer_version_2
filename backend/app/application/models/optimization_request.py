from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class OptimizationRequest:
    """
    Application request for a complete
    resume optimization.
    """

    resume_path: str

    job_description: str

    output_path: str

    role_id: str

    resume_id: str

    selected_skills: list[str] = field(
        default_factory=list
    )