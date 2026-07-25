from .client import StripeClient


class StripeCustomer:

    def __init__(self):

        self.stripe = (
            StripeClient().client
        )

    def create(

        self,

        email: str,

        name: str,

        metadata: dict | None = None,

    ):

        return self.stripe.Customer.create(

            email=email,

            name=name,

            metadata=metadata or {},

        )

    def retrieve(

        self,

        customer_id: str,

    ):

        return self.stripe.Customer.retrieve(

            customer_id

        )

    def update(

        self,

        customer_id: str,

        **kwargs,

    ):

        return self.stripe.Customer.modify(

            customer_id,

            **kwargs,

        )

    def delete(

        self,

        customer_id: str,

    ):

        return self.stripe.Customer.delete(

            customer_id

        )

    def search(

        self,

        email: str,

    ):

        customers = self.stripe.Customer.list(

            email=email,

            limit=1,

        )

        if customers.data:

            return customers.data[0]

        return None