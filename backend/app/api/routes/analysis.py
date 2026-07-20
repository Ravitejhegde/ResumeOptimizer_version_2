from fastapi import APIRouter, HTTPException

from app.schemas.analysis import ResumeAnalysisRequest
from app.schemas.match import MatchResponse

from app.services.analysis.analysis_service import (
    ResumeAnalysisService,
)

router = APIRouter(
    prefix="/analysis",
    
    tags=["Analysis"],
)


@router.post(
    "/match",
    response_model=MatchResponse,
)
async def match_resume(
    request: ResumeAnalysisRequest,
):

    try:

        return ResumeAnalysisService.analyze(

            request.resume_id,

            request.job_description,

        )

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )