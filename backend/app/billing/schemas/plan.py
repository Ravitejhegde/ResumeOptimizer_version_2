from pydantic import BaseModel
from pydantic import ConfigDict


class PlanResponse(BaseModel):
    """
    Subscription plan returned to clients.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    code: str

    name: str

    description: str | None

    active: bool




