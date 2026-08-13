from __future__ import annotations

import logging
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.current_user import (
    get_current_user,
)
from app.application.models.optimization_request import (
    OptimizationRequest,
)
from app.application.services.resume_optimization_service import (
    ResumeOptimizationService,
)
from app.database.models.user import User
from app.database.repositories.resume_repository import (
    ResumeRepository,
)
from app.database.session import get_db
from app.schemas.optimize_request import (
    OptimizeRequest,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/optimization",
    tags=["Optimization"],
)


@router.post(
    "/optimize",
    status_code=status.HTTP_200_OK,
)
def optimize_resume(
    request: OptimizeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Optimize an uploaded resume for a target job description.

    The client provides a resume ID rather than a filesystem path.

    The server:
        1. Finds the resume.
        2. Verifies ownership.
        3. Resolves the stored file path.
        4. Executes the optimization workflow.
    """

    # ======================================================
    # Find Resume
    # ======================================================

    resumes = ResumeRepository(db)

    resume = resumes.get(
        request.resume_id,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    # ======================================================
    # Ownership
    # ======================================================

    if resume.workspace.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this resume.",
        )

    # ======================================================
    # Verify Physical File
    # ======================================================

    resume_path = Path(
        resume.file_path,
    )

    if not resume_path.exists():
        logger.error(
            "Resume file missing: resume_id=%s path=%s",
            resume.id,
            resume_path,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file is no longer available.",
        )

    # ======================================================
    # Output Path
    # ======================================================

    output_path = (
        resume_path.parent
        / f"{resume_path.stem}_optimized.docx"
    )

    # ======================================================
    # Application Request
    # ======================================================

    optimization_request = OptimizationRequest(
        resume_path=str(resume_path),
        job_description=request.job_description,
        output_path=str(output_path),
    )

    # ======================================================
    # Execute Workflow
    # ======================================================

    try:

        service = ResumeOptimizationService()

        response = service.optimize(
            optimization_request,
        )

        return response

    except FileNotFoundError as exc:

        logger.exception(
            "Resume file not found during optimization: %s",
            resume.id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file could not be found.",
        ) from exc

    except ValueError as exc:

        logger.exception(
            "Invalid optimization request: resume_id=%s",
            resume.id,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        logger.exception(
            "Resume optimization failed: resume_id=%s",
            resume.id,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resume optimization failed.",
        ) from exc