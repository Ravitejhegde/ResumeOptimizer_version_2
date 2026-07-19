from dataclasses import dataclass, field

from .skill import Skill


@dataclass
class ResumeSection:

    name: str

    skills: list[Skill] = field(
        default_factory=list
    )