"""
app.understanding.project.project_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines the strongest project.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class ProjectUnderstanding:
    """
    Determines project-related understanding.
    """

    def analyze(
        self,
        document: DocumentModel,
        understanding: ResumeUnderstanding,
    ) -> ResumeUnderstanding:

        if not document.projects:
            return understanding

        # MVP:
        # Assume the first parsed project is the strongest.
        strongest = document.projects[0]

        understanding.strongest_project = (
            strongest.name
        )

        return understanding