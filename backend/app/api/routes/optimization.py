from pathlib import Path
import traceback

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.repositories.resume_repository import ResumeRepository
from app.services.optimization.optimization_pipeline import (
    OptimizationPipeline,
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

    repository = ResumeRepository(db)

    resume = repository.get(request.resume_id)

    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    resume_path = Path(resume.file_path)

    if not resume_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Resume file not found."
        )

    try:

        pipeline = OptimizationPipeline()

        result = pipeline.optimize(

            resume_path=str(resume_path),

            job_description=request.job_description,

            selected_skills=request.selected_skills,

        )

        return {

            "success": True,

            "optimized_filename": result.get(
                "optimized_filename"
            ),

            "blocks": result.get(
                "blocks",
                []
            ),

            "layout": result.get(
                "layout",
                {}
            )

        }

    except Exception:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Resume optimization failed."
        )