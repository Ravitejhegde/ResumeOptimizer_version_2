"""
app.analyzer.project.project_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extracts projects from a resume.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.analyzer.project.project_parser import (
    ProjectParser,
)


class ProjectAnalyzer:
    """
    Populates document.projects.
    """

    def __init__(self) -> None:
        self._parser = ProjectParser()

    def analyze(
        self,
        document: DocumentModel,
    ) -> DocumentModel:
        """
        Extract project entries.
        """

        print(type(document))

        document.projects = self._parser.parse(
            document
        )

        return document