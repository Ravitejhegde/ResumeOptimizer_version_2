"""
app.understanding.skill.skill_understanding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines the primary skills of a resume.
"""

from __future__ import annotations

from app.analyzer.models.document_model import (
    DocumentModel,
)
from app.understanding.models.resume_understanding import (
    ResumeUnderstanding,
)


class SkillUnderstanding:
    """
    Determines skill-related understanding.
    """

    def analyze(
        self,
        document: DocumentModel,
        understanding: ResumeUnderstanding,
    ) -> ResumeUnderstanding:

        skills = sorted(
            (
                skill.name
                for skill in document.skills.values()
            ),
        )

        understanding.primary_skills = skills

        return understanding