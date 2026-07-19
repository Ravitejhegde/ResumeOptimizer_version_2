from dataclasses import dataclass


@dataclass(slots=True)
class SkillOccurrence:

    name: str

    category: str

    section: str

    paragraph_id: int