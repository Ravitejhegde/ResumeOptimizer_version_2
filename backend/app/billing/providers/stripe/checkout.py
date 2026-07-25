from .client import StripeClient


class StripeCheckout:

    def __init__(self):

        self.stripe = (
            StripeClient().client
        )

    def create(

        self,

        *,

        customer: str,

        price_id: str,

        success_url: str,

        cancel_url: str,

        client_reference_id: str,

        metadata: dict | None = None,

        trial_days: int | None = None,

        allow_promotion_codes: bool = True,

        automatic_tax: bool = True,

    ):

        subscription_data = {

            "metadata": metadata or {},

        }

        if trial_days:

            subscription_data[
                "trial_period_days"
            ] = trial_days

        return self.stripe.checkout.Session.create(

            mode="subscription",

            customer=customer,

            line_items=[

                {

                    "price": price_id,

                    "quantity": 1,

                }

            ],

            success_url=success_url,

            cancel_url=cancel_url,

            client_reference_id=client_reference_id,

            allow_promotion_codes=allow_promotion_codes,

            automatic_tax={

                "enabled": automatic_tax,

            },

            subscription_data=subscription_data,

            metadata=metadata or {},

        )

    def retrieve(

        self,

        session_id: str,

    ):

        return self.stripe.checkout.Session.retrieve(

            session_id

        )

    def expire(

        self,

        session_id: str,

    ):

        return self.stripe.checkout.Session.expire(

            session_id

        )