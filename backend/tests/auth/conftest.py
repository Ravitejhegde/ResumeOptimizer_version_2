from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.database.base import Base
from app.database.models import *  # noqa: F401,F403


# ==========================================================
# Test Database
# ==========================================================

_test_url = make_url(settings.DATABASE_URL).set(
    database="resume_optimizer_test"
)

TEST_DATABASE_URL = _test_url.render_as_string(
    hide_password=False
)


engine = create_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)


# ==========================================================
# Database Lifecycle
# ==========================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create application tables in the isolated test database.
    """

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

    engine.dispose()


# ==========================================================
# Database Session
# ==========================================================

@pytest.fixture
def db() -> Session:
    """
    Provide a database session for an individual test.
    """

    session = TestingSessionLocal()

    try:
        yield session
        session.rollback()
    finally:
        session.close()