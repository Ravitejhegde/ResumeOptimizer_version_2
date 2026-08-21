from app.database.models.payment_transaction import PaymentTransaction


def test_payment_transaction_is_successful():
    transaction = PaymentTransaction(status="paid")

    assert transaction.is_successful is True


def test_payment_transaction_is_not_successful():
    transaction = PaymentTransaction(status="failed")

    assert transaction.is_successful is False