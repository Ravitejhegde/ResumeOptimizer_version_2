from __future__ import annotations

from app.database.repositories.resume_repository import (
    ResumeRepository,
)
from app.database.session import SessionLocal

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
    V3 Resume Analysis Service.

    Responsibilities
    ----------------
    - Load resume
    - Parse document
    - Run analysis
    - Return frontend-ready response

    Never performs optimization.
    """

    @staticmethod
    def analyze(
        resume_id: str,
        job_description: str | None = None,
    ):

        db = SessionLocal()

        try:

            repository = ResumeRepository(db)

            resume = repository.get(
                resume_id
            )

            if resume is None:
                raise FileNotFoundError(
                    "Resume not found."
                )

            document = DocumentParser.parse(
                resume.file_path
            )

            knowledge = KnowledgeBase()
            knowledge.initialize()

            analyzer = DocumentAnalyzer(
                knowledge
            )

            analysis = analyzer.analyze(
                document
            )

            return {

                "score": analysis.ats.score,

                "matched_skills": (
                    analysis.keywords.normalized_skills
                ),

                "missing_skills": [],

                "extra_skills": [],

            }

        finally:

            db.close()