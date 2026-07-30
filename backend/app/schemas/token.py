from __future__ import annotations

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Authentication token response.
    """

    access_token: str

    refresh_token: str | None = None

    token_type: str = "bearer"



class UserResponse(BaseModel):
    """
    User information response.

    Used when returning authenticated
    user details from API endpoints.
    """

    id: str

    name: str

    email: str