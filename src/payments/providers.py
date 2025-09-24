"""Payment providers: sandbox implementations for Stripe, Daraja(M-Pesa), Binance Pay, TON."""
from payments.payment_stub import PaymentStub
from logger_setup import get_logger
from storage.db import init_db

log = get_logger(__name__)
conn = init_db()

class StripeProvider(PaymentStub):
    def __init__(self):
        super().__init__('stripe')

    def create_payment(self, user_id, amount_cents, currency='USD'):
        intent = self.create_payment_intent(amount_cents, currency, metadata={'user_id':user_id})
        # simulate immediate success in sandbox
        return {'status':'succeeded','id':intent['id'], 'amount':intent['amount']}

class MpesaProvider(PaymentStub):
    def __init__(self):
        super().__init__('mpesa')

    def create_payment(self, user_phone, amount_cents):
        return {'status':'pending', 'id':'mpesa_mock_123', 'phone':user_phone}

class BinancePayProvider(PaymentStub):
    def __init__(self):
        super().__init__('binancepay')

    def create_payment(self, user_id, amount_cents):
        return {'status':'succeeded','id':'binance_mock_123','amount':amount_cents}
