from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SectionRewrite:
    """
    Represents AI optimized content for one resume section.

    Used for:

        - Experience bullets
        - Project descriptions
        - Education entries
        - Other structured sections


    Flow:

        AI Response JSON
              |
              v
        SectionRewrite
              |
              v
        Writer Mapping
              |
              v
        DOCX Update


    Responsibilities:

        - Store rewritten section content.
        - Preserve original mapping information.
        - Carry AI optimization metadata.


    Does NOT:

        - Modify DOCX.
        - Validate AI output.
        - Generate content.
    """


    # --------------------------------------------------
    # Section identity
    # --------------------------------------------------

    section_type: str

    identifier: str | None = None


    # --------------------------------------------------
    # Original mapping
    # --------------------------------------------------

    original_text: str | None = None


    # --------------------------------------------------
    # Optimized content
    # --------------------------------------------------

    optimized_text: str = ""


    bullets: list[str] = field(
        default_factory=list,
    )


    # --------------------------------------------------
    # AI explanation
    # --------------------------------------------------

    reason: str | None = None


    confidence: float = 0.0


    # --------------------------------------------------
    # Preservation metadata
    # --------------------------------------------------

    preserve_formatting: bool = True

    preserve_length: bool = True


    original_length: int = 0

    optimized_length: int = 0


    # --------------------------------------------------
    # Dynamic metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def has_change(
        self,
    ) -> bool:
        """
        Check whether AI actually changed content.
        """

        if not self.original_text:

            return bool(
                self.optimized_text
            )


        return (
            self.original_text.strip()
            !=
            self.optimized_text.strip()
        )



    def word_growth_ratio(
        self,
    ) -> float:
        """
        Calculate content growth.

        Used later by AI response validator.
        """

        original_words = len(
            self.original_text.split()
        ) if self.original_text else 0


        optimized_words = len(
            self.optimized_text.split()
        )


        if original_words == 0:

            return 0.0


        return (
            optimized_words
            /
            original_words
        )



    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store additional AI information.
        """

        self.metadata[key] = value