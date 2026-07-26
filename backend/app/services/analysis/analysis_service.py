from __future__ import annotations

from app.database.session import SessionLocal
from app.database.repositories.resume_repository import (
    ResumeRepository,
)

from app.engine.analyzer.document_analyzer import (
    DocumentAnalyzer,
)
from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.reader.parser import (
    DocumentParser,
)


class ResumeAnalysisService:
    """
    Analysis service powered by the new V3 engine.

    Responsibilities
    ----------------
    - Load resume
    - Parse document
    - Analyze document
    - Return analysis result

    This service NEVER performs optimization.
    """

    @staticmethod
    def analyze(
        resume_id: str,
        job_description: str | None = None,
    ):

        db = SessionLocal()

        try:

            repository = ResumeRepository(db)

            resume = repository.get(resume_id)

            if resume is None:
                raise FileNotFoundError(
                    "Resume not found."
                )

            # Parse DOCX using the new engine
            document = DocumentParser.parse(
                resume.file_path
            )

            # Initialize knowledge
            knowledge = KnowledgeBase()

            knowledge.initialize()

            # Analyze document
            analyzer = DocumentAnalyzer(
                knowledge
            )

            analysis = analyzer.analyze(
                document
            )

            return analysis

        finally:

            db.close()