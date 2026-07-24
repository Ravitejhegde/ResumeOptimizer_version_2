from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:

    id: str

    email: str

    name: str

    plan: str

    provider: str

    verified: bool

    created_at: datetime

    updated_at: datetime

    last_login: datetime | None = None

    guest_id: str | None = None

    country: str | None = None

    language: str = "en"

    active: bool = True