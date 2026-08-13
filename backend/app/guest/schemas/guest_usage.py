from pydantic import BaseModel


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