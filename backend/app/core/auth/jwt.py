from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(
    subject: str,
    expires_minutes: int = 60,
) -> str:
    """
    Create JWT access token.
    """

    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=expires_minutes)
    )

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict:

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[ALGORITHM],
    )