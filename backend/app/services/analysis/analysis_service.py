from app.database.session import SessionLocal
from app.database.repositories.resume_repository import ResumeRepository

from app.services.resume.extractor import ResumeExtractor
from app.services.resume.profile_builder import ResumeProfileBuilder
from app.services.job_description.analyzer import JobDescriptionAnalyzer
from app.services.matching.matcher import ResumeMatcher


class ResumeAnalysisService:

    @staticmethod
    def analyze(
        resume_id: str,
        job_description: str,
    ):

        db = SessionLocal()

        try:

            repository = ResumeRepository(db)

            resume = repository.get(resume_id)

            if resume is None:

                raise FileNotFoundError(
                    "Resume not found."
                )

            resume_text = ResumeExtractor.extract(
                resume.file_path
            )

            resume_profile = ResumeProfileBuilder.build(
                resume_text
            )

            job_profile = JobDescriptionAnalyzer.analyze(
                job_description
            )

            return ResumeMatcher.match(
                resume_profile,
                job_profile,
            )

        finally:

            db.close()