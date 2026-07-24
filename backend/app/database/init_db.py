"""
Database initialization.

Creates all database tables and
seeds default application data.
"""

from sqlalchemy.orm import Session

from app.database.base import Base
from app.database.database import SessionLocal
from app.database.database import engine
from app.database.seed import seed_database

# --------------------------------------------------
# Import ALL models
# --------------------------------------------------

from app.database.models.user import User
from app.database.models.workspace import Workspace

from app.database.models.resume import Resume
from app.database.models.optimization_job import OptimizationJob
from app.database.models.generated_resume import GeneratedResume
from app.database.models.download import Download

from app.database.models.guest_session import GuestSession
from app.database.models.usage_event import UsageEvent

from app.database.models.feature import Feature
from app.database.models.plan import Plan
from app.database.models.plan_feature import PlanFeature
from app.database.models.pricing import Pricing
from app.database.models.order import Order
from app.database.models.payment_transaction import PaymentTransaction
from app.database.models.subscription import Subscription


def initialize_database() -> None:
    """
    Creates all tables and seeds
    initial application data.
    """

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed data
    db: Session = SessionLocal()

    try:
        seed_database(db)

    finally:
        db.close()