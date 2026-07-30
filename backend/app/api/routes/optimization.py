from __future__ import annotations

import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from pydantic import BaseModel, Field

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.services.optimization.optimization_service import (
    OptimizationService,
)

from app.engine.orchestrator import (
    ResumeOptimizationEngine,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/optimization",
    tags=["Optimization"],
)



# --------------------------------------------------
# Engine instance
# --------------------------------------------------

engine = ResumeOptimizationEngine()



# --------------------------------------------------
# Request Model
# --------------------------------------------------

class OptimizeRequest(BaseModel):
    """
    Resume optimization request.
    """

    resume_id: str

    job_description: str

    selected_skills: list[str] = Field(
        default_factory=list,
    )



# --------------------------------------------------
# API
# --------------------------------------------------

@router.post("/optimize")
async def optimize_resume(
    request: OptimizeRequest,
    db: Session = Depends(get_db),
):
    """
    Optimize existing resume.

    Async pipeline:

        API
         |
         v
        Service
         |
         v
        ResumeOptimizationEngine
         |
         v
        OptimizerEngine
         |
         v
        AI/OpenRouter
         |
         v
        Writer
    """



    service = OptimizationService(
        db=db,
        engine=engine,
    )



    try:

        generated_resume = await service.optimize(

            resume_id=request.resume_id,

            job_description=request.job_description,

            selected_skills=request.selected_skills,

        )



        return {

            "success": True,

            "resume_id": generated_resume.id,

            "filename": generated_resume.filename,

            "file_path": generated_resume.file_path,

        }



    except FileNotFoundError as exc:


        logger.warning(

            "Resume file not found: %s",

            exc,

        )


        raise HTTPException(

            status_code=404,

            detail=str(exc),

        )



    except Exception as exc:


        logger.exception(

            "Resume optimization failed."

        )


        raise HTTPException(

            status_code=500,

            detail="Resume optimization failed.",

        ) from exc