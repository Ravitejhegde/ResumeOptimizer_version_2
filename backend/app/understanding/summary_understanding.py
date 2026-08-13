"""
app.understanding.summary_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builds a high-level summary of the resume.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class SummaryUnderstanding:
    """
    Builds the resume summary.
    """

    def analyze(
        self,
        document: DocumentModel,
        understanding: ResumeUnderstanding,
    ) -> ResumeUnderstanding:

        understanding.summary = (
            f"{understanding.primary_role} "
            f"with {len(document.skills)} skills "
            f"and {len(document.technologies)} technologies."
        )

        return understanding