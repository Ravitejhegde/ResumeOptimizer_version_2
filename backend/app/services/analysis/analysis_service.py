from __future__ import annotations

from app.database.repositories.resume_repository import (
    ResumeRepository,
)
from app.database.session import (
    SessionLocal,
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
from app.engine.knowledge.knowledge_base import (
    KnowledgeBase,
)
from app.engine.reader.parser import (
    DocumentParser,
)


class ResumeAnalysisService:
    """
    Resume Analysis Service.

    Responsibilities
    ----------------
    • Load resume
    • Analyze resume
    • Analyze job description
    • Compare skills
    • Return frontend response
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

            # ----------------------------------
            # Parse Resume
            # ----------------------------------

            document = DocumentParser.parse(
                resume.file_path
            )

            # ----------------------------------
            # Initialize Knowledge
            # ----------------------------------

            knowledge = KnowledgeBase()
            knowledge.initialize()

            # ----------------------------------
            # Analyze Resume
            # ----------------------------------

            document_analyzer = (
                DocumentAnalyzer(
                    knowledge
                )
            )

            analysis = (
                document_analyzer.analyze(
                    document
                )
            )

            resume_skills = (
                analysis.keywords.normalized_skills
            )

            print("\n" + "=" * 80)
            print("RESUME SKILLS")
            print("=" * 80)
            print(resume_skills)
            print("=" * 80)

            # ----------------------------------
            # Analyze Job Description
            # ----------------------------------

            jd_analysis = None
            jd_skills: list[str] = []

            if job_description:

                jd_analyzer = (
                    JobDescriptionAnalyzer(
                        knowledge
                    )
                )

                jd_analysis = (
                    jd_analyzer.analyze(
                        job_description
                    )
                )

                jd_skills = (
                    jd_analysis.required_skills
                )

            print("\n" + "=" * 80)
            print("JD SKILLS")
            print("=" * 80)
            print(jd_skills)
            print("=" * 80)

            # ----------------------------------
            # Compare Skills
            # ----------------------------------

            comparison = (
                SkillComparator.compare(
                    resume_skills=resume_skills,
                    jd_skills=jd_skills,
                )
            )

            print("\n" + "=" * 80)
            print("MATCHED SKILLS")
            print("=" * 80)
            print(comparison.matched_skills)

            print("\n" + "=" * 80)
            print("MISSING SKILLS")
            print("=" * 80)
            print(comparison.missing_skills)

            print("\n" + "=" * 80)
            print("EXTRA SKILLS")
            print("=" * 80)
            print(comparison.extra_skills)
            print("=" * 80)

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

                # Placeholder until Role Analyzer
                # and Experience Analyzer are built.
                "detected_role": "",

                "experience": 0,

            }

        finally:

            db.close()