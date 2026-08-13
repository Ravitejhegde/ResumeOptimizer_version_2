"""
app.analyzer.project.project_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parses the Projects section into ProjectModel objects.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.analyzer.models.project_model import (
    ProjectModel,
)


class ProjectParser:
    """
    Parses resume projects.
    """

    def parse(
        self,
        document: DocumentModel,
    ) -> list[ProjectModel]:
        """
        Parse project entries from the resume.
        """

        projects: list[ProjectModel] = []

        section = document.sections.get(
            "projects"
        )

        if section is None:
            return projects

        project = ProjectModel(
            description=section.paragraphs.copy()
        )

        projects.append(project)

        return projects