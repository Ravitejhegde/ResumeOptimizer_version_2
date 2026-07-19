from dataclasses import dataclass, field

from .skill import Skill


@dataclass
class JDAnalysis:
    """
    Structured knowledge extracted from a Job Description.
    """

    target_role: str = ""

    skills: list[Skill] = field(
        default_factory=list
    )

    original_text: str = ""