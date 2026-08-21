from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentMethod:
    """
    Provider-neutral payment method definition.

    This model describes a payment method available to a customer.
    It does not contain provider-specific implementation details.
    """

    code: str
    name: str
    country_code: str
    currency_code: str
    priority: int = 100
    active: bool = True

    def is_available(self) -> bool:
        """
        Return whether this payment method is currently available.
        """
        return self.active