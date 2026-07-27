from __future__ import annotations

from dataclasses import dataclass, field

from app.engine.intelligence.promotion_engine import (
    PromotionDecision,
)
from app.engine.models.document import (
    Document,
)


@dataclass(slots=True, frozen=True)
class ParagraphAssignment:
    """
    A technology assigned to a paragraph.
    """

    technology: str

    paragraph_id: str

    section: str

    action: str


class ParagraphAssignmentEngine:
    """
    Decides where promoted technologies
    should appear.

    AI follows these assignments instead
    of deciding placement itself.
    """

    SECTION_PRIORITY = {

        "summary": 1,

        "experience": 2,

        "projects": 3,

        "skills": 4,

    }

    def assign(
        self,
        document: Document,
        decisions: list[PromotionDecision],
    ) -> list[ParagraphAssignment]:

        assignments: list[
            ParagraphAssignment
        ] = []

        section_lookup: dict[
            str,
            list[str],
        ] = {}

        for paragraph in document.paragraphs:

            section = (
                paragraph.section or ""
            ).lower()

            section_lookup.setdefault(
                section,
                []
            ).append(
                paragraph.id
            )

        for decision in decisions:

            if decision.action == "ignore":
                continue

            paragraph_id = ""

            section = "skills"

            if decision.category == "Backend":

                section = "experience"

            elif decision.category == "Frontend":

                section = "projects"

            elif decision.category == "Database":

                section = "experience"

            elif decision.category == "Cloud & DevOps":

                section = "projects"

            elif decision.category == "AI/ML":

                section = "projects"

            elif decision.category == "Testing":

                section = "experience"

            elif decision.category == "Tools":

                section = "skills"

            candidates = section_lookup.get(
                section,
                []
            )

            if candidates:

                paragraph_id = candidates[0]

            elif document.paragraphs:

                paragraph_id = (
                    document.paragraphs[0].id
                )

            assignments.append(

                ParagraphAssignment(

                    technology=decision.technology,

                    paragraph_id=paragraph_id,

                    section=section,

                    action=decision.action,

                )

            )

        return assignments