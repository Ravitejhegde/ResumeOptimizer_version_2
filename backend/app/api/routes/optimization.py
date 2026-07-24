from pathlib import Path
import traceback

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
def optimize_resume(
    request: OptimizeRequest,
):

    resume_path = (
        Path("storage/temp")
        / request.resume_filename
    )

    if not resume_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Resume file not found.",
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

            "message": "Resume optimized successfully.",

            "data": {

                "optimized_filename": result.get(
                    "optimized_filename"
                ),

                "blocks": result.get(
                    "blocks",
                    [],
                ),

                "layout": result.get(
                    "layout",
                    {},
                ),

            },

        }

    except Exception:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Resume optimization failed.",
        )