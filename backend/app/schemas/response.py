from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field


T = TypeVar(
    "T"
)


class ApiResponse(
    BaseModel,
    Generic[T],
):
    """
    Standard API response wrapper.

    Used by all FastAPI endpoints.

    Example:

        {
            "success": true,
            "message": "Resume uploaded",
            "data": {...}
        }
    """


    success: bool = Field(
        ...,
        description="Request success status",
    )


    message: str = Field(
        ...,
        description="Human readable response message",
    )


    data: T | None = Field(
        default=None,
        description="Response payload",
    )


    error: str | None = Field(
        default=None,
        description="Error details when request fails",
    )