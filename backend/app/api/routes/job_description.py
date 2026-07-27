from fastapi import APIRouter

from app.schemas.job_description import JobDescriptionRequest
from app.services.job_description.analyzer import JobDescriptionAnalyzer

router = APIRouter(
    prefix="/job-description",
    tags=["Job Description"],
)


@router.post("/analyze")
async def analyze(
    request: JobDescriptionRequest,
):

    return JobDescriptionAnalyzer.analyze(
        request.job_description
    )




