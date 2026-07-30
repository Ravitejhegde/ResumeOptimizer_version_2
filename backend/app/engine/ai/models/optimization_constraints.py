from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class OptimizationConstraints:
    """
    Rules and safety boundaries given to AI.

    These constraints control AI behavior.

    Responsibilities:

        - Protect resume identity.
        - Preserve document structure.
        - Control rewrite boundaries.
        - Provide AI instructions.


    Does NOT:

        - Validate AI response.
        - Modify DOCX.
        - Call AI.
    """


    # --------------------------------------------------
    # Identity protection
    # --------------------------------------------------

    preserve_identity: bool = True

    protected_fields: list[str] = field(
        default_factory=lambda: [
            "name",
            "email",
            "phone",
            "location",
            "links",
        ],
    )


    # --------------------------------------------------
    # Document preservation
    # --------------------------------------------------

    preserve_formatting: bool = True

    preserve_section_order: bool = True

    preserve_paragraph_count: bool = True

    preserve_bullet_count: bool = True


    # --------------------------------------------------
    # Content boundaries
    # --------------------------------------------------

    allow_title_change: bool = True

    allow_summary_rewrite: bool = True

    allow_project_rewrite: bool = True

    allow_skill_reorganization: bool = True


    # --------------------------------------------------
    # AI safety rules
    # --------------------------------------------------

    prevent_fake_experience: bool = True

    prevent_skill_invention: bool = True

    use_only_supported_technologies: bool = True


    # --------------------------------------------------
    # Length control
    # --------------------------------------------------

    max_content_growth_ratio: float = 1.35

    max_sentence_growth_ratio: float = 1.50

    preserve_line_budget: bool = True


    # --------------------------------------------------
    # Output requirements
    # --------------------------------------------------

    output_format: str = "json"

    require_structured_response: bool = True


    # --------------------------------------------------
    # Extensible rules
    # --------------------------------------------------

    custom_rules: list[str] = field(
        default_factory=list,
    )


    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def add_rule(
        self,
        rule: str,
    ) -> None:
        """
        Add dynamic AI instruction.
        """

        self.custom_rules.append(
            rule
        )


    def to_instruction_list(
        self,
    ) -> list[str]:
        """
        Convert constraints into
        AI-readable instructions.
        """

        rules: list[str] = []


        if self.preserve_identity:

            rules.append(
                "Never change candidate identity information."
            )


        if self.preserve_formatting:

            rules.append(
                "Preserve original document formatting."
            )


        if self.prevent_fake_experience:

            rules.append(
                "Never create false experience or unsupported claims."
            )


        if self.prevent_skill_invention:

            rules.append(
                "Only use verified skills from provided context."
            )


        rules.extend(
            self.custom_rules
        )


        return rules