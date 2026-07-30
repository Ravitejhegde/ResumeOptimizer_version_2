from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.engine.ai.models.section_rewrite import (
    SectionRewrite,
)


@dataclass(slots=True)
class AIOptimizationResponse:
    """
    Structured output returned by AI.

    Architecture:

        OpenRouter
             |
             v
    AIOptimizationResponse
             |
             v
    AIResponseMapper
             |
             v
    RewriteResult[]
             |
             v
           Writer


    Represents the complete optimized resume
    generated in ONE AI call.


    Does NOT:

        - Validate AI quality.
        - Modify DOCX.
        - Call AI.
    """



    # ==================================================
    # Candidate Information
    # ==================================================

    title: str | None = None


    summary: str | None = None



    # ==================================================
    # Paragraph Level Optimization
    # ==================================================

    paragraphs: list[SectionRewrite] = field(
        default_factory=list,
    )



    # ==================================================
    # Optimized Skills
    # ==================================================

    skills: dict[str, list[str]] = field(
        default_factory=dict,
    )



    # ==================================================
    # AI Metadata
    # ==================================================

    optimization_notes: list[str] = field(
        default_factory=list,
    )


    confidence: float = 0.0



    # ==================================================
    # Safety Tracking
    # ==================================================

    preserved_fields: list[str] = field(
        default_factory=list,
    )


    warnings: list[str] = field(
        default_factory=list,
    )



    # ==================================================
    # Raw AI Backup
    # ==================================================

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )



    # ==================================================
    # Helpers
    # ==================================================

    def has_changes(
        self,
    ) -> bool:
        """
        Check whether AI generated
        usable optimization output.
        """


        return any(

            [

                bool(self.title),

                bool(self.summary),

                bool(self.paragraphs),

                bool(self.skills),

            ]

        )



    def paragraph_count(
        self,
    ) -> int:
        """
        Return optimized paragraph count.
        """

        return len(
            self.paragraphs
        )



    def add_warning(
        self,
        message: str,
    ) -> None:
        """
        Add validation warning.
        """

        self.warnings.append(
            message
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