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

from app.schemas.match import (
    MatchResponse,
)

from app.services.resume.resume_service import (
    ResumeService,
)

from app.analyzer.document.document_analyzer import (
    DocumentAnalyzer,
)

from app.analyzer.document.section_analyzer import (
    SectionAnalyzer,
)

from app.job_description.services.job_description_parser import (
    JobDescriptionParser,
)

from app.understanding.services.resume_understanding_service import (
    ResumeUnderstandingService,
)

from app.job_understanding.services.job_understanding_service import (
    JobUnderstandingService,
)

from app.gap_analysis.services.gap_analysis_service import (
    GapAnalysisService,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post(
    "/match",
    response_model=MatchResponse,
)
def match_resume(
    request: ResumeAnalysisRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze an uploaded resume against a job description.
    """

    try:
        # ----------------------------------
        # 1. Resolve uploaded resume
        # ----------------------------------

        resume_service = ResumeService(db)

        resume = resume_service.get_resume(
            request.resume_id
        )

        if resume is None:
            raise HTTPException(
                status_code=404,
                detail="Resume not found.",
            )

        resume_path = resume.file_path

        # ----------------------------------
        # 2. Analyze resume document
        # ----------------------------------

        document = DocumentAnalyzer().analyze(
            resume_path
        )

        document = SectionAnalyzer().analyze(
            document
        )

        # ----------------------------------
        # 3. Understand resume
        # ----------------------------------

        resume_understanding = (
            ResumeUnderstandingService().understand(
                document
            )
        )

        # ----------------------------------
        # 4. Parse job description
        # ----------------------------------

        if not request.job_description:
            raise HTTPException(
                status_code=400,
                detail="Job description is required for match analysis.",
            )

        job_description = (
            JobDescriptionParser().parse(
                request.job_description
            )
        )

        # ----------------------------------
        # 5. Understand job
        # ----------------------------------

        job_understanding = (
            JobUnderstandingService().understand(
                job_description
            )
        )

        # ----------------------------------
        # 6. Gap analysis
        # ----------------------------------

        gap = GapAnalysisService().analyze(
            resume=resume_understanding,
            job=job_understanding,
        )

        # ----------------------------------
        # 7. Return match result
        # ----------------------------------

        return MatchResponse(
            score=round(
                gap.overall_match * 100
            ),
            matched_skills=gap.matched_skills,
            missing_skills=gap.missing_skills,
            extra_skills=[],
        )

    except HTTPException:
        raise

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception(
            "Resume analysis failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed.",
        ) from exc