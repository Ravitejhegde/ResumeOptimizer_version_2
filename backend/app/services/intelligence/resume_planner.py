from dataclasses import dataclass, field

from app.services.intelligence.skill import Skill
from app.services.intelligence.replacement_planner import (
    ReplacementPlan,
)


@dataclass
class SectionPlan:

    name: str

    keep: list[Skill] = field(default_factory=list)

    remove: list[Skill] = field(default_factory=list)

    add: list[Skill] = field(default_factory=list)


class ResumePlanner:

    @staticmethod
    def build(
        plan: ReplacementPlan,
    ) -> list[SectionPlan]:

        sections: dict[str, SectionPlan] = {}

        def get_section(name: str):

            if name not in sections:

                sections[name] = SectionPlan(
                    name=name,
                )

            return sections[name]

        # Keep
        for skill in plan.keep:

            section = get_section(
                skill.section,
            )

            section.keep.append(skill)

        # Remove
        for skill in plan.remove:

            section = get_section(
                skill.section,
            )

            section.remove.append(skill)

        # Add
        for skill in plan.add:

            section = get_section(
                skill.section,
            )

            section.add.append(skill)

        return list(
            sections.values()
        )