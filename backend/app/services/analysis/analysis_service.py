from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.database.repositories.resume_repository import (
    ResumeRepository,
)
from app.engine.analyzer.document_analyzer import (
    DocumentAnalyzer,
)
from app.engine.analyzer.job_description_analyzer import (
    JobDescriptionAnalyzer,
)
from app.engine.analyzer.skill_comparator import (
    SkillComparator,
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
    Resume Analysis Service.

    Responsibilities
    ----------------
    • Load resume
    • Parse resume
    • Analyze resume
    • Analyze job description
    • Compare skills
    • Return analysis results
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self._repository = ResumeRepository(db)

        self._knowledge = KnowledgeManager()
        self._knowledge.initialize()

    def analyze(
        self,
        resume_id: str,
        job_description: str | None = None,
    ) -> dict:

        resume = self._repository.get(
            resume_id
        )

        if resume is None:

            raise FileNotFoundError(
                "Resume not found."
            )

        # ----------------------------------
        # Parse Resume
        # ----------------------------------

        document = DocumentParser.parse(
            resume.file_path
        )

        # ----------------------------------
        # Analyze Resume
        # ----------------------------------

        analysis = DocumentAnalyzer(
            self._knowledge
        ).analyze(
            document
        )

        resume_skills = (
            analysis.keywords.normalized_skills
        )
        print("\n" + "=" * 80)
        print("RESUME SKILLS")
        print("=" * 80)
        print(resume_skills)
        logger.info(
            "Resume skills: %s",
            resume_skills,
        )

        # ----------------------------------
        # Analyze Job Description
        # ----------------------------------

        jd_skills: list[str] = []

        if job_description:

            jd_analysis = JobDescriptionAnalyzer(
                self._knowledge
            ).analyze(
                job_description
            )

            jd_skills = (
                jd_analysis.required_skills
            )
            print("\n" + "=" * 80)
            print("JD SKILLS")
            print("=" * 80)
            print(jd_skills)
        logger.info(
            "JD skills: %s",
            jd_skills,
        )

        # ----------------------------------
        # Compare Skills
        # ----------------------------------

        comparison = SkillComparator.compare(
            resume_skills=resume_skills,
            jd_skills=jd_skills,
        )
        print("\n" + "=" * 80)
        print("MATCHED")
        print(comparison.matched_skills)

        print("\nMISSING")
        print(comparison.missing_skills)

        print("\nEXTRA")
        print(comparison.extra_skills)
        print("=" * 80)

        logger.info(
            "Matched: %s",
            comparison.matched_skills,
        )

        logger.info(
            "Missing: %s",
            comparison.missing_skills,
        )

        logger.info(
            "Extra: %s",
            comparison.extra_skills,
        )

        # ----------------------------------
        # Response
        # ----------------------------------
        
        return {

            "score": comparison.match_percentage,

            "matched_skills": (
                comparison.matched_skills
            ),

            "missing_skills": (
                comparison.missing_skills
            ),

            "extra_skills": (
                comparison.extra_skills
            ),

            "detected_role": "",

            "experience": 0,

        }