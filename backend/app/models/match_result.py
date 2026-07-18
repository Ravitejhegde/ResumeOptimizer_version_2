from dataclasses import dataclass, field


@dataclass
class MatchResult:

    score: int = 0

    matched_skills: list[str] = field(default_factory=list)

    missing_skills: list[str] = field(default_factory=list)

    extra_skills: list[str] = field(default_factory=list)