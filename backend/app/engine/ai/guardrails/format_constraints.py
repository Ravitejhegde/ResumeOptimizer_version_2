from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FormatConstraints:
    """
    Controls document structure preservation rules.

    These rules are sent to AI through PromptBuilder.

    Purpose:

        Prevent AI from changing:
            - Resume structure
            - Section order
            - Layout assumptions
            - Bullet structure


    Does NOT:

        - Modify DOCX.
        - Validate final DOCX.
        - Call AI.
    """


    # --------------------------------------------------
    # Document structure
    # --------------------------------------------------

    preserve_section_order: bool = True

    preserve_section_names: bool = True

    preserve_paragraph_count: bool = True

    preserve_bullet_count: bool = True



    # --------------------------------------------------
    # Content boundaries
    # --------------------------------------------------

    allow_merge_paragraphs: bool = False

    allow_split_paragraphs: bool = False

    allow_new_sections: bool = False



    # --------------------------------------------------
    # Formatting protection
    # --------------------------------------------------

    preserve_formatting: bool = True

    preserve_heading_styles: bool = True

    preserve_bullet_styles: bool = True

    preserve_spacing: bool = True



    # --------------------------------------------------
    # Layout safety
    # --------------------------------------------------

    preserve_line_budget: bool = True

    prevent_large_expansion: bool = True



    # --------------------------------------------------
    # Custom future rules
    # --------------------------------------------------

    additional_rules: list[str] = field(
        default_factory=list,
    )


    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def to_instructions(
        self,
    ) -> list[str]:
        """
        Convert formatting rules into
        AI-readable instructions.
        """

        rules: list[str] = []


        if self.preserve_section_order:

            rules.append(
                "Keep existing resume section order."
            )


        if self.preserve_paragraph_count:

            rules.append(
                "Do not increase or decrease paragraph count."
            )


        if self.preserve_bullet_count:

            rules.append(
                "Keep the same number of bullet points."
            )


        if self.preserve_formatting:

            rules.append(
                "Preserve original document formatting."
            )


        if self.preserve_heading_styles:

            rules.append(
                "Do not change heading structure."
            )


        if self.prevent_large_expansion:

            rules.append(
                "Avoid unnecessary content expansion."
            )


        if not self.allow_new_sections:

            rules.append(
                "Do not create new resume sections."
            )


        rules.extend(
            self.additional_rules
        )


        return rules



    def add_rule(
        self,
        rule: str,
    ) -> None:
        """
        Add dynamic formatting instruction.
        """

        self.additional_rules.append(
            rule
        )