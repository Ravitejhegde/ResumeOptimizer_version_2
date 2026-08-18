from __future__ import annotations

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import models  # noqa: F401
from app.database.base import Base


@pytest.fixture
def test_engine():
    """
    Create a fresh in-memory SQLite database
    for each test.
    """

    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def db_session(
    test_engine,
) -> Generator[Session, None, None]:
    """
    Provide an isolated SQLAlchemy session for each test.
    """

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=test_engine,
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def db(
    db_session: Session,
) -> Session:
    """
    Backward-compatible alias for db_session.
    """

    return db_session