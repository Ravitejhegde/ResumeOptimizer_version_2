from __future__ import annotations

from app.engine.models.document.document import (
    Document,
)
from app.engine.models.planner.section_plan import (
    SectionPlan,
)


class SectionExecutor:
    """
    Executes optimization for one section.
    """

    def execute(
        self,
        document: Document,
        plan: SectionPlan,
    ) -> list:

        paragraphs = []

        for paragraph in document.paragraphs:

            if paragraph.section == plan.section:

                paragraphs.append(
                    paragraph,
                )

        return paragraphs
