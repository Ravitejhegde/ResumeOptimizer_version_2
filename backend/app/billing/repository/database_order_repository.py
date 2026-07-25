from sqlalchemy.orm import Session

from app.database.models.order import Order


class DatabaseOrderRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    def create(
        self,
        order: Order,
    ) -> Order:

        self.db.add(order)

        self.db.commit()

        self.db.refresh(order)

        return order

    def update(
        self,
        order: Order,
    ) -> Order:

        self.db.commit()

        self.db.refresh(order)

        return order

    def get(
        self,
        order_id: str,
    ) -> Order | None:

        return (

            self.db.query(Order)

            .filter(

                Order.id == order_id

            )

            .first()

        )

    def by_user(
        self,
        user_id: str,
    ) -> list[Order]:

        return (

            self.db.query(Order)

            .filter(

                Order.user_id == user_id

            )

            .order_by(

                Order.created_at.desc()

            )

            .all()

        )

    def pending(
        self,
        user_id: str,
    ) -> list[Order]:

        return (

            self.db.query(Order)

            .filter(

                Order.user_id == user_id,

                Order.status == "pending",

            )

            .order_by(

                Order.created_at.desc()

            )

            .all()

        )

    def successful(
        self,
        user_id: str,
    ) -> list[Order]:

        return (

            self.db.query(Order)

            .filter(

                Order.user_id == user_id,

                Order.status == "paid",

            )

            .order_by(

                Order.created_at.desc()

            )

            .all()

        )

    def delete(
        self,
        order: Order,
    ) -> None:

        self.db.delete(order)

        self.db.commit()