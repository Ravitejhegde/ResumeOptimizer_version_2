from __future__ import annotations

import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database.session import (
    get_db,
)

from app.schemas.analysis import (
    ResumeAnalysisRequest,
)

from app.application.models.optimization_request import (
    OptimizationRequest,
)

from app.application.services.resume_optimization_service import (
    ResumeOptimizationService,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post("/match")
def match_resume(
    request: ResumeAnalysisRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze a resume using the new optimization workflow.

    NOTE:
    This endpoint is temporarily adapted during the
    migration from the old engine to the new engine.
    """

    try:

        # -------------------------------------------------
        # TODO:
        # Replace this with ResumeRepository once the
        # repository layer is migrated.
        # -------------------------------------------------

        resume_path = ""

        optimization_request = OptimizationRequest(
            resume_path=resume_path,
            job_description=request.job_description,
            output_path="",
        )

        service = ResumeOptimizationService()

        return service.optimize(
            optimization_request
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception:

        logger.exception(
            "Resume analysis failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed.",
        )