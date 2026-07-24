from dataclasses import dataclass

from .feature_flags import FEATURE_FLAGS


@dataclass(frozen=True)
class Plan:

    id: str

    name: str

    optimization_limit: int

    resume_history: bool

    pdf_download: bool

    priority_queue: bool


FREE = Plan(
    id="free",
    name="Free",
    optimization_limit=3,
    resume_history=False,
    pdf_download=False,
    priority_queue=False,
)

PRO = Plan(
    id="pro",
    name="Pro",
    optimization_limit=-1,
    resume_history=True,
    pdf_download=True,
    priority_queue=True,
)

TEAM = Plan(
    id="team",
    name="Team",
    optimization_limit=-1,
    resume_history=True,
    pdf_download=True,
    priority_queue=True,
)

PLANS = {
    FREE.id: FREE,
    PRO.id: PRO,
    TEAM.id: TEAM,
}