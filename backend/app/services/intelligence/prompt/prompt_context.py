from dataclasses import dataclass, field

from app.services.intelligence.models import (
    OptimizationPlan,
)


@dataclass
class PromptContext:
    """
    Context passed to PromptBuilder.
    """

    plan: OptimizationPlan

    blocks: list[dict] = field(default_factory=list)

    keep: list[str] = field(default_factory=list)

    remove: list[str] = field(default_factory=list)

    add: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    formatting_rules: str = ""

    job_description: str = ""

    system_rules: str = ""