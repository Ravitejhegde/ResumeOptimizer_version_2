from pathlib import Path
import traceback

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.repositories.resume_repository import (
    ResumeRepository,
)
from app.database.session import get_db

from app.engine.orchestrator import (
    ResumeOptimizationEngine,
)

router = APIRouter(
    prefix="/optimization",
    tags=["Optimization"],
)


class OptimizeRequest(BaseModel):
    resume_id: str
    job_description: str
    selected_skills: list[str] = []


@router.post("/optimize")
def optimize_resume(
    request: OptimizeRequest,
    db: Session = Depends(get_db),
):

    print("=" * 80)
    print("OPTIMIZATION REQUEST")
    print("=" * 80)
    print("Resume ID:", request.resume_id)
    print("Selected Skills:", request.selected_skills)
    print("=" * 80)

    repository = ResumeRepository(db)

    resume = repository.get(request.resume_id)

    if resume is None:

        print("❌ Resume not found in database.")

        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    print("✅ Resume found.")
    print("File Path:", resume.file_path)

    resume_path = Path(resume.file_path)

    if not resume_path.exists():

        print("❌ Resume file missing:", resume_path)

        raise HTTPException(
            status_code=404,
            detail="Resume file not found.",
        )

    try:

        engine = ResumeOptimizationEngine()

        output_path = (
            resume_path.parent
            / f"{resume_path.stem}_optimized.docx"
        )

        engine.optimize(
            input_docx=str(resume_path),
            output_docx=str(output_path),
            selected_skills=request.selected_skills,
        )

        return {
            "success": True,
            "optimized_filename": output_path.name,
            "output_path": str(output_path),
        }

    except Exception as exc:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )