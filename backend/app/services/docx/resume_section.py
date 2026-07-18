from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ResumeSection:
    name: str
    priority: int
    can_optimize: bool
    allow_skill_insertion: bool
    allow_overflow: bool