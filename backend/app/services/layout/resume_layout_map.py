from dataclasses import dataclass, field


@dataclass(slots=True)
class SectionLayout:

    name: str

    paragraph_ids: list[int] = field(default_factory=list)

    estimated_capacity: int = 0

    current_length: int = 0


@dataclass(slots=True)
class ResumeLayoutMap:

    sections: list[SectionLayout] = field(default_factory=list)