from dataclasses import dataclass, field

from .skill import Skill
from .resume_section import ResumeSection


@dataclass
class ResumeAnalysis:
    """
    Structured knowledge extracted from a resume.
    """

    detected_role: str = ""

    sections: list[ResumeSection] = field(
        default_factory=list
    )

    skills: list[Skill] = field(
        default_factory=list
    )

    summary: list = field(
        default_factory=list
    )

    experience: list = field(
        default_factory=list
    )

    projects: list = field(
        default_factory=list
    )

    education: list = field(
        default_factory=list
    )

    hyperlinks: list[str] = field(
        default_factory=list
    )

    total_skill_capacity: int = 0