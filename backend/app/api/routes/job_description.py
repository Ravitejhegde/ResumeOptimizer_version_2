from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(
    prefix="/job-descriptions",
    tags=["Job Descriptions"],
)