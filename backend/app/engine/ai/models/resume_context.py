from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ResumeContext:
    """
    Structured resume information sent to AI.

    Represents the candidate's existing resume
    in an AI-friendly format.

    Responsibilities:

        - Carry resume content safely.
        - Preserve original document information.
        - Provide structured sections for AI optimization.


    Does NOT:

        - Rewrite content.
        - Modify DOCX.
        - Call AI.
    """


    # --------------------------------------------------
    # Candidate identity (protected)
    # --------------------------------------------------

    name: str | None = None

    email: str | None = None

    phone: str | None = None

    location: str | None = None

    links: list[str] = field(
        default_factory=list,
    )


    # --------------------------------------------------
    # Professional information
    # --------------------------------------------------

    title: str | None = None

    summary: str | None = None


    # --------------------------------------------------
    # Resume sections
    # --------------------------------------------------

    experience: list[dict[str, Any]] = field(
        default_factory=list,
    )


    projects: list[dict[str, Any]] = field(
        default_factory=list,
    )


    education: list[dict[str, Any]] = field(
        default_factory=list,
    )


    skills: dict[str, list[str]] = field(
        default_factory=dict,
    )


    # --------------------------------------------------
    # Document preservation data
    # --------------------------------------------------

    paragraph_count: int = 0

    bullet_count: int = 0

    original_sections: list[str] = field(
        default_factory=list,
    )


    # --------------------------------------------------
    # Additional extracted information
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def protected_fields(
        self,
    ) -> dict[str, Any]:
        """
        Fields AI must never change.
        """

        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "links": self.links,
        }



    def section_count(
        self,
    ) -> int:
        """
        Number of resume sections.
        """

        return len(
            self.original_sections
        )



    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store additional extracted data.
        """

        self.metadata[key] = value