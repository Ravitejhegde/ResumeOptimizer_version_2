"""
app.analyzer.models.section_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents a resume section.

Examples
--------
Summary
Experience
Projects
Skills
Education
Certifications
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SectionModel:
    """
    Represents one logical section of a resume.
    """

    name: str

    paragraphs: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        """
        Complete section text.
        """
        return "\n".join(self.paragraphs)

    @property
    def is_empty(self) -> bool:
        """
        True if the section contains no text.
        """
        return not self.paragraphs

    @property
    def paragraph_count(self) -> int:
        """
        Number of paragraphs.
        """
        return len(self.paragraphs)