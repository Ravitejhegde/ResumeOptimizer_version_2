from __future__ import annotations

import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.analysis import (
    ResumeAnalysisRequest,
)

from app.application.models.optimization_request import (
    OptimizationRequest,
)

from app.application.services.resume_optimization_service import (
    ResumeOptimizationService,
)

from app.services.resume.resume_service import (
    ResumeService,
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
    Analyze an uploaded resume against a job description.

    The client provides only the resume ID.
    The stored resume path is resolved internally.
    """

    try:
        # -------------------------------------------------
        # Resolve uploaded resume
        # -------------------------------------------------

        resume_service = ResumeService(db)

        resume = resume_service.get_resume(
            request.resume_id
        )

        if resume is None:
            raise HTTPException(
                status_code=404,
                detail="Resume not found.",
            )

        # -------------------------------------------------
        # Resolve physical resume path internally
        # -------------------------------------------------

        resume_path = resume.file_path

        # -------------------------------------------------
        # Build optimization request
        # -------------------------------------------------

        optimization_request = OptimizationRequest(
            resume_path=resume_path,
            job_description=request.job_description,
            output_path="",
        )

        # -------------------------------------------------
        # Execute optimization workflow
        # -------------------------------------------------

        service = ResumeOptimizationService()

        return service.optimize(
            optimization_request
        )

    except HTTPException:
        raise

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception:

        logger.exception(
            "Resume analysis failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed.",
        )