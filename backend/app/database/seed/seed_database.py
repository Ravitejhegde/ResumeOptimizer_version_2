from sqlalchemy.orm import Session


def seed_database(db: Session) -> None:
    """
    Seed initial application data.
    """

    # Add default plans/features/pricing here

    db.commit()