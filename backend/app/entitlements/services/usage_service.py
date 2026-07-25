from datetime import datetime
from datetime import timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models.usage_event import (
    UsageEvent,
)


class UsageService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def usage_count(

        self,

        user_id: str,

        feature_code: str,

        start: datetime,

        end: datetime,

    ) -> int:

        count = (

            self.db.query(

                func.count(
                    UsageEvent.id
                )

            )

            .filter(

                UsageEvent.user_id
                == user_id,

                UsageEvent.feature_code
                == feature_code,

                UsageEvent.created_at
                >= start,

                UsageEvent.created_at
                < end,

            )

            .scalar()

        )

        return count or 0

    def month_usage(

        self,

        user_id: str,

        feature_code: str,

    ) -> int:

        now = datetime.utcnow()

        start = datetime(

            now.year,

            now.month,

            1,

        )

        if now.month == 12:

            end = datetime(

                now.year + 1,

                1,

                1,

            )

        else:

            end = datetime(

                now.year,

                now.month + 1,

                1,

            )

        return self.usage_count(

            user_id,

            feature_code,

            start,

            end,

        )

    def today_usage(

        self,

        user_id: str,

        feature_code: str,

    ) -> int:

        today = datetime.utcnow()

        start = datetime(

            today.year,

            today.month,

            today.day,

        )

        end = start + timedelta(days=1)

        return self.usage_count(

            user_id,

            feature_code,

            start,

            end,

        )

    def add(

        self,

        user_id: str,

        feature_code: str,

        amount: int = 1,

    ) -> UsageEvent:

        event = UsageEvent(

            user_id=user_id,

            feature_code=feature_code,

            amount=amount,

        )

        self.db.add(event)

        self.db.commit()

        self.db.refresh(event)

        return event