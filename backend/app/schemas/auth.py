from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


# ==========================================================
# Register Request
# ==========================================================

class RegisterRequest(BaseModel):
    """
    Request payload for creating a new user account.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=[
            "Raviteja Hegde"
        ],
        description="User full name",
    )

    email: EmailStr = Field(
        ...,
        examples=[
            "user@example.com"
        ],
        description="User email address",
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=[
            "password123"
        ],
        description="User account password",
    )


# ==========================================================
# Login Request
# ==========================================================

class LoginRequest(BaseModel):
    """
    Request payload for normal application login.
    """

    email: EmailStr = Field(
        ...,
        examples=[
            "user@example.com"
        ],
        description="Registered email address",
    )

    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        examples=[
            "password123"
        ],
        description="Account password",
    )


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "teju2@gmail.com",
                    "password": "Teju2103",
                }
            ]
        }
    }