from __future__ import annotations

from pydantic import BaseModel


class GuestOptimizationRequest(BaseModel):
    session_token: str
    resume_id: str
    job_description: str


class GuestOptimizationResponse(BaseModel):
    success: bool
    message: str
    output_path: str = ""