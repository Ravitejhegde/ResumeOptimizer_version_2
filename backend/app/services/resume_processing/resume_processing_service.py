from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.database.models.resume import Resume
from app.database.repositories.resume_repository import ResumeRepository

from app.engine.models.document.document import Document
from app.engine.reader.parser import DocumentParser


logger = logging.getLogger(__name__)


class ResumeProcessingService:
    """
    Connects application layer with ResumeOptimizer engine.

    Responsibilities:
        - Load uploaded resume
        - Parse DOCX
        - Create document model

    Does not:
        - Analyze resume
        - Optimize resume
        - Write DOCX
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        self.resumes = ResumeRepository(
            db
        )


    def parse_resume(
        self,
        resume_id: str,
    ) -> Document:
        """
        Convert uploaded DOCX into engine Document model.
        """


        resume = self.resumes.get(
            resume_id
        )


        if resume is None:

            raise ValueError(
                "Resume not found."
            )


        logger.info(
            "Parsing resume: %s",
            resume.original_filename,
        )


        document = DocumentParser.parse(
            resume.file_path
        )


        logger.info(
            "Resume parsed successfully. paragraphs=%s tables=%s",
            len(document.paragraphs),
            len(document.tables),
        )


        return document