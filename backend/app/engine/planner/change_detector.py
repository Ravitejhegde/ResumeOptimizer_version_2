from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.paragraph import Paragraph


@dataclass(slots=True, frozen=True)
class ChangeDecision:
    """
    Planner decision for a paragraph.

    This is the single source of truth for whether
    a paragraph may be optimized.
    """

    paragraph_id: str

    editable: bool

    should_rewrite: bool

    reason: str | None = None


class ChangeDetector:
    """
    Determines which paragraphs should be sent
    to the AI.

    This class NEVER rewrites text.
    It only produces decisions.
    """

    PROTECTED_SECTIONS = {
        "education",
        "contact",
        "header",
        "heading",
        "title",
        "certifications",
    }

    @classmethod
    def analyze(
        cls,
        paragraph: Paragraph,
    ) -> ChangeDecision:

        text = paragraph.text.strip()

        if not paragraph.editable:

            return ChangeDecision(
                paragraph_id=paragraph.id,
                editable=False,
                should_rewrite=False,
                reason="Paragraph is locked.",
            )

        if not text:

            return ChangeDecision(
                paragraph_id=paragraph.id,
                editable=False,
                should_rewrite=False,
                reason="Empty paragraph.",
            )

        section = (
            paragraph.section or ""
        ).lower()

        if section in cls.PROTECTED_SECTIONS:

            return ChangeDecision(
                paragraph_id=paragraph.id,
                editable=True,
                should_rewrite=False,
                reason="Protected section.",
            )

        if len(text.split()) <= 2:

            return ChangeDecision(
                paragraph_id=paragraph.id,
                editable=True,
                should_rewrite=False,
                reason="Heading.",
            )

        return ChangeDecision(
            paragraph_id=paragraph.id,
            editable=True,
            should_rewrite=True,
            reason=None,
        )