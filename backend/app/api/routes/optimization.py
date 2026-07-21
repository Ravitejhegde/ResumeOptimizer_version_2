from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import traceback

from app.services.optimization.optimization_pipeline import (
    OptimizationPipeline,
)

router = APIRouter(
    prefix="/optimization",
    tags=["Optimization"],
)


class OptimizeRequest(BaseModel):
    resume_filename: str
    job_description: str
    selected_skills: list[str] = []


@router.post("/optimize")
def optimize_resume(request: OptimizeRequest):

    resume_path = (
        f"storage/temp/{request.resume_filename}"
    )

    try:

        pipeline = OptimizationPipeline()

        result = pipeline.optimize(
            resume_path=resume_path,
            job_description=request.job_description,
            selected_skills=request.selected_skills,
        )

        return {
            "success": True,
            "data": result,
        }

    except Exception as e:

        traceback.print_exc()      # <-- IMPORTANT

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )