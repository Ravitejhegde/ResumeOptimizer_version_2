from __future__ import annotations

from app.database.session import SessionLocal
from app.database.seed.seed_database import seed_database


def initialize_database() -> None:
    """
    Initialize database.

    Responsibilities:
    - Create session
    - Run seed data
    - Close session
    """

    db = SessionLocal()

    try:
        seed_database(db)

    finally:
        db.close()