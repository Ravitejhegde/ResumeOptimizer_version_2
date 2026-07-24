from typing import Dict

from .models import GuestIdentity


class GuestRepository:
    """
    Temporary in-memory repository.

    Replace with PostgreSQL later.
    """

    _guests: Dict[str, GuestIdentity] = {}

    @classmethod
    def save(
        cls,
        guest: GuestIdentity,
    ) -> None:

        cls._guests[guest.guest_id] = guest

    @classmethod
    def get(
        cls,
        guest_id: str,
    ) -> GuestIdentity | None:

        return cls._guests.get(
            guest_id
        )

    @classmethod
    def exists(
        cls,
        guest_id: str,
    ) -> bool:

        return guest_id in cls._guests