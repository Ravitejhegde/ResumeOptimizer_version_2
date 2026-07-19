from dataclasses import dataclass

from .enums import SkillCategory


@dataclass
class Skill:

    name: str

    category: SkillCategory

    section: str

    source: str

    confidence: int = 100

    priority: int = 0