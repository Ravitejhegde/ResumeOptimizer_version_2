from dataclasses import dataclass, field


@dataclass
class Approval:

    approved: bool = True

    retry: bool = False

    auto_fixed: bool = False

    errors: list[str] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )