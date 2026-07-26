from __future__ import annotations

from dataclasses import dataclass

from app.engine.models.paragraph import Paragraph


@dataclass(slots=True, frozen=True)
class ChangeDecision:
    """
    Represents whether a paragraph can be modified.
    """

    paragraph_id: str

    editable: bool

    reason: str | None = None


class ChangeDetector:
    """
    Determines whether each paragraph is eligible
    for optimization.

    This class never changes content.
    """

    PROTECTED_SECTIONS = {

        "education",

        "certifications",

    }

    @classmethod
    def analyze(
        cls,
        paragraph: Paragraph,
    ) -> ChangeDecision:

        if not paragraph.editable:

            return ChangeDecision(

                paragraph_id=paragraph.id,

                editable=False,

                reason="Paragraph is locked.",

            )

        if paragraph.section in cls.PROTECTED_SECTIONS:

            return ChangeDecision(

                paragraph_id=paragraph.id,

                editable=False,

                reason="Protected section.",

            )

        if not paragraph.text.strip():

            return ChangeDecision(

                paragraph_id=paragraph.id,

                editable=False,

                reason="Empty paragraph.",

            )

        return ChangeDecision(

            paragraph_id=paragraph.id,

            editable=True,

            reason=None,

        )