from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.database.repositories.resume_repository import (
    ResumeRepository,
)

from app.engine.analyzer.document_analyzer import (
    DocumentAnalyzer,
)

from app.engine.analyzer.analyzers.job_description_analyzer import (
    JobDescriptionAnalyzer,
)

from app.engine.analyzer.comparators.skill_comparator import (
    SkillComparator,
)

from app.engine.models.analysis.jd_analysis import (
    JDAnalysis,
)

from app.engine.reader.parser import (
    DocumentParser,
)

from app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


logger = logging.getLogger(__name__)


class ResumeAnalysisService:
    """
    Resume analysis workflow.

    Pipeline:

        Resume
          |
          v
        Document Parser
          |
          v
        Document Analyzer
          |
          v
        JD Analyzer
          |
          v
        Skill Comparator
          |
          v
        Analysis Result
    """


    def __init__(
        self,
        db: Session,
        knowledge: KnowledgeManager,
    ) -> None:


        self._repository = ResumeRepository(
            db
        )

        self._knowledge = knowledge


        self._document_analyzer = DocumentAnalyzer(
            self._knowledge
        )


        self._jd_analyzer = JobDescriptionAnalyzer(
            self._knowledge
        )


        self._skill_comparator = SkillComparator(
            self._knowledge
        )


    def analyze(
        self,
        resume_id: str,
        job_description: str | None = None,
    ) -> dict[str, object]:

        logger.info(
            "Starting analysis for resume %s",
            resume_id,
        )


        resume = self._repository.get(
            resume_id
        )


        if resume is None:

            raise ResourceNotFoundError(
    "Resume not found."
)


        document = DocumentParser.parse(
            resume.file_path
        )


        logger.info(
            "Document parsed successfully"
        )


        analysis = (
            self._document_analyzer.analyze(
                document
            )
        )


        resume_keywords = (
            analysis.keywords
        )


        jd_analysis = JDAnalysis()


        if job_description:

            jd_analysis = (
                self._jd_analyzer.analyze(
                    job_description
                )
            )


        comparison = (
            self._skill_comparator.compare(
                resume_keywords,
                jd_analysis,
            )
        )


        logger.info(
            "Skill comparison completed"
        )


        return {

            "score": comparison.score,

            "matched_skills": comparison.matched,

            "missing_skills": comparison.missing,

            "extra_skills": comparison.extra,

            "detected_role": jd_analysis.role,

            "experience": (
                jd_analysis.minimum_experience
            ),

        }