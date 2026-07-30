from __future__ import annotations

import logging

from fastapi import (
    APIRouter,
    HTTPException,
)

from app.schemas.job_description import (
    JobDescriptionRequest,
)

from app.services.job_description.job_description_service import (
    JobDescriptionService,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/job-description",
    tags=["Job Description"],
)


@router.post("/analyze")
def analyze(
    request: JobDescriptionRequest,
):
    """
    Analyze a job description.
    """

    service = JobDescriptionService()

    try:

        return service.analyze(
            request.job_description
        )

    except Exception:

        logger.exception(
            "Job description analysis failed"
        )

        raise HTTPException(
            status_code=500,
            detail="Job description analysis failed.",
        )