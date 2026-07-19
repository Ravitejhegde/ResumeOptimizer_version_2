from dataclasses import dataclass

from app.services.intelligence.skill import Skill


@dataclass
class SkillDecision:

    skill: Skill

    action: str

    reason: str

    priority: int


class SkillDecisionEngine:

    @staticmethod
    def build(

        keep: list[Skill],

        remove: list[Skill],

        add: list[Skill],

    ) -> list[SkillDecision]:

        decisions: list[SkillDecision] = []

        # Keep skills
        for skill in keep:

            decisions.append(

                SkillDecision(

                    skill=skill,

                    action="KEEP",

                    reason="Required or transferable skill",

                    priority=100,

                )

            )

        # Remove skills
        for skill in remove:

            decisions.append(

                SkillDecision(

                    skill=skill,

                    action="REMOVE",

                    reason="Low relevance for target role",

                    priority=10,

                )

            )

        # Add skills
        for skill in add:

            decisions.append(

                SkillDecision(

                    skill=skill,

                    action="ADD",

                    reason="Required by Job Description",

                    priority=90,

                )

            )

        decisions.sort(

            key=lambda d: d.priority,

            reverse=True,

        )

        return decisions