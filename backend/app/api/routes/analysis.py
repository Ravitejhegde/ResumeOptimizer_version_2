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


from app.services.analysis.analysis_service import (
    ResumeAnalysisService,
)


from app.knowledge.knowledge_manager import (
    KnowledgeManager,
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
    Analyze uploaded resume against job description.

    Flow:

        API
          |
          v
        ResumeAnalysisService
          |
          v
        DocumentParser
          |
          v
        DocumentAnalyzer
          |
          v
        SkillComparator
    """


    try:

        # ----------------------------------
        # Knowledge dependency
        # ----------------------------------

        knowledge = KnowledgeManager()

        knowledge.initialize()


        # ----------------------------------
        # Service
        # ----------------------------------

        service = ResumeAnalysisService(
            db=db,
            knowledge=knowledge,
        )


        # ----------------------------------
        # Execute analysis
        # ----------------------------------

        return service.analyze(

            resume_id=request.resume_id,

            job_description=request.job_description,

        )


    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


    except Exception:

        logger.exception(
            "Resume analysis failed"
        )


        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed.",
        )