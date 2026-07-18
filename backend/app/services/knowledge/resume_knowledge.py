from dataclasses import dataclass, field


@dataclass
class ResumeKnowledge:

    frontend: set[str] = field(default_factory=set)

    backend: set[str] = field(default_factory=set)

    database: set[str] = field(default_factory=set)

    programming_languages: set[str] = field(default_factory=set)

    cloud: set[str] = field(default_factory=set)

    devops: set[str] = field(default_factory=set)

    tools: set[str] = field(default_factory=set)

    frameworks: set[str] = field(default_factory=set)

    testing: set[str] = field(default_factory=set)

    mobile: set[str] = field(default_factory=set)

    other: set[str] = field(default_factory=set)