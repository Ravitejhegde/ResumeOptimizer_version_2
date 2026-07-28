from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

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

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post("/match")
async def match_resume(
    request: ResumeAnalysisRequest,
    db: Session = Depends(get_db),
):

    service = ResumeAnalysisService(
        db,
    )

    try:

        return service.analyze(
            resume_id=request.resume_id,
            job_description=request.job_description,
        )

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )