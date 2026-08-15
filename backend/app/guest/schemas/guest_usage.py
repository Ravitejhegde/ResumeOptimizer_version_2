from pydantic import BaseModel, Field


class GuestUsageResponse(BaseModel):
    """
    Current free usage available to an anonymous guest.
    """

    is_guest: bool

    free_samples: int

    used_samples: int

    earned_samples: int

    remaining_samples: int

    can_optimize: bool

    share_rewards: int

    max_share_rewards: int


class GuestShareRewardRequest(BaseModel):
    """
    Request to claim a guest sharing reward.
    """

    session_token: str = Field(
        min_length=1,
        max_length=255,
    )


class GuestShareRewardResponse(BaseModel):
    """
    Result of a successfully claimed sharing reward.
    """

    message: str

    reward_samples: int

    usage: GuestUsageResponse


class GuestOptimizationRequest(BaseModel):
    """
    Request to optimize a guest resume.
    """

    session_token: str = Field(
        min_length=1,
        max_length=255,
    )

    resume_id: str = Field(
        min_length=1,
        max_length=36,
    )

    job_description: str = Field(
        min_length=10,
        max_length=20000,
    )