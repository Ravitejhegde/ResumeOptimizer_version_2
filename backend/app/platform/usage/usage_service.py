from datetime import datetime

from .events import UsageEvent
from .models import Usage
from .usage_repository import UsageRepository


class UsageService:

    @classmethod
    def get_or_create(
        cls,
        identity_id: str,
    ) -> Usage:

        usage = UsageRepository.get(identity_id)

        if usage:

            return usage

        now = datetime.utcnow()

        usage = Usage(

            identity_id=identity_id,

            created_at=now,

            updated_at=now,

        )

        UsageRepository.save(usage)

        return usage

    @classmethod
    def record(
        cls,
        identity_id: str,
        event: UsageEvent,
    ) -> Usage:

        usage = cls.get_or_create(identity_id)

        if event == UsageEvent.UPLOAD:
            usage.uploads += 1

        elif event == UsageEvent.ANALYZE:
            usage.analyses += 1

        elif event == UsageEvent.OPTIMIZE:
            usage.optimizations += 1

        elif event == UsageEvent.DOWNLOAD:
            usage.downloads += 1

        usage.updated_at = datetime.utcnow()

        UsageRepository.save(usage)

        return usage