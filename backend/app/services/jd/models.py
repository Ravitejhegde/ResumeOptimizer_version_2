from dataclasses import dataclass, field


@dataclass
class JDKnowledge:

    title: str = ""

    required_skills: set[str] = field(default_factory=set)

    preferred_skills: set[str] = field(default_factory=set)

    soft_skills: set[str] = field(default_factory=set)

    responsibilities: list[str] = field(default_factory=list)