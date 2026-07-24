from datetime import datetime

from .browser_id import BrowserID
from .guest_repository import GuestRepository
from .models import GuestIdentity


class GuestService:

    @classmethod
    def create_guest(
        cls,
        country: str,
        language: str,
        user_agent: str,
        ip_address: str | None = None,
    ) -> GuestIdentity:

        guest = GuestIdentity(

            guest_id=BrowserID.generate(),

            created_at=datetime.utcnow(),

            last_seen=datetime.utcnow(),

            country=country,

            language=language,

            user_agent=user_agent,

            ip_address=ip_address,

        )

        GuestRepository.save(
            guest
        )

        return guest

    @classmethod
    def get_guest(
        cls,
        guest_id: str,
    ) -> GuestIdentity | None:

        return GuestRepository.get(
            guest_id
        )