from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import traceback
from app.database.session import get_db

from app.services.optimization.optimization_service import (
    OptimizationService,
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

    service = OptimizationService(db)

    try:

        output_file = service.optimize(
            resume_id=request.resume_id,
            job_description=request.job_description,
            selected_skills=request.selected_skills,
        )

        return {
            "success": True,
            "output_file": output_file,
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
