from dataclasses import dataclass

from .skill import Skill

from .enums import SkillAction


@dataclass
class SkillDecision:

    skill: Skill

    action: SkillAction

    reason: str

    priority: int