from sqlalchemy.orm import Session

from app.database.models.feature import Feature
from app.database.models.plan import Plan
from app.database.models.plan_feature import PlanFeature
from app.database.models.pricing import Pricing


def seed_database(db: Session) -> None:
    """
    Seed default application data.
    Safe to execute multiple times.
    """

    if db.query(Feature).first():
        return

    # --------------------------------------------------
    # Feature
    # --------------------------------------------------

    feature = Feature(
        code="resume_optimization",
        name="Resume Optimization",
        description="Optimize resumes using AI.",
    )

    db.add(feature)
    db.flush()

    # --------------------------------------------------
    # Plan
    # --------------------------------------------------

    plan = Plan(
        code="free",
        name="Free",
        description="Free Plan",
    )

    db.add(plan)
    db.flush()

    # --------------------------------------------------
    # Plan Feature
    # --------------------------------------------------

    plan_feature = PlanFeature(
        plan_id=plan.id,
        feature_id=feature.id,
        value="10",
        active=True,
    )

    db.add(plan_feature)

    # --------------------------------------------------
    # Pricing
    # --------------------------------------------------

    pricing = Pricing(
        plan_id=plan.id,
        country_code="IN",
        currency_code="INR",
        monthly_price=0,
        yearly_price=0,
        payment_provider="internal",
    )

    db.add(pricing)

    db.commit()