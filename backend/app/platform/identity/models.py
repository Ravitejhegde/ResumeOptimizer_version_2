from dataclasses import dataclass
from datetime import datetime


@dataclass
class GuestIdentity:
    """
    Represents a visitor before login.
    """

    guest_id: str

    created_at: datetime

    last_seen: datetime

    country: str

    language: str

    user_agent: str

    ip_address: str | None = None

    user_id: str | None = None