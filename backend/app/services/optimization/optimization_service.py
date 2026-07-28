from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from app.database.repositories.resume_repository import (
    ResumeRepository,
)

from app.engine.orchestrator import (
    ResumeOptimizationEngine,
)


class OptimizationService:
    """
    Coordinates resume optimization.

    Responsibilities
    ----------------
    • Load resume
    • Execute optimization engine
    • Return output path
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self._repository = ResumeRepository(db)

        self._engine = ResumeOptimizationEngine()

    def optimize(
        self,
        resume_id: str,
        job_description: str,
        selected_skills: list[str],
    ) -> str:

        resume = self._repository.get(
            resume_id
        )

        if resume is None:

            raise FileNotFoundError(
                "Resume not found."
            )

        output_file = (
            Path(resume.file_path)
            .with_stem(
                Path(resume.file_path).stem
                + "_optimized"
            )
        )

        self._engine.optimize(
            input_docx=resume.file_path,
            output_docx=str(output_file),
            selected_skills=selected_skills,
        )

        return str(output_file)