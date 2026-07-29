from __future__ import annotations

import logging

from sqlalchemy.orm import Session

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

    # --------------------------------------------------

    def analyze(
        self,
        resume_id: str,
        job_description: str | None = None,
    ) -> dict:

        # ----------------------------------
        # Load Resume
        # ----------------------------------

        resume = self._repository.get(
            resume_id,
        )

        print("STEP 1 - Resume loaded")

        if resume is None:
            raise FileNotFoundError(
                "Resume not found.",
            )

        # ----------------------------------
        # Parse Resume
        # ----------------------------------

        document = DocumentParser.parse(
            resume.file_path,
        )

        print("STEP 2 - Document parsed")

        # ----------------------------------
        # Analyze Resume
        # ----------------------------------

        analysis = DocumentAnalyzer(
            self._knowledge,
        ).analyze(
            document,
        )

        print("STEP 3 - Resume analyzed")

        resume_skills = (
            analysis.keywords.normalized
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

        jd_analysis = JDAnalysis()

        if job_description:

            print("STEP 4 - JD analysis starting")

            jd_analysis = JobDescriptionAnalyzer(
                self._knowledge,
            ).analyze(
                job_description,
            )

            print("STEP 5 - JD analyzed")

            print("\n" + "=" * 80)
            print("JD SKILLS")
            print("=" * 80)
            print(
                jd_analysis.required_skills,
            )

        logger.info(
            "JD skills: %s",
            jd_analysis.required_skills,
        )

        # ----------------------------------
        # Compare Skills
        # ----------------------------------

        comparison = SkillComparator(
            self._knowledge,
        ).compare(
            analysis.keywords,
            jd_analysis,
        )

        print("STEP 6 - Comparison complete")

        print("\n" + "=" * 80)
        print("MATCHED")
        print(comparison.matched)

        print("\nMISSING")
        print(comparison.missing)

        print("\nEXTRA")
        print(comparison.extra)
        print("=" * 80)

        logger.info(
            "Matched: %s",
            comparison.matched,
        )

        logger.info(
            "Missing: %s",
            comparison.missing,
        )

        logger.info(
            "Extra: %s",
            comparison.extra,
        )

        # ----------------------------------
        # Response
        # ----------------------------------

        return {

            "score": comparison.score,

            "matched_skills": comparison.matched,

            "missing_skills": comparison.missing,

            "extra_skills": comparison.extra,

            "detected_role": jd_analysis.role,

            "experience": jd_analysis.minimum_experience,

        }