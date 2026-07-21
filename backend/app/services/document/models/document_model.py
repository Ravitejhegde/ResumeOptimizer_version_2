from dataclasses import dataclass, field

from app.services.document.models.section_model import (
    SectionModel,
)


@dataclass
class DocumentModel:
    """
    Root representation of an entire DOCX document.
    """

    filename: str = ""

    title: str = ""

    author: str = ""

    company: str = ""

    subject: str = ""

    keywords: list[str] = field(
        default_factory=list
    )

    sections: list[SectionModel] = field(
        default_factory=list
    )

    page_count: int = 0

    version: int = 1