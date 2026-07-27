from dataclasses import dataclass, field


@dataclass
class JobProfile:

    title: str = ""

    experience: str = ""

    skills: list[str] = field(default_factory=list)




