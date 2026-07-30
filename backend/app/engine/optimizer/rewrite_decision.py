from dataclasses import dataclass


@dataclass
class RewriteDecision:

    paragraph_id: str

    should_rewrite: bool

    reason: str

    technologies: list[str]